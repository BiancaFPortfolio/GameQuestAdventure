import socket

server = "10.0.2.15"
port = 5555
RECV_BITS = 2048

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server
        self.port = port
        self.addr = (server, port)
        self.pos = self.connect()
        
    def getPos(self):
        return self.pos

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(RECV_BITS).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(RECV_BITS)
        except socket.error as e:
            print(e)

