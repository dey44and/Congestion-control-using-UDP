import os

from Builder.Builder import PacketBuilder
from Packets import packets

path = ".\\Root\\"


def list_files_packet(data: bytes) -> bytes:
    result = "Files:\n"
    for subdir, dirs, files in os.walk('./Root'):
        for file in files:
            result += "-> " + file + "\n"

    # Generate a list file packet
    builder: PacketBuilder = PacketBuilder()
    builder.set_control(packets.CONTROL_RESPONSE)
    builder.set_command(packets.LIST_FILES)

    # Get packet for client
    return builder.generate_packet() + result.encode('utf-8')


def create_file_packet(data: bytes) -> bytes:
    # Generate a create file packet
    builder: PacketBuilder = PacketBuilder()
    builder.set_control(packets.CONTROL_RESPONSE)
    builder.set_command(packets.CREATE_FILE)
    packet = builder.generate_packet()

    # Try to create file
    try:
        file_name = data[2:].decode('utf-8')
        file = open(path + file_name, 'x')
        file.close()
        packet += "INFO: File created!".encode('utf-8')
    except:
        packet += "WARNING: The file already exists.".encode('utf-8')
    return packet


def append_to_file_packet(data: bytes) -> bytes:
    # Generate an append to file packet
    builder: PacketBuilder = PacketBuilder()
    builder.set_control(packets.CONTROL_RESPONSE)
    builder.set_command(packets.APPEND_FILE)
    packet = builder.generate_packet()

    # Try to append to file
    try:
        items = data[2:].decode('utf-8').split('\0')
        file = open(path + items[0], 'a')
        file.write(items[1])
        file.close()
        packet += "INFO: Text appended to file.".encode('utf-8')
    except:
        packet += "ERROR: Text cannot be writed!".encode('utf-8')
    return packet


def remove_file_packet(data: bytes) -> bytes:
    # Generate a remove file packet
    builder: PacketBuilder = PacketBuilder()
    builder.set_control(packets.CONTROL_RESPONSE)
    builder.set_command(packets.REMOVE_FILE)
    packet = builder.generate_packet()

    # Try to remove the file
    try:
        file_name = data[2:].decode('utf-8')
        current_path = os.getcwd()
        os.remove(current_path + path[1:] + file_name)
        packet += "INFO: The file was removed.".encode('utf-8')
    except:
        packet += "WARNING: The file was already removed.".encode('utf-8')
    return packet
