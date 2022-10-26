import multiprocessing
import json
import socket
from Networking.Constants import *


class Networking:
    def __init__(self, game):
        self.id = None

        self.tcp_s = None
        self.udp_s = None

        self.game = game

        self.active = False

        self.tcp_process = None
        self.udp_process = None

    @staticmethod
    def listeningUDP(id):
        from Networking.Constants import PLAYER_PORT
        udp_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_s.bind(('', PLAYER_PORT))
        message = {
            'id': id.value
        }
        udp_s.sendto(json.dumps(message).encode(), (HOST, PORT))
        while True:
            data, address = udp_s.recvfrom(262144)

            print(data)

            message = {
                'id': id.value
            }

            udp_s.sendto(json.dumps(message).encode(), (HOST, PORT))

    @staticmethod
    def listeningTCP(id):
        tcp_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_s.connect((HOST, PORT))

        id.value = int(tcp_s.recv(1024).decode())
        while True:
            data = tcp_s.recv(204888)

            data = json.load(data)

            if data['command'] == "dc":
                # self.game.exiting = True
                pass

            elif data['command'] == 'reset':
                pass
                # self.player.pos = data['args']['pos']
                # self.player.health = data['args']['health']

    def start(self):
        self.id = multiprocessing.Value('i', -1)

        self.tcp_process = multiprocessing.Process(target=self.listeningTCP, args=(self.id, ))
        self.tcp_process.start()

        while self.id.value == -1: pass  # Wait for the server to assign player Id

        self.udp_process = multiprocessing.Process(target=self.listeningUDP, args=(self.id, ))
        self.udp_process.start()

        self.active = True

    def stop(self):
        if self.tcp_process:
            self.tcp_process.join()

        if self.udp_process:
            self.udp_process.join()
