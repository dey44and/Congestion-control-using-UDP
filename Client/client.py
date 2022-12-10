import socket
import sys
import select
import threading

running = False
s = None


def receive_fct(s: socket):
    global running
    contor = 0
    while running:
        # Apelam la functia sistem IO -select- pentru a verifca daca socket-ul are date in bufferul de receptie
        # Stabilim un timeout de 1 secunda
        r, _, _ = select.select([s], [], [], 1)
        if not r:
            contor = contor + 1
        else:
            data, address = s.recvfrom(1024)
            print("S-a receptionat ", str(data), " de la ", address)
            print("Contor= ", contor)


def start_socket(sport: str, dport: str, dip: str):
    # Creare socket UDP
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    s.bind(('0.0.0.0', int(sport)))

    global running
    running = True

    try:
        receive_thread = threading.Thread(target=receive_fct, args=[s])
        receive_thread.start()
    except:
        print("Eroare la pornirea thread‐ului")
        sys.exit()

    '''while True:
        try:
            data = input("Trimite: ")
            s.sendto(bytes(data, encoding="ascii"), (dip, int(dport)))
        except KeyboardInterrupt:
            running = False
            print("Waiting for the thread to close...")
            receive_thread.join()
            break
    '''

def send_data(data: str):
    s.sendto(data.encode(), )