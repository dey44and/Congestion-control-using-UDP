import os
import socket
import sys
import time
from datetime import datetime

import select

from Builder.Builder import PacketBuilder
from Utilities import utility as util
from Utilities.entity import Entity
from Utilities import packets


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
        try:
            self.__sock.bind((self.__ip, self.__source_port))
            self.running = True

            # Append history to debug
            with open("debug_server.txt", 'a') as f:
                date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                f.write(f"\n{date}: Server is starting connection on ({self.__ip}, {self.__source_port})\n")
                f.close()

            # Server Execution
            while self.running:
                # We call select function to check the buffer for data using a timeout of one second
                receive, _, _ = select.select([self.__sock], [], [], self.timeout_socket)
                if receive:
                    # Get data from Client
                    data, address = self.__sock.recvfrom(1024)

                    # Append history to debug
                    with open("debug_server.txt", 'a') as f:
                        date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        f.write(f"{date}: Receive UDP datagram from: {address}\n")
                        f.close()

                    # Unpack data and process it
                    control = data[0]
                    if control == packets.CONTROL_INSTR:
                        instruction = data[1]

                        if instruction == packets.LIST_FILES:
                            result = "Files:\n"
                            for subdir, dirs, files in os.walk('./Root'):
                                for file in files:
                                    result += "-> " + file + "\n"

                            # Generate a list file packet
                            builder: PacketBuilder = PacketBuilder()
                            builder.set_control(packets.CONTROL_RESPONSE)
                            builder.set_command(packets.LIST_FILES)

                            # Get packet and send to client
                            packet = builder.generate_packet() + result.encode('utf-8')
                            self.__sock.sendto(packet, (self.__ip, self.__dest_port))

                time.sleep(self.__sleep_time)
        except:
            # Append history to debug
            with open("debug_server.txt", 'a') as f:
                date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                f.write(f"\n{date}: Server is closing connection.\n")
                f.close()
            sys.exit(-1)


if __name__ == "__main__":
    # Read UDP data from sysargv
    if len(sys.argv) != 4:
        print("help : ")
        print("  --sport=source_port ")
        print("  --dport=destination_port ")
        print("  --dip=peer_ip ")
        sys.exit()

    # Get arguments and initialize Server object
    s_port, d_port, d_ip = util.get_arguments(sys.argv)
    udp_sleep_time = 0.01

    # Try to start the server
    try:
        if not util.is_valid_ip(d_ip) or not util.is_valid_port(s_port) or not util.is_valid_port(d_port):
            raise Exception()
        server: Server = Server(s_port, d_port, d_ip, udp_sleep_time)

        # Start server connection
        server.start()

        # Stop server
        server.join()

        # Append history to debug
        with open("debug_server.txt", 'a') as f:
            date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"\n{date}: Server is closing connection.\n")
            f.close()
    except:
        # Append history to debug
        with open("debug_server.txt", 'a') as f:
            date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"\n{date}: Server is closing connection.\n")
            f.close()
        sys.exit(-1)
