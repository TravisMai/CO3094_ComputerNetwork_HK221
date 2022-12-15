import socket
import threading
import time

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname("127.0.0.1")
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

listClients = []

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    # Request name
    conn.send(str("Input your name (Your name won't be check for now because we don't have it yet. Please enter nicely): ").encode(FORMAT))
    msg_length = conn.recv(HEADER).decode(FORMAT)
    msg_length = int(msg_length)
    name = conn.recv(msg_length).decode(FORMAT)
    listClients.append((name,conn,addr))

    # Send back address to open peer server
    conn.send(str(addr).encode(FORMAT))

    connected = True
    while connected:

        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            if msg == DISCONNECT_MESSAGE:
                connected = False
            else:
                foundPeer = False
                peerFound = ()
                for cl in listClients:
                    if cl[0] == msg:
                        foundPeer = True
                        peerFound = cl
                        break
                if foundPeer:
                    conn.send("Peer found".encode(FORMAT))
                    conn.send(str(peerFound[2]).encode(FORMAT))
                else:
                    conn.send("Peer not found".encode(FORMAT))

            # print(f"[{addr}] {msg}")


    conn.close()
    print(f"{addr} disconnected. Erasing from list")


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


print("[STARTING] server is starting...")
start()