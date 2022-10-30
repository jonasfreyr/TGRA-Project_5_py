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
from Game.Object import Teeth, RotatingCube, Object, NetworkPlayer
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

        pygame.init()
        pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF)

        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)

        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)

        self.shader = Shader3D()
        self.shader.use()

        self.model_matrix = ModelMatrix()

        # self.projection_view_matrix = ProjectionViewMatrix()
        # self.shader.set_projection_view_matrix(self.projection_view_matrix.get_matrix())

        self.player = Player(Vector(0, 0, 0), 1, 1, None, self)
        # self.player = FlyingPlayer(Vector(0, 0, 0), 1, 1)
        self.shader.set_projection_matrix(self.player.projection_matrix.get_matrix())

        self.player.draw(self.shader)

        self.clock = pygame.time.Clock()
        self.clock.tick()

        self.angle = 0

        self.keys = defaultdict(lambda: False)

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

        self.tex_id_cock = ojb_3D_loading.load_texture(TEXTURES_PATH + "/test.png")
        self.tex_id_vag = ojb_3D_loading.load_texture(TEXTURES_PATH + "/test2.png")
        self.tex_id_tits = ojb_3D_loading.load_texture(TEXTURES_PATH + "/test3.png")
        self.tex_id_aids = ojb_3D_loading.load_texture(TEXTURES_PATH + "/test4.png")
        self.tex_id_phobos = ojb_3D_loading.load_texture(TEXTURES_PATH + "/phobos.png")
        self.tex_id_earth = ojb_3D_loading.load_texture(TEXTURES_PATH + "/earth.jpg")
        self.tex_id_earth_spec = ojb_3D_loading.load_texture(TEXTURES_PATH + "/earth_spec.png")
        self.tex_id_skybox2 = ojb_3D_loading.load_texture(TEXTURES_PATH + "/sky.jpg")
        self.tex_id_skybox = ojb_3D_loading.load_texture(TEXTURES_PATH + "/space.png")

        self.fr_ticker = 0
        self.fr_sum = 0

        self.id = None
        self.exiting = False

        self.networking = Networking(self)

    def init_objects(self):
        self.sphere = Sphere(24, 48)

        self.lights = [Light(Vector(0, 80, 0), Color(2, 2, 2), Color(2, 2, 0.5), Color(0.5, 0.5, 0.25), 300.0),
                       Light(Vector(-0.3, 0, -0.3), Color(3, 3, 3), Color(1, 1, 1), Color(0.5, 0.5, 0.5), 1.0)]
        self.player_light = Light(Vector(0, 0, 0), Color(1, 1, 1), Color(1, 1, 1), Color(0.5, 0.5, 0.5), 5.0)
        self.fence_leftpost = Object(Vector(0, 0, 5), Vector(0, 0, 0), Vector(1, 1, 1), self.fence_leftpost_model,
                                     static=True)
        self.player_object = Object(Vector(5, 0, 5), Vector(0, 0, 0), Vector(0.5, 0.5, 0.5), self.player_model)
        # self.houses = Object(Vector(10, 0.3, 10), Vector(0, 0, 0), Vector(0.5, 0.5, 0.5), self.houses_model,static=True)

        self.map = Object(Vector(10, 0.3, 10), Vector(0, 0, 0), Vector(0.5, 0.5, 0.5), self.map_model,
                          static=True)
        self.skybox_model = Cube()

        # self.level = Level(self.grass_patch_model, self.ground_model, self.fence_leftpost_model, self.skybox_model,
        #                   self.tex_id_skybox)
        # self.boi = Object(Vector(5, 0, 5), Vector(0, 0, 0), Vector(1, 1, 1), self.player_model)

        self.rock = Object(Vector(0, 0, 5), Vector(0, 0, 0), Vector(10, 10, 10), self.rock_model)
        rpg = Gun(Vector(0.3, -0.1, -0.2), Vector(0, -90, 0), Vector(0.5, 0.5, 0.5), self.rpg_model)
        self.player.gun = rpg

        self.bullets = []
        self.new_rocket = None
        self.fired = False

        # self.networking.start()  # Comment this out, if testing locally
        self.network_rockets = {}
        self.network_players = {}

    def create_network_rocket(self, id, pos, rot):
        new_rocket = Rocket(pos, rot, Vector(1, 1, 1), self.rocket_model)
        self.network_rockets[id] = new_rocket

    def create_network_player(self, id, pos, rot):
        new_player = NetworkPlayer(pos, rot, Vector(5, 5, 5), self.rock_model)
        self.network_players[id] = new_player

    def shoot(self, look_pos, x_rot, y_rot):
        new_rocket = Rocket(self.player.top_pos, Vector(0, -x_rot - 90, -y_rot), Vector(1, 1, 1), self.rocket_model)
        new_rocket.set_vel(look_pos)

        self.bullets.append(new_rocket)

        self.fired = True

    def update(self):
        delta_time = self.clock.tick() / 1000.0

        self.fr_sum += delta_time
        self.fr_ticker += 1
        if self.fr_sum > 1.0:
            print(self.fr_ticker / self.fr_sum)
            self.fr_sum = 0
            self.fr_ticker = 0

        self.networking.receive()

        # self.cube.update(delta_time)
        # self.teeth.update(delta_time)
        self.player.update(delta_time, self.keys, [])
        self.player_light.pos = self.player.top_pos

        if not self.networking.active:
            temp = self.bullets.copy()
            for bullet in temp:
                if bullet.kill:
                    self.bullets.remove(bullet)
                else:
                    bullet.update(delta_time)

        else:
            message = {'pos': self.player.pos.to_array(),
                       'rot': (self.player.x_rotation, self.player.y_rotation),
                       'health': self.player.health}

            rockets = []
            for rocket in self.bullets:
                r = {'pos': rocket.pos.to_array(),
                     'rot': rocket.rotation.to_array(),
                     'vel': rocket.vel.to_array()}

                rockets.append(r)

            self.bullets.clear()

            message['rockets'] = rockets

            self.networking.send(message)

        # pygame.mouse.set_pos((WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.fired = False

    def draw_models(self):
        # self.player_object.draw(self.shader)
        # self.houses.draw(self.shader)
        # self.level.draw(self.shader)
        self.map.draw(self.shader)
        self.rock.draw(self.shader)

        if not self.networking.active:
            for bullet in self.bullets:
                bullet.draw(self.shader)

        else:
            temp = self.network_rockets.copy()
            for id, rocket in temp.items():
                if rocket.updated:
                    rocket.draw(self.shader)
                else:
                    del self.network_rockets[id]

            temp = self.network_players.copy()
            for id, player in temp.items():
                if player.updated:
                    player.draw(self.shader)
                else:
                    del self.network_players[id]

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.shader.set_calculate_lights(1.0)

        self.player.draw(self.shader)

        lights = [*self.lights, self.player_light]
        for i, light in enumerate(lights):
            light.draw(self.shader, i)

        self.shader.set_light_amount(len(lights))

        self.draw_models()

        pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Quitting!")
                self.exiting = True
            elif event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    print("Escaping!")
                    self.exiting = True
                self.keys[event.key] = True

            elif event.type == pygame.KEYUP:
                self.keys[event.key] = False

    def program_loop(self):
        self.init_objects()
        while not self.exiting:
            self.events()
            self.update()
            self.display()

        # OUT OF GAME LOOP
        pygame.quit()

        self.networking.stop()

    def start(self):
        self.program_loop()


if __name__ == "__main__":
    GraphicsProgram3D().start()
