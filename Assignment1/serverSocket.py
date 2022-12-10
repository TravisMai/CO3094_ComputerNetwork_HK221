import socket
import threading
#from flask import Flask
#app = Flask(__name__)

host = socket.gethostbyname('127.0.0.1')
port = 5505

server = socket.socket()
server.bind((host, port))

listClients = []

def clientListen():
    server.listen(10)
    conn, addr = server.accept()
    y = threading.Thread(target = handleMessage, args = (conn, addr))
    y.start()
    
def handleMessage(conn, addr):
    peerName = conn.recv(2048).decode()
    for client in listClients:
        if (peerName == client[0]):
            conn.send(str(addr).encode())

def addClients(username, conn, addr):
    listClients.append((username, conn, addr))
    

if __name__ == "__main__":
    clientListen()

        
