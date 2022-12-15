import socket
import threading
import time

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "127.0.0.1"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

connectedPeerNo = 0
connectedPeer = []

def sendServer(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    # print(client.recv(2048).decode(FORMAT))


def handle_peer(conn, addr):
    global connectedPeerNo
    print(f"[NEW PEER] {addr} connected.")
    connectedPeerNo = connectedPeerNo +1
    print(f'Connected to {connectedPeerNo} peer')
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            # print(f"[{addr}] {msg}")
    conn.close()

def startUsing():
    global connectedPeerNo
    time.sleep(1)
    disconnected = False
    print("Enter (connect)<name> to find peer (no space pls)")
    print("Enter (<name>)<message> to send message to peer")
    print("Enter (disconnect) to exit")
    print(f'Connected to {connectedPeerNo} peer')
    while not disconnected:
        msg = input()
        if msg.startswith("(connect)"):
            findWho = msg[9:]
            sendServer(findWho)
            sMess = client.recv(2048).decode(FORMAT)
            print(sMess)
            if sMess == "Peer found":
                connectAddr = client.recv(2048).decode(FORMAT)
                haddr, paddr = connectAddr[1:-1].split(", ")
                cAddress = (haddr[1:-1], int(paddr))
                print(f'Peer Address {cAddress}')
                newPeer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                newPeer.connect(cAddress)
                connectedPeer.append((findWho,newPeer,cAddress))
                connectedPeerNo = connectedPeerNo + 1
                print(f'Connected to {connectedPeerNo} peer')
        elif msg.startswith("(disconnect)"):
            disconnected = True
            sendServer(DISCONNECT_MESSAGE)
            print("Will be broadcast to every connected friend")
        elif msg.startswith("(") and msg.__contains__(")"): # Chat to peer
            if connectedPeerNo <=0:
                print("You don't have any connected peer")
            else:
                pass
        else:
            print("Invalid command")
    print("You are disconnected! Cannot stop the process now pls help")


def startListen(hAddr, pAddr):
    pServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    peeraddr = (hAddr, pAddr)
    pServer.bind(peeraddr)
    pServer.listen()
    print(f"[LISTENING] You are is listening on {peeraddr}")
    while True:
        conn, addr = pServer.accept()
        thread = threading.Thread(target=handle_peer, args=(conn, addr))
        thread.start()
        print(f"[A FRIEND HAS CONNECTED] {addr}")


def setUp():
    print(client.recv(2048).decode(FORMAT))

    # Input name
    name = input()
    sendServer(name)

    # Receive address
    inaddr = client.recv(2048).decode(FORMAT)
    haddr, paddr = inaddr[1:-1].split(", ")
    haddr = haddr[1:-1]
    paddr = int(paddr)
    oAddr = (haddr,paddr)
    openSocket = threading.Thread(target=startListen, args=oAddr)
    openSocket.start()
    startUse = threading.Thread(target=startUsing())
    startUse.start()

print("[Starting] Client is starting...")
setUp()
