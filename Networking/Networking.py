import multiprocessing
import json
import select
import socket

from Core.Vector import Vector
from Game.Gun import Rocket
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

        data = None
        try:
            while True: data, _ = self.udp_s.recvfrom(262144)
        except:
            pass

        if data is None: return

        data = json.loads(data)

        print(data)

        for rocket in data['rockets']:
            id = rocket['id']
            if id in self.game.network_rockets:
                r = self.game.network_rockets[id]

                new_pos = rocket['pos']
                new_rot = rocket['rot']

                r.pos.x = new_pos[0]
                r.pos.y = new_pos[1]
                r.pos.z = new_pos[2]

                r.rotation.x = new_rot[0]
                r.rotation.y = new_rot[1]
                r.rotation.z = new_rot[2]
            else:
                new_pos = rocket['pos']
                new_rot = rocket['rot']
                pos = Vector(new_pos[0], new_pos[1], new_pos[2])
                rot = Vector(new_rot[0], new_rot[1], new_rot[2])

                self.game.create_network_rocket(id, pos, rot)

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
        self.udp_s.setblocking(False)
        self.udp_s.bind(('', PLAYER_PORT))

        self.active = True

    def stop(self):
        if self.tcp_s is not None:
            self.tcp_s.close()

        if self.udp_s is not None:
            self.udp_s.close()


