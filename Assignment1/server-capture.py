import socket

def doprint():
    host1 = socket.gethostname()
    print(str(host1))

    host2 = socket.gethostbyname("localhost")
    print(str(host2))

    host3 = socket.gethostbyname("127.0.0.1")
    print(str(host3))

def doserver():
    host = socket.gethostbyname("127.0.0.1")
    port = 5505
    srv = socket.socket()
    srv.bind((host, port))
    srv.listen(19)
    clientconnect, address = srv.accept()
    dataFromClient = clientconnect.recv(1024)
    print(dataFromClient.decode())

if __name__ == "__main__":
    i = 0
    while i < 10:
       doserver()
       i += 1