from struct import pack


class PacketBuilder(object):
    def __init__(self):
        self.__control: int = 0
        self.__command: int = 0

    # Set control value
    def set_control(self, control_type: int):
        self.__control = control_type

    # Set command value
    def set_command(self, command_type: int):
        self.__command = command_type

    # Generate packet
    def generate_packet(self) -> bytes:
        return pack('BB', self.__control, self.__command)
