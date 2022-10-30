import _thread
import json
import socket
from dataclasses import dataclass

import pygame

from Core.Constants import *
from Core.Vector import Vector
from Game.Gun import Rocket
from Game.Object import Collider
from Networking.Constants import *

@dataclass
class Player:
    health: int
    dead: bool

import _thread
import json

# from OpenGL.GL import *
# from OpenGL.GLU import *

import pygame
from pygame.locals import *

from collections import defaultdict

from Core.Light import Light
from Game.Gun import Gun, Rocket
from Game.Level import Level
from Game.Object import Teeth, RotatingCube, Object, NetworkPlayer, ObjectCube
from Game.Player import FlyingPlayer, Player
from Networking.Networking import Networking
from OpenGLCore.Shaders import *
from Core.Matrices import *
from OpenGLCore import ojb_3D_loading
from Core.Constants import *
from Core.Color import Color
import socket


class GraphicsProgram3D:
    def __init__(self):
        self.model_matrix = ModelMatrix()

        # self.projection_view_matrix = ProjectionViewMatrix()
        # self.shader.set_projection_view_matrix(self.projection_view_matrix.get_matrix())

        pygame.init()
        pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF)


        self.clock = pygame.time.Clock()
        self.clock.tick(120)

        # self.teeth_object_model = ojb_3D_loading.load_obj_file(MODELS_PATH, "mouth.obj")
        self.rocket_model = ojb_3D_loading.load_obj_file(MODELS_PATH, "rocket.obj")
        self.grass_object_model = ojb_3D_loading.load_obj_file(MODELS_PATH, "grass_with_texture.obj")
        self.grass_patch_model = ojb_3D_loading.load_obj_file(MODELS_PATH, "grass_patch.obj")
        self.rock_model = ojb_3D_loading.load_obj_file(MODELS_PATH, "rock.obj")
        self.ground_model = ojb_3D_loading.load_obj_file(MODELS_PATH, "grass-plain.obj")
        self.rpg_model = ojb_3D_loading.load_obj_file(MODELS_PATH, "launcher.obj")
        self.fence_leftpost_model = ojb_3D_loading.load_obj_file(MODELS_PATH, "fence-leftpost.obj")
        self.player_model = ojb_3D_loading.load_obj_file(MODELS_PATH, "playermodel.obj")
        self.houses_model = ojb_3D_loading.load_obj_file(MODELS_PATH, "houses-test.obj")
        self.map_model = ojb_3D_loading.load_obj_file(MODELS_PATH, "whole-map.obj")

        self.tex_id_skybox2 = ojb_3D_loading.load_texture(TEXTURES_PATH + "/sky.jpg")
        self.tex_id_skybox = ojb_3D_loading.load_texture(TEXTURES_PATH + "/space.png")

        self.fr_ticker = 0
        self.fr_sum = 0

        self.exiting = False

        self.connsUDP = {}
        self.connsTCP = {}
        self.TCPaddress = {}

        self.stats = {}
        self.players = {}
        self.rockets = {}

        self.id = 0
        self.rocket_id = 0

    def remove_client(self, id):
        if id in self.connsUDP:
            del self.connsUDP[id]
        if id in self.connsTCP:
            del self.connsTCP[id]
        if id in self.players:
            del self.players[id]
        if id in self.TCPaddress:
            del self.TCPaddress[id]
        if id in self.stats:
            del self.stats[id]

    def init_objects(self):
        self.fence_leftpost = Object(Vector(0, 0, 5), Vector(0, 0, 0), Vector(1, 1, 1), self.fence_leftpost_model,
                                     static=True)
        self.player_object = Object(Vector(-5, 0, -5), Vector(0, 0, 0), Vector(0.5, 0.5, 0.5), self.player_model)
        # self.houses = Object(Vector(10, 0.3, 10), Vector(0, 0, 0), Vector(0.5, 0.5, 0.5), self.houses_model,static=True)

        self.map = Object(Vector(10, 0.3, 10), Vector(0, 0, 0), Vector(0.5, 0.5, 0.5), self.map_model,
                          static=True)

        self.boi = Object(Vector(5, 0, 5), Vector(0, 0, 0), Vector(1, 1, 1), self.player_model)

        self.rock = Object(Vector(0, 0, 5), Vector(0, 0, 0), Vector(10, 10, 10), self.rock_model)

        self.bullets = []
        self.new_rocket = None
        self.fired = False

    def new_client(self, conn, addr, id):
        conn.sendall(str(id).encode())

        while True:
            try:
                data = conn.recv(1024).decode()

            except:
                if id in self.connsUDP:
                    print("Connection ended with: \n id: " + str(id) + "\n TCP address: " + str(
                        addr) + "\n UDP address: " + str(
                        self.connsUDP[id]))
                else:
                    print("Connection ended with: \n id: " + str(id) + "\n TCP address: " + str(
                        addr))

                self.remove_client(id)
                break

            if data == "respawn":
                player = self.players[id]
                player.health = PLAYER_HEALTH
                player.dead = False

                message = {
                    'command': 'reset',
                    'args': {'pos': (0, 0, 0),
                             'health': PLAYER_HEALTH}
                }

                conn.sendall(json.dumps(message).encode())

            elif data == "":
                if id in self.connsUDP:
                    print("Connection ended with: \n id: " + str(id) + "\n TCP address: " + str(
                        addr) + "\n UDP address: " + str(
                        self.connsUDP[id]))
                else:
                    print("Connection ended with: \n id: " + str(id) + "\n TCP address: " + str(
                        addr))

                self.remove_client(id)
                break

    def listening_TCP(self):
        print("TCP started!")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen(3)

            # _thread.start_new_thread(start_main, ())
            while True:
                conn, addr = s.accept()

                self.connsTCP[self.id] = conn
                self.TCPaddress[self.id] = addr

                self.stats[self.id] = {
                    "kills": 0,
                    "deaths": 0
                }

                print("Connection Started with: " + str(addr))

                # ui.update_user(id)
                _thread.start_new_thread(self.new_client, (conn, addr, self.id))

                self.id += 1

    def listening_UDP(self, s):
        print("UDP started!")
        while True:
            try:
                data, address = s.recvfrom(262144)

                data = json.loads(data)
                self.connsUDP[data["id"]] = address

                self.players[data['id']] = {'pos': data['pos'], 'rot': data['rot'], 'health': data['health']}

                for rocket in data['rockets']:
                    pos = Vector(rocket['pos'][0], rocket['pos'][1], rocket['pos'][2])
                    rot = Vector(rocket['rot'][0], rocket['rot'][1], rocket['rot'][2])
                    vel = Vector(rocket['vel'][0], rocket['vel'][1], rocket['vel'][2])

                    r = Rocket(pos, rot, Vector(1, 1, 1), None)
                    r.set_vel(vel)
                    self.rockets[self.rocket_id] = r

                    self.rocket_id += 1

                    if self.rocket_id >= 5000:
                        self.rocket_id = 0

            except ConnectionResetError:
                pass

    def update(self, s):
        delta_time = self.clock.tick(120) / 1000.0

        temp = self.rockets.copy()
        for id, rocket in temp.items():
            if rocket.kill:
                del self.rockets[id]
            else:
                rocket.update(delta_time)

        # {'pos': (x, y, z), 'rot': (x, y), 'health': 100}
        for id, player in self.players.items():
            pass

        # print(connsUDP)
        message = {
            "players": {},
            "rockets": {}
        }

        temp_players = self.players.copy()
        for player_id in temp_players:
            if temp_players[player_id]['health'] > 0:
                message['players'][player_id] = temp_players[player_id]

        temp_rockets = self.rockets.copy()
        for id, rocket in temp_rockets.items():
            rock = {'pos': rocket.pos.to_array(), 'rot': rocket.rotation.to_array()}
            message['rockets'][id] = rock

        temp = self.connsUDP.copy()

        for id in temp:
            message_to_send = dict(message)
            players_to_send = dict(message_to_send['players'])
            if id in players_to_send:
                del players_to_send[id]

            try:
                message_to_send['players'] = players_to_send
                s.sendto(json.dumps(message_to_send).encode(), temp[id])
            except:
                continue

    def program_loop(self):
        print("Game Started!")
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((HOST, PORT))
        _thread.start_new_thread(self.listening_TCP, ())
        _thread.start_new_thread(self.listening_UDP, (s,))
        self.init_objects()
        while not self.exiting:
            self.update(s)

        # OUT OF GAME LOOP
        pygame.quit()

    def start(self):
        self.program_loop()


