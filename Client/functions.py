def is_valid_ip(ip):
    valid_format = True
    if ip.count('.') != 3:
        valid_format = False
    if valid_format:
        valid_format = ip.split('.')
        for i in range(4):
            if int(valid_format[i]) < 0 or int(valid_format[i]) > 255:
                valid_format = False
    return valid_format


def is_valid_port(port):
    if int(port) < 1024 or int(port) > 65353:
        return False
    return True
