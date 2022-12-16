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

    # Request name
    while True:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        msg_length = int(msg_length)
        if msg_length:
            name = conn.recv(msg_length).decode(FORMAT)
            name = name.strip()
            sameName = False
            for cl in listClients:
                if cl[0] == name:
                    sameName = True
                    break
            if sameName:
                conn.send("Name has been taken".encode(FORMAT))
            else:
                conn.send("Ok".encode(FORMAT))
                break
    listClients.append((name,conn,addr))
    print(f"[NEW CONNECTION] {name} connected at {addr}. Total connection: {len(listClients)}")
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



    for cl in listClients:
        if cl[1] == conn:
            listClients.remove(cl)
            break
    print(f'[DISCONNECTION] {name} disconnected. Total connection: {len(listClients)}')
    conn.close()

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


print("[STARTING] server is starting...")
start()