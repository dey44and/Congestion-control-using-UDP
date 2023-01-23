import random
import socket
import sys
import time
from datetime import datetime

import select

from Commander.commands import *
from Entity import utility as util
from Entity.entity import Entity
from Packets import packet_items as packets

path = "./Root/"


# noinspection PyBroadException
class Server(Entity):
    def __init__(self, source_port: str, dest_port: str, ip: str, sleep_time, err_rate: float):
        # Call super constructor
        super().__init__()

        # Initialize attributes
        self.__source_port: int = int(source_port)
        self.__dest_port: int = int(dest_port)
        self.__ip: str = ip

        # Config UDP Socket
        self.__sock: socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.__sleep_time = sleep_time
        self.__sock.settimeout(self.__sleep_time)

        # Communication attributes
        self.running = False
        self.timeout_socket = 1
        self.__state = "Idle"
        self.__multireceive_mode = None
        self.__err_rate = err_rate
        self.__pckts = dict()

    def run(self):
        # Create UDP Socket
        global packet
        try:
            self.__sock.bind((self.__ip, self.__source_port))
            self.running = True

            # Append history to debug
            with open("../DebugSection/debug_server.txt", 'a') as file:
                date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                file.write(f"\n{date_time}: Server is starting connection on ({self.__ip}, {self.__source_port})\n")
                file.close()

            # Server Execution
            while self.running:
                # We call select function to check the buffer for data using a timeout of one second
                receive, _, _ = select.select([self.__sock], [], [], self.timeout_socket)
                if receive:
                    # If server is in idle state, he is ready to receive and to send one packet
                    if self.__state == "Idle":
                        self.__receive_one_packet_handler()
                    # If server is in watch congestion state, he is ready to receive and to send more packets
                    elif self.__state == "Watch":
                        self.__receive_more_packets_handler()
                time.sleep(self.__sleep_time)
        except:
            # Append history to debug
            with open("../DebugSection/debug_server.txt", 'a') as file:
                date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                file.write(f"\n{date_time}: Server is closing connection.\n")
                file.close()
            sys.exit(-1)

    # Handler for one packet receive
    def __receive_one_packet_handler(self):
        # Get data from Client
        global pckt
        data, address = self.__sock.recvfrom(1024)

        # Append history to debug
        with open("../DebugSection/debug_server.txt", 'a') as file:
            date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            file.write(f"{date_time}: Receive UDP datagram from: {address}.\n")
            file.close()

        # Unpack data and process it
        control = data[0]
        if control == packets.CONTROL_INSTR:
            instruction = data[1]

            # List file instruction
            if instruction == packets.LIST_FILES:
                pckt = list_files_packet()
            # Add file instruction
            elif instruction == packets.CREATE_FILE:
                pckt = create_file_packet(data)
            # Append to file instruction
            elif instruction == packets.APPEND_FILE:
                # Add packet to dictionary
                self.__pckts[data[2]] = data
                # Create response
                pckt = append_to_file_packet_response(data)

                # Start congestion control
                self.__state = "Watch"
                self.__multireceive_mode = packets.APPEND_FILE
            # Remove file instruction
            elif instruction == packets.REMOVE_FILE:
                pckt = remove_file_packet(data)

            # Send packet to client
            self.__sock.sendto(pckt, address)

            # Append history to debug
            with open("../DebugSection/debug_server.txt", 'a') as file:
                date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                file.write(f"{date_time}: Server send UDP datagram '{control} - {instruction}' to: "
                           f"{address}.\n")
                file.close()
        elif control == packets.CONTROL_CONN:
            instruction = data[1]

            # Check for leave connection
            if instruction == packets.CONN_LEAVE:
                # Append history to debug
                with open("../DebugSection/debug_server.txt", 'a') as file:
                    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    file.write(f"{date_time}: Client ('{self.__ip}', {self.__dest_port}) disconnected from "
                               f"server.\n")
                    file.close()

    # Handler for more packets receive
    def __receive_more_packets_handler(self):
        packets_list = []
        client_adress = None
        # Wait in a loop for packets
        while True:
            # Try to get data from the client
            try:
                data, address = self.__sock.recvfrom(1024)
                client_adress = address
                packets_list.append(data)

            except:
                # If no packet arrived, stop waiting
                break

        # Process every packet and send back response
        if self.__multireceive_mode == packets.APPEND_FILE:
            # For every packet, we format and send back response
            for packet_item in packets_list:
                # Check if is an over packet
                if packet_item[0] == packets.CONTROL_CONN and packet_item[1] == packets.CONN_OVER:
                    # Create a run to save data, then clear data
                    write_to_file(self.__pckts)
                    self.__pckts.clear()

                    # Go back to idle state
                    self.__state = "Idle"
                    self.__multireceive_mode = None
                # Otherwise, the packet belongs to transmission
                else:
                    # Add packet to dictionary
                    self.__pckts[packet_item[2]] = packet_item

                    # Create response
                    pcktt = append_to_file_packet_response(packet_item)

                    # Send packet to client
                    val = random.uniform(0, 1)
                    if val > self.__err_rate:
                        self.__sock.sendto(pcktt, client_adress)

                    # Append history to debug
                    with open("../DebugSection/debug_server.txt", 'a') as file:
                        date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        file.write(f"{date_time}: Server send UDP datagram '{pcktt[0]} - {pcktt[1]}' to: "
                                   f"{client_adress}.\n")
                        file.close()
                # Append history to debug
                with open("../DebugSection/debug_server.txt", 'a') as file:
                    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    file.write(f"{date_time}: Receive UDP datagram from: {client_adress}.\n")
                    file.close()

    # Handler for one packet send
    def __send_one_packet_handler(self):
        pass


if __name__ == "__main__":
    # Read UDP data from sysargv
    if len(sys.argv) != 3:
        print("help : ")
        print("  --sport=source_port ")
        print("  --dip=peer_ip ")
        sys.exit()

    # Get arguments and initialize Server object
    s_port, d_ip = util.get_arguments(sys.argv)
    udp_sleep_time = 0.01
    udp_err_rate = 0.05

    # Try to start the server
    try:
        if not util.is_valid_ip(d_ip) or not util.is_valid_port(s_port):
            raise Exception()
        server: Server = Server(s_port, "0", d_ip, udp_sleep_time, udp_err_rate)

        # Start server connection
        server.start()

        # Stop server
        server.join()

        # Append history to debug
        with open("../DebugSection/debug_server.txt", 'a') as f:
            date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"\n{date}: Server is closing connection.\n")
            f.close()
    except:
        sys.exit(-1)
