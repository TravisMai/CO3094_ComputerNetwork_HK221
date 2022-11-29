import socket


def doclient():
    host = socket.gethostbyname("127.0.0.1")
    port = 5505

    client = socket.socket()
    client.connect((host, port))


if __name__ == "__main__":
    doclient() 