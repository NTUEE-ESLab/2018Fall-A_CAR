import socket
import pickle
import time

#server
class video_serial_server():
    def __init__(self, port):
        self.HOST = ''
        self.PORT = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.HOST, self.PORT))
        self.socket.listen(1)
        self.data = []

    def ready(self, conn):
        received = conn.recv(4096)
        if received.decode(encoding = 'UTF-8', errors = 'strict') ==\
            'ready':
            return True
        return False

    def run(self):
        conn, addr = self.socket.accept()
        while True:
            time.sleep (0.0001)
            try:
                count = 0
                while count < len(self.data):
                    if self.send(conn, self.data[count:count + 1]):
                       count += 1
                while True:
                    if self.send(conn, b''):
                        break
            except KeyboardInterrupt:
                self.socket.close()

    def send(self, conn, data):
        if self.ready(conn):
            encoded = pickle.dumps(data)
            conn.send(encoded)
            return True
        return False
