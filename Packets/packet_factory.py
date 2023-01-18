from Builder.Builder import PacketBuilder
from Packets import packets


class PacketFactory(object):
    def __init__(self, args: list):
        self.__args = args
        self.__builder = PacketBuilder()

    def get_packet(self) -> bytes:
        # Generate a list_file packet
        if self.__args[0] == "ls":
            self.__builder.set_control(packets.CONTROL_INSTR)
            self.__builder.set_command(packets.LIST_FILES)
            return self.__builder.generate_packet()
        # Generate an add file packet
        elif self.__args[0] == "add":
            self.__builder.set_control(packets.CONTROL_INSTR)
            self.__builder.set_command(packets.CREATE_FILE)
            return self.__builder.generate_packet() + self.__args[1].encode('utf-8')
        # Generate an append file packet
        elif self.__args[0] == "app":
            self.__builder.set_control(packets.CONTROL_INSTR)
            self.__builder.set_command(packets.APPEND_FILE)
            text = self.__args[1] + '\0' + self.__args[2]
            return self.__builder.generate_packet() + text.encode('utf-8')
        # Generate a remove file packet
        elif self.__args[0] == "rm":
            self.__builder.set_control(packets.CONTROL_INSTR)
            self.__builder.set_command(packets.REMOVE_FILE)
            return self.__builder.generate_packet()
