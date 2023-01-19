import socket
import sys
import time
from datetime import datetime
import select
from Commander.commands import *
from Entity import utility as util
from Entity.entity import Entity
from Packets import packets

path = "./Root/"


# noinspection PyBroadException
class Server(Entity):
    def __init__(self, source_port: str, dest_port: str, ip: str, sleep_time):
        # Call super constructor
        super().__init__()

        # Initialize attributes
        self.__source_port: int = int(source_port)
        self.__dest_port: int = int(dest_port)
        self.__ip: str = ip

        # Config UDP Socket
        self.__sock: socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.__sleep_time = sleep_time

        self.running = False
        self.timeout_socket = 1

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
                    # Get data from Client
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
                            packet = list_files_packet(data)
                        # Add file instruction
                        elif instruction == packets.CREATE_FILE:
                            packet = create_file_packet(data)
                        # Append to file instruction
                        elif instruction == packets.APPEND_FILE:
                            packet = append_to_file_packet(data)
                        # Remove file instruction
                        elif instruction == packets.REMOVE_FILE:
                            packet = remove_file_packet(data)

                        # Send packet to client
                        self.__sock.sendto(packet, address)

                        # Append history to debug
                        with open("../DebugSection/debug_server.txt", 'a') as file:
                            date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            file.write(f"{date_time}: Send UDP datagram '{control} - {instruction}' to: ({self.__ip}, "
                                       f"{self.__source_port}).\n")
                            file.close()
                    elif control == packets.CONTROL_CONN:
                        instruction = data[1]

                        # Check for leave connection
                        if instruction == packets.CONN_LEAVE:
                            # Append history to debug
                            with open("../DebugSection/debug_server.txt", 'a') as file:
                                date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                                file.write(f"{date_time}: Client ({self.__ip}, {self.__dest_port}) disconnected from "
                                           f"server.\n")
                                file.close()

                time.sleep(self.__sleep_time)
        except:
            # Append history to debug
            with open("../DebugSection/debug_server.txt", 'a') as file:
                date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                file.write(f"\n{date_time}: Server is closing connection.\n")
                file.close()
            sys.exit(-1)


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

    # Try to start the server
    try:
        if not util.is_valid_ip(d_ip) or not util.is_valid_port(s_port):
            raise Exception()
        server: Server = Server(s_port, "0", d_ip, udp_sleep_time)

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
