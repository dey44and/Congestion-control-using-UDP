import socket
from datetime import datetime
import select
import time

from CongestionControl.SenderControl import SenderControl
from Entity.entity import Entity
from Packets import packet_items as packets
from Packets.packet_factory import PacketFactory
from Statistics.stats import Stats


# noinspection PyBroadException
class Client(Entity):
    def __init__(self, source_port: str, dest_port: str, ip: str, sleep_time):
        # Call super constructor
        super().__init__()

        # Initialize attributes
        self.__source_port: int = int(source_port)
        self.__dest_port: int = int(dest_port)
        self.__ip: str = ip
        self.__queue = []

        # Config UDP Socket
        self.__sock: socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.__sleep_time = sleep_time
        self.__sock.settimeout(self.__sleep_time)

        # Communication attributes
        self.__running = False
        self.__timeout_socket = 1
        self.__state = "Idle"
        self.__controller = SenderControl()
        self.__unsend_packets = []
        self.__multireceive_mode = None

        self.__send_packets = None
        self.__packets_to_send = None

        self.__current_session_send_packets = 0
        self.__retransmissions = 0

        # Statistics part
        self.__stats = Stats()

    def run(self):
        # Create UDP Socket
        self.__sock.bind((self.__ip, self.__source_port))
        self.__running = True

        # Append history to debug
        with open("../DebugSection/debug_client.txt", 'a') as f:
            date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"{date}: Client ('{self.__ip}', {self.__source_port}) is connecting to server.\n")
            f.close()

        # Client execution
        while self.__running:
            # We call select function to check the buffer for data using a timeout of one second
            r, _, _ = select.select([self.__sock], [], [], 1)
            # If client receive data, it will process it
            if r:
                # If client is in idle state, he is ready to receive one packet
                if self.__state == "Idle":
                    self.__receive_one_packet_handler()
                # If client is in watch congestion state, he is ready to receive more packets
                elif self.__state == "Watch":
                    self.__receive_more_packets_handler()
            # Otherwise, he will send a packet from queue
            else:
                # If client is in idle state, he is ready to send one packet
                if self.__state == "Idle":
                    self.__send_one_packet_handler()
                # If client is in watch congestion state, he is ready to send more packests
                elif self.__state == "Watch":
                    self.__send_more_packets_handler()
            time.sleep(self.__sleep_time)

    def add_packet(self, packet: bytes):
        self.__queue.append(packet)

    def set_packets_to_send(self, packets_number: int):
        self.__packets_to_send = packets_number

    # Handler for one packet receive
    def __receive_one_packet_handler(self):
        # Get data from server
        data, address = self.__sock.recvfrom(1024)

        # Append history to debug
        with open("../DebugSection/debug_client.txt", 'a') as f:
            date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"{date}: Receive UDP datagram from: {address}.\n")
            f.close()

        # Handle packet content
        control = data[0]
        if control == packets.CONTROL_RESPONSE:
            instruction = data[1]
            if instruction == packets.LIST_FILES or instruction == packets.CREATE_FILE \
                    or instruction == packets.APPEND_FILE or instruction == packets.REMOVE_FILE:
                content = data[2:].decode('utf-8')
                print(content)
            elif instruction == packets.CONN_ACK:
                content = data[2]
                print(f"Server waits for packet with number {content}")

    # Handler for more packet receive
    def __receive_more_packets_handler(self):
        if self.__multireceive_mode == packets.APPEND_FILE:
            packets_list = []
            server_adress = None

            # We wait for packets while timeout is not reached
            finish_time = time.time() + self.__sleep_time
            while time.time() < finish_time:
                # Get data from server
                try:
                    data, address = self.__sock.recvfrom(1024)
                    server_adress = address
                    # Push data to packets list
                    packets_list.append(data)
                except:
                    break

            # Check packets integrity
            next_packet = -1
            received_packets = 0
            for packet in packets_list:
                # Check if packet is of type aknowledge
                if packet[0] == packets.CONTROL_RESPONSE and packet[1] == packets.CONN_ACK:
                    # Print packet info
                    print(f"Server waits for packet with number {packet[2]}")

                    received_packets += 1
                    if next_packet == -1:
                        next_packet = packet[2]
                    elif next_packet + 1 == packet[2]:
                        next_packet = packet[2]
                    else:
                        next_packet = -1
                        break

                # Append history to debug
                with open("../DebugSection/debug_client.txt", 'a') as f:
                    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    f.write(f"{date}: Receive UDP datagram from: {server_adress}.\n")
                    f.close()

            # Check if next_packet != get_recv_packets() + 1
            if next_packet != self.__controller.get_send_packets() + 1 or received_packets != \
                    self.__current_session_send_packets:
                # Then inform controller that some packets are not send
                self.__controller.packet_lost(self.__send_packets)
            else:
                # Update number of sent packets
                self.__send_packets = self.__controller.get_send_packets()

                # Clear queue of packets
                self.__unsend_packets.clear()

                # Update stats
                self.__stats.add_point(received_packets)

                # If client send all packets, go back to idle
                if self.__packets_to_send == self.__send_packets:
                    self.__controller.reset()
                    self.__state = "Idle"
                    self.__multireceive_mode = None

                    # and generate a plot
                    self.__stats.save_plot()

                    # and notify server that transmition is over
                    items = ["over"]
                    packet = PacketFactory(items).get_packet()
                    self.__sock.sendto(packet, server_adress)

                    # Append history to debug
                    with open("../DebugSection/debug_client.txt", 'a') as f:
                        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        f.write(f"{date}: Client ('{self.__ip}', {self.__source_port}) send UDP datagram "
                                f"'{packet[0]} - {packet[1]}' to: ('{self.__ip}', {self.__source_port}).\n")
                        f.close()

                    print("INFO: Announce server that transmission is over.")

                # Info for debug
                print("INFO: All packets from current window were send!")

            print(f"Number of sended packets until now is {self.__send_packets}\n")
            print(f"Size of cwnd is {self.__controller.get_cwnd()}")

    # Handler for one packet send
    def __send_one_packet_handler(self):
        # Check if queue is not empty
        if len(self.__queue) > 0:
            # Get first packet and send it to server
            packet = self.__queue.pop(0)
            self.__sock.sendto(packet, (self.__ip, self.__dest_port))

            # Check for append to file packet (needs congestion control)
            if packet[0] == packets.CONTROL_INSTR and packet[1] == packets.APPEND_FILE:
                # Client enter in congestion avoidance state and it reinitialize controller
                print(f"Client will send to server {self.__packets_to_send} packets.")
                print(f"Client send packet with number {packet[2]}")
                self.__state = "Watch"
                self.__multireceive_mode = packets.APPEND_FILE
                self.__send_packets = 1
                self.__controller.reset()
                self.__controller.update_cwnd()
                self.__current_session_send_packets = 1

            # Check for leave packet
            elif packet[0] == packets.CONTROL_CONN and packet[1] == packets.CONN_LEAVE:
                self.__running = False
                # Append history to debug
                with open("../DebugSection/debug_client.txt", 'a') as f:
                    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    f.write(f"{date}: Client ('{self.__ip}', {self.__source_port}) send UDP datagram "
                            f"'{packet[0]} - {packet[1]}' to: ('{self.__ip}', {self.__source_port}).\n")
                    f.write(f"{date}: Client ('{self.__ip}', {self.__source_port}) disconnected from server.\n")
                    f.close()
                self.__running = False

            # Append history to debug
            with open("../DebugSection/debug_client.txt", 'a') as f:
                date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                f.write(f"{date}: Client ('{self.__ip}', {self.__source_port}) send UDP datagram "
                        f"'{packet[0]} - {packet[1]}' to: ('{self.__ip}', {self.__source_port}).\n")
                f.close()

    # Handler for more packet receive
    def __send_more_packets_handler(self):
        # Get congestion window size and send next cwnd packets
        cwnd_len = self.__controller.get_cwnd()

        self.__current_session_send_packets = 0

        # If there are packets unsend, we send them again, without change value of cwnd
        if len(self.__unsend_packets) > 0:
            # If client have tried for 3 times, we clear the not send queue and restart the send process
            if self.__retransmissions == 3:
                # We reset transmissions, and we put back packets to the queue
                print("INFO: 2 failed retransmissions, reset all")
                self.__retransmissions = 0

                # Then inform controller that some packets are not send
                self.__controller.packet_lost(self.__send_packets)

                # Put back packets and clear queue
                for i in range(0, len(self.__unsend_packets)):
                    self.__queue.insert(i, self.__unsend_packets[i])
                self.__unsend_packets.clear()

            else:
                # Increment the value of retransmissions
                self.__retransmissions += 1

                # Clone the not send packets
                unsend_packets_clone = []
                for packet in self.__unsend_packets:
                    unsend_packets_clone.append(packet)

                # Go through packets and send them
                while len(self.__unsend_packets) > 0:
                    # Resend packets
                    packet = self.__unsend_packets.pop(0)
                    self.__sock.sendto(packet, (self.__ip, self.__dest_port))
                    print(f"Client send packet with number {packet[2]}")

                    # Update congestion control
                    self.__controller.increment_packets()
                    self.__current_session_send_packets += 1

                    # Append history to debug
                    with open("../DebugSection/debug_client.txt", 'a') as f:
                        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        f.write(f"{date}: Client ('{self.__ip}', {self.__source_port}) send UDP datagram "
                                f"'{packet[0]} - {packet[1]}' to: ('{self.__ip}', {self.__source_port}).\n")
                        f.close()

                # Get back unsed packets
                self.__unsend_packets = unsend_packets_clone

        # If all packets were send succesful, we continue with next packets
        else:
            # Reset number of retransmissions
            self.__retransmissions = 0

            for i in range(0, cwnd_len):
                # If client process all packets, stop the loop
                if len(self.__queue) == 0:
                    break

                # Otherwise, get and send the packet
                pckt = self.__queue.pop(0)
                self.__sock.sendto(pckt, (self.__ip, self.__dest_port))
                print(f"Client send packet with number {pckt[2]}")

                # Update control for congestion
                self.__unsend_packets.append(pckt)
                self.__controller.update_cwnd()
                self.__current_session_send_packets += 1

                # Append history to debug
                with open("../DebugSection/debug_client.txt", 'a') as f:
                    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    f.write(f"{date}: Client ('{self.__ip}', {self.__source_port}) send UDP datagram "
                            f"'{pckt[0]} - {pckt[1]}' to: ('{self.__ip}', {self.__source_port}).\n")
                    f.close()