'''
def run_game(s):
    print("Game Started!")
    clock = pygame.time.Clock()
    clock.tick(120)

    while True:
        delta_time = clock.tick(120) / 1000.0

        temp = rockets.copy()
        for id, rocket in temp.items():
            if rocket.kill: del rockets[id]
            else: rocket.update(delta_time)

        # {'pos': (x, y, z), 'rot': (x, y), 'health': 100}
        for id, player in players.items():
            pass

        # print(connsUDP)
        message = {
            "players": {},
            "rockets": {}
        }

        temp_players = players.copy()
        for player_id in temp_players:
            if temp_players[player_id]['health'] > 0:
                message['players'][player_id] = temp_players[player_id]

        temp_rockets = rockets.copy()
        for id, rocket in temp_rockets.items():
            rock = {'pos': rocket.pos.to_array(), 'rot': rocket.rotation.to_array()}
            message['rockets'][id] = rock

        temp = connsUDP.copy()

        for id in temp:
            message_to_send = dict(message)
            players_to_send = dict(message_to_send['players'])
            if id in players_to_send:
                del players_to_send[id]

            try:
                message_to_send['players'] = players_to_send
                s.sendto(json.dumps(message_to_send).encode(), temp[id])
            except:
                continue
'''
g = GraphicsProgram3D()
g.start()
# run_game(s)
