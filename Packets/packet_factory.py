from Builder.Builder import PacketBuilder
from Packets import packet_items as packets


class PacketFactory(object):
    def __init__(self, args: list):
        self.__args = args
        self.__builder = PacketBuilder("")

    def get_packet(self) -> any:
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
            packets_list = []

            self.__builder.set_type("APPEND_SEND")
            self.__builder.set_control(packets.CONTROL_INSTR)
            self.__builder.set_command(packets.APPEND_FILE)

            # Get slices of text
            text_data = self.__args[2]
            n = 512
            chunks = [text_data[i:i + n] for i in range(0, len(text_data), n)]
            self.__builder.set_packets(len(chunks))

            # Generate a packet for every slice
            for i in range(0, len(chunks)):
                self.__builder.set_packet_number(i + 1)
                text = self.__args[1] + '\0' + chunks[i]
                packet = self.__builder.generate_packet() + text.encode('utf-8')
                packets_list.append(packet)

            return packets_list
        # Generate a remove file packet
        elif self.__args[0] == "rm":
            self.__builder.set_control(packets.CONTROL_INSTR)
            self.__builder.set_command(packets.REMOVE_FILE)
            return self.__builder.generate_packet() + self.__args[1].encode('utf-8')
        # Generate a disconnect packet
        elif self.__args[0] == "leave":
            self.__builder.set_control(packets.CONTROL_CONN)
            self.__builder.set_command(packets.CONN_LEAVE)
            return self.__builder.generate_packet()
        # Generate a stop transmition packet
        elif self.__args[0] == "over":
            self.__builder.set_control(packets.CONTROL_CONN)
            self.__builder.set_command(packets.CONN_OVER)
            return self.__builder.generate_packet()
