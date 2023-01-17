import os
import socket
import select
import threading
from Utilities import utility as util


# noinspection PyBroadException
class Server(object):
    def __init__(self, source_port, dest_port, ip):
        # Initializare atribute pentru clasa Server
        self.source_port: int = int(source_port)
        self.dest_port: int = int(dest_port)
        self.ip: str = ip
        self.sock: socket = None
        self.execution_thread: threading = None
        self.running = True

    def receive_fct(self):
        # Creare socket UDP
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.bind(('0.0.0.0', self.source_port))

        # Bucla executie server
        contor = 0
        while self.running:
            # Apelam la functia sistem IO -select- pentru a verifca daca socket-ul are date in bufferul de receptie
            # Stabilim un timeout de 1 secunda
            r, _, _ = select.select([self.sock], [], [], 1)
            if not r:
                contor = contor + 1
            else:
                data, address = self.sock.recvfrom(1024)
                instructions = str(data).split(" ")
                result = "Files:\n"
                if instructions[0] == "ls":
                    for subdir, dirs, files in os.walk('./'):
                        for file in files:
                            result += file + "\n"
                    self.sock.sendto(result.encode(), (self.ip, self.dest_port))
                elif instructions[0] == "add":
                    pass
                elif instructions[0] == "rm":
                    pass
                # print("S-a receptionat ", str(data), " de la ", address)
                # print("Contor= ", contor)

    def start_server(self):
        try:
            self.execution_thread = threading.Thread(target=self.receive_fct())
            self.execution_thread.start()
        except:
            print("Error: Starting server gone wrong!")
            sys.exit(-1)


if __name__ == "__main__":
    # Citire nr port din linia de comanda
    if len(sys.argv) != 4:
        print("help : ")
        print("  --sport=numarul_meu_de_port ")
        print("  --dport=numarul_de_port_al_peer-ului ")
        print("  --dip=ip-ul_peer-ului ")
        sys.exit()

    # Obtinere argumente si initializare obiect de tip Server
    s_port, d_port, d_ip = util.get_arguments(sys.argv)
    try:
        if not util.is_valid_ip(d_ip) or not util.is_valid_port(s_port) or not util.is_valid_port(d_port):
            raise Exception()
        server: Server = Server(s_port, d_port, d_ip)
        # Pornire server
        server.start_server()
    except:
        print("Error: Starting server gone wrong!")
        sys.exit(-1)
