import socket
import threading

host = socket.gethostbyname('127.0.0.1')
port = 5505

client = socket.socket()
client.connect((host,port))

def peerConnect():
    sentence = input("Input a peer's name: ")
    client.send(sentence.encode())
    result = client.recv(1024).decode()
    client.connect((result[0], result[1]))
    sendMessageThread = threading.Thread(sendMessage, ())
    sendMessageThread.start()

def sendMessage():
    while True:
        message = input("input your message: ")
        client.send(message.encode()) 
    
#print(client)

if __name__ == "__main__":
    x =  threading.Thread(target = peerConnect, args=())
    x.start()
    x.join()