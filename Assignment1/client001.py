import socket
import sys
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

name = ""
connectedPeerNo = 0
connectedPeer = []

using = True

def sendServer(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    # print(client.recv(2048).decode(FORMAT))

def sendPeer(conn, msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    conn.send(send_length)
    conn.send(message)

def handle_peer(conn, addr):
    global connectedPeerNo

    # Hear for name
    name_length = conn.recv(HEADER).decode(FORMAT)
    name_msg = ""
    if name_length:
        name_length = int(name_length)
        name_msg = conn.recv(name_length).decode(FORMAT)

    already = False

    for cl in connectedPeer:
        if cl[0] == name_msg:
            already = True
            break

    if not already:
        findWho = name_msg
        sendServer(findWho)
        sMess = client.recv(2048).decode(FORMAT)
        connectAddr = client.recv(2048).decode(FORMAT)
        haddr, paddr = connectAddr[1:-1].split(", ")
        cAddress = (haddr[1:-1], int(paddr))
        newPeer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        newPeer.connect(cAddress)
        global name
        sendPeer(newPeer, name)
        connectedPeer.append((name_msg,newPeer,cAddress))
        connectedPeerNo = connectedPeerNo +1
        print(f"Connected with {name_msg}. Total connection: {connectedPeerNo}")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            else:
                print(f'[{name_msg}]->{msg}')

    for cl in connectedPeer:
        if cl[0] == name_msg:
            cl[1].close()
            connectedPeer.remove(cl)
            connectedPeerNo = connectedPeerNo - 1
            break

    print(f'{name_msg} has disconnected. Total connection: {connectedPeerNo}')

    conn.close()

def startUsing():
    global connectedPeerNo
    time.sleep(1)
    disconnected = False

    # print(f'Connected to {connectedPeerNo} peer')
    print(f'Enter [help] for more info')
    while not disconnected:
        msg = input()
        socketSendingPeer = []
        if msg.startswith("[connect]"):
            findWho = msg[9:].strip()
            global name
            if findWho == name:
                print("It's you")
            else:
                already = False
                for cl in connectedPeer:
                    if cl[0] == findWho:
                        already = True
                        break
                if already:
                    print(f'You are already connected with {findWho}')
                else:
                    sendServer(findWho)
                    sMess = client.recv(2048).decode(FORMAT)
                    if sMess == "Peer found":
                        connectAddr = client.recv(2048).decode(FORMAT)
                        haddr, paddr = connectAddr[1:-1].split(", ")
                        cAddress = (haddr[1:-1], int(paddr))
                        newPeer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        newPeer.connect(cAddress)
                        sendPeer(newPeer, name)
                        socketSendingPeer.append(newPeer)
                    else:
                        print(sMess)
        elif msg.startswith("[disconnect]"):
            disconnected = True
            sendServer(DISCONNECT_MESSAGE)
            print("Thank you for using")
            for cl in connectedPeer:
                sendPeer(cl[1],DISCONNECT_MESSAGE)
                cl[1].close()
        elif msg.startswith("[help]"):
            print("Enter [connect]<name> to find peer")
            print("Enter (<name>)<message> to send message to peer")
            print("Enter [disconnect] to exit")
        elif msg.startswith("(") and msg.__contains__(")"): # Chat to peer
            if connectedPeerNo <=0:
                print("You don't have any connected peer")
            else:
                nameStart = msg.find(")")
                pname = msg[1:(nameStart)]
                pfound = False
                pafound = ""
                for cl in connectedPeer:
                    if cl[0] == pname:
                        pfound = True
                        pafound = cl
                        break
                if pfound:
                    sendMess = msg[nameStart+1:].strip()
                    sendPeer(pafound[1],sendMess)
                else:
                    print(f'Not found connected peer name {pname}')
        else:
            print("Invalid command")

    for sk in socketSendingPeer:
        sk.close()

    global using
    using = False

    print("You are disconnected! Cannot stop the server process now pls help")


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


def setUp():

    # Input name
    while True:
        global name
        name = input("Input your name: ")
        sendServer(name)
        sMess = client.recv(2048).decode(FORMAT)
        if sMess != "Name has been taken":
            break
        else:
            print(sMess)

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