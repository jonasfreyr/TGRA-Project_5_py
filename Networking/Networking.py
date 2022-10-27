import multiprocessing
import json
import select
import socket
from Networking.Constants import *


class Networking:
    def __init__(self, game):
        self.id = None

        self.tcp_s = None
        self.udp_s = None

        self.game = game

        self.active = False

    def receive(self):
        if not self.active: return

        ready, _ , _ = select.select([self.udp_s], [], [], 0)

        if len(ready) == 0: return

        data, address = ready[0].recvfrom(262144)

        data = json.loads(data)

        print(data)

    def send(self, message: dict):
        if not self.active: return

        message['id'] = self.id
        self.udp_s.sendto(json.dumps(message).encode(), (HOST, PORT))

    def start(self):
        self.tcp_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Connecting to server...")
        self.tcp_s.connect((HOST, PORT))
        print("Connected to server!")

        print("Getting Id from server...")
        self.id = int(self.tcp_s.recv(1024).decode())  # Get Id from server
        print("Got Id:", self.id)

        self.udp_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_s.bind(('', PLAYER_PORT))

        self.active = True

    def stop(self):
        if self.tcp_s is not None:
            self.tcp_s.close()

        if self.udp_s is not None:
            self.udp_s.close()


