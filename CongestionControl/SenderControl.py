# A class that implements attributes and behavior of Tahoe Congestion Control Algorithm
class SenderControl(object):
    def __init__(self):
        # Initialize maximum segment size
        self.__mss: int = 1
        # Initialize congestion window size
        self.__cwnd: float = 1
        # Initialize slow start threshold
        self.__ssthresh: int = 65536
        # Set initial state
        self.__state: str = "SlowStart"
        # Set packet number
        self.__packet_number: int = 0

    # Update congestion window
    def update_cwnd(self):
        self.__packet_number += 1

        if self.__state == "SlowStart":
            self.__cwnd += 1
        elif self.__state == "AIMD":
            self.__cwnd += self.__mss * self.__mss / self.__cwnd

        # Check if we are in slow start, and we reach the sstresh
        if self.__state == "SlowStart" and self.__cwnd > self.__ssthresh:
            self.__state = "AIMD"

    # Increment number of packets
    def increment_packets(self):
        self.__packet_number += 1

    # Manage lost packet
    def packet_lost(self, send_packets: int):
        self.__packet_number = send_packets

        if self.__state == "SlowStart":
            self.__state = "AIMD"
        elif self.__state == "AIMD":
            self.__state = "SlowStart"
            self.__ssthresh = int(self.__cwnd / 2)
            self.__cwnd = self.__mss

    # Method to get value of cwnd
    def get_cwnd(self):
        return int(round(self.__cwnd))

    # Method to get number of received packets
    def get_send_packets(self):
        return self.__packet_number

    # Method to reset attributes of algorithm
    def reset(self):
        # Initialize maximum segment size
        self.__mss: int = 1
        # Initialize congestion window size
        self.__cwnd: float = 1
        # Initialize slow start threshold
        self.__ssthresh: int = 65536
        # Set initial state
        self.__state: str = "SlowStart"
        # Set packet number
        self.__packet_number: int = 0
