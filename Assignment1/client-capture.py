import socket


def doclient():
    host = socket.gethostbyname("127.0.0.1")
    port = 5505
    client = socket.socket()
    client.connect((host, port))
    client.send(data.encode())

if __name__ == "__main__":
    i = 0
    while i < 10:
        data = input("input: ")
        doclient() 
        i += 1