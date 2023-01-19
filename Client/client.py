import socket
from datetime import datetime
import select
import time

from Entity.entity import Entity
from Packets import packet_items as packets


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

        self.__running = False
        self.__timeout_socket = 1

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

            # Otherwise, he will send a packet from queue
            else:
                # Check if queue is not empty
                if len(self.__queue) > 0:
                    # Get first packet and send it to server
                    packet = self.__queue.pop(0)
                    self.__sock.sendto(packet, (self.__ip, self.__dest_port))

                    # Check for leave packet
                    if packet[0] == packets.CONTROL_CONN and packet[1] == packets.CONN_LEAVE:
                        self.__running = False
                        # Append history to debug
                        with open("../DebugSection/debug_client.txt", 'a') as f:
                            date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            f.write(f"{date}: Client ('{self.__ip}', {self.__source_port}) send UDP datagram "
                                    f"'{packet[0]} - {packet[1]}' to: ('{self.__ip}', {self.__source_port}).\n")
                            f.write(f"{date}: Client ('{self.__ip}', {self.__source_port}) disconnected from server.\n")
                            f.close()
                        break

                    # Append history to debug
                    with open("../DebugSection/debug_client.txt", 'a') as f:
                        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        f.write(f"{date}: Client ('{self.__ip}', {self.__source_port}) send UDP datagram "
                                f"'{packet[0]} - {packet[1]}' to: ('{self.__ip}', {self.__source_port}).\n")
                        f.close()

            time.sleep(self.__sleep_time)

    def add_packet(self, packet: bytes):
        self.__queue.append(packet)
