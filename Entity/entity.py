from threading import Thread


class Entity(Thread):
    def __init__(self):
        # Call the thread constructor
        super().__init__()

    # Run method remain to be overrided
    def run(self):
        pass

    # Handler for one packet receive
    def __receive_one_packet_handler(self):
        pass

    # Handler for one packet send
    def __send_one_packet_handler(self):
        pass
