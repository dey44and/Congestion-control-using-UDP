from struct import pack


class PacketBuilder(object):
    def __init__(self, packet_type: str):
        self.__control: int = 0
        self.__command: int = 0
        self.__packet_number: int = 0
        self.__packets: int = 0
        self.__type: str = packet_type

    # Set control value
    def set_control(self, control_type: int):
        self.__control = control_type

    # Set type value
    def set_type(self, packet_type: str):
        self.__type = packet_type

    # Set command value
    def set_command(self, command_type: int):
        self.__command = command_type

    # Set packet number
    def set_packet_number(self, packet_number: int):
        self.__packet_number = packet_number

    # Set packets
    def set_packets(self, packets: int):
        self.__packets = packets

    # Generate packet
    def generate_packet(self) -> bytes:
        if self.__type == "APPEND_SEND":
            return pack('BBBB', self.__control, self.__command, self.__packet_number, self.__packets)
        elif self.__type == "APPEND_RESPONSE":
            return pack('BBB', self.__control, self.__command, self.__packet_number)
        return pack('BB', self.__control, self.__command)
