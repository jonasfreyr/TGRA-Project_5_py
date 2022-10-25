import _thread
import json
import socket
from dataclasses import dataclass

from Core.Constants import *

connsUDP = {}
connsTCP = {}
TCPaddress = {}

stats = {}
bullets = {}
players = {}


@dataclass
class Player:
    health: int
    dead: bool


def remove_client(id):
        if id in connsUDP:
            del connsUDP[id]
        if id in connsTCP:
            del connsTCP[id]
        if id in players:
            del players[id]
        if id in bullets:
            del bullets[id]
        if id in TCPaddress:
            del TCPaddress[id]
        if id in stats:
            del stats[id]


def new_client(conn, addr, id):
    conn.sendall(str(id).encode())

    while True:
        try:
            data = conn.recv(1024).decode()

        except:
            if id in connsUDP:
                print("Connection ended with: \n id: " + str(id) + "\n TCP address: " + str(
                    addr) + "\n UDP address: " + str(
                    connsUDP[id]))
            else:
                print("Connection ended with: \n id: " + str(id) + "\n TCP address: " + str(
                    addr))

            remove_client(id)
            break

        if data == "respawn":
            player = players[id]
            player.health = PLAYER_HEALTH
            player.dead = False

            message = {
                'command': 'reset',
                'args': {'pos': (0, 0, 0),
                         'health': PLAYER_HEALTH}
            }

            conn.sendall(json.dumps(message).encode())

        elif data == "":
            if id in connsUDP:
                print("Connection ended with: \n id: " + str(id) + "\n TCP address: " + str(
                    addr) + "\n UDP address: " + str(
                    connsUDP[id]))
            else:
                print("Connection ended with: \n id: " + str(id) + "\n TCP address: " + str(
                    addr))

            remove_client(id)
            break


def listening_TCP():
    global id
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(3)

        # _thread.start_new_thread(start_main, ())
        while True:
            conn, addr = s.accept()

            connsTCP[id] = conn
            TCPaddress[id] = addr

            bullets[id] = []

            stats[id] = {
                "kills": 0,
                "deaths": 0
            }

            print("Connection Started with: " + str(addr))

            # ui.update_user(id)
            _thread.start_new_thread(new_client, (conn, addr, id))

            id += 1


def listening_UDP(s):
    print("UDP started!")
    while True:
        try:
            data, address = s.recvfrom(262144)

            print(data)
            continue

            data = json.loads(data)
            connsUDP[data["id"]] = address
            players[data["id"]] = data["player"]
            for bullet in data["bullets"]:
                # print(bullet)
                bullets[data["id"]].append(bullet)

        except ConnectionResetError:
            pass


def run_game(s):
    print("Game Started!")
    while True:
        print(connsUDP)
        for id in connsUDP:
            s.sendto(str("Yo!").encode(), connsUDP[id])


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((HOST, PORT))
_thread.start_new_thread(listening_UDP, (s, ))
# _thread.start_new_thread(listening_TCP, ())
run_game(s)
