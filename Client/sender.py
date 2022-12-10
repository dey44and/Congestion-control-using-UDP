import json
import time
import socket
from typing import List, Dict, Tuple, Optional


class Sender(object):

    def __int__(self, sock: socket, data, dip, dport) -> None:
        self.dip = dip
        self.dport = dport
        self.cwnd = 1
        self.default_cwnd = 1
        self.sshtresh = 1000
        self.ack = []
        self.no_ack = 0
        self.send_bytes = 0
        self.manage_congestion = False
        self.current_packet = None

    def get_next_packet(self):
        self.current_packet = self.data[self.send_bytes:self.send_bytes+512]
        self.send_bytes += 512

    def send(self):
        self.get_next_packet()
        if self.cwnd >= self.sshtresh:
            self.sock.send(self.current_packet.encode(), (self.dip, int(self.dport)))
            self.manage_congestion = True

        if self.no_ack > 1:
            self.sshtresh = self.cwnd / 2
            self.cwnd = self.default_cwnd
            self.manage_congestion = False
            # Trimit din nou pachetul
            self.sock.send(self.current_packet.encode(), (self.dip, int(self.dport)))
            self.no_ack = self.no_ack - 1

        if self.manage_congestion:
            self.cwnd = self.cwnd + 1
        else:
            self.cwnd = 2 * self.cwnd

    def recv(self):
        data, address = self.sock.recvfrom(1024)
        decoded_data = json.dumps(data.decode())
        if decoded_data["ack"] <= self.sent_bytes:
            self.no_ack = self.no_ack + 1
            # Trimit din nou pachetul
            self.sock.send(self.current_packet.encode(), (self.dip, int(self.dport)))
        else:
            self.ack.append(decoded_data["ack"])
            self.no_ack = self.no_ack - 1


        