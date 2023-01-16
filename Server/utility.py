def get_arguments(argvs):
    global sport, dport, dip
    for arg in argvs:
        if arg.startswith("--sport"):
            temp, sport = arg.split("=")
        elif arg.startswith("--dport"):
            temp, dport = arg.split("=")
        elif arg.startswith("--dip"):
            temp, dip = arg.split("=")
    return sport, dport, dip
