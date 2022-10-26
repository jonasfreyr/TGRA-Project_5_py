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

        self.event = multiprocessing.Event()

    @staticmethod
    def listeningUDP(id, event):
        from Networking.Constants import PLAYER_PORT
        udp_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_s.bind(('', PLAYER_PORT))
        message = {
            'id': id.value
        }
        udp_s.sendto(json.dumps(message).encode(), (HOST, PORT))
        while not event.is_set():
            data, address = udp_s.recvfrom(262144)

            message = {
                'id': id.value
            }

            udp_s.sendto(json.dumps(message).encode(), (HOST, PORT))

        udp_s.close()

    @staticmethod
    def listeningTCP(id, event):
        tcp_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_s.connect((HOST, PORT))
        id.value = int(tcp_s.recv(1024).decode())
        tcp_s.setblocking(False)
        tcp_s.settimeout(0.5)
        while not event.is_set():
            try:
                data = tcp_s.recv(204888)
            except TimeoutError:
                continue

            print(data)

            data = json.load(data)

            if data['command'] == "dc":
                # self.game.exiting = True
                pass

            elif data['command'] == 'reset':
                pass
                # self.player.pos = data['args']['pos']
                # self.player.health = data['args']['health']

        tcp_s.close()

    def send(self, message: dict):
        if not self.active: return

        message['id'] = self.id

        ## Todo Share message to UDP socket


    def start(self):
        self.id = multiprocessing.Value('i', -1)
        self.message = multiprocessing.Array

        self.tcp_process = multiprocessing.Process(target=self.listeningTCP, args=(self.id, self.event))
        self.tcp_process.start()

        while self.id.value == -1: pass  # Wait for the server to assign player Id

        self.udp_process = multiprocessing.Process(target=self.listeningUDP, args=(self.id, self.event))
        self.udp_process.start()

        self.active = True

    def stop(self):
        self.event.set()

        if self.tcp_process:
            self.tcp_process.join()

        if self.udp_process:
            self.udp_process.join()
