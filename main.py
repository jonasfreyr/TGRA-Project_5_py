# from OpenGL.GL import *
# from OpenGL.GLU import *

from collections import defaultdict

import pygame
from pygame.locals import *

from Core.Color import Color
from Core.Light import Light
from Core.Matrices import *
from Game.Gun import Gun, Rocket
from Game.Object import Object, NetworkPlayer, Collider
from Game.Player import FlyingPlayer, Player
from Networking.Constants import USE_NETWORKING
from Networking.Networking import Networking
from OpenGLCore import ojb_3D_loading
from OpenGLCore.Shaders import *


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

        # self.projection_view_matrix = ProjectionViewMatrix()
        # self.shader.set_projection_view_matrix(self.projection_view_matrix.get_matrix())

        self.non_flying_player = Player(Vector(0, 0, 0), 1, .5, None, self)
        self.flying_player = FlyingPlayer(Vector(0, 0, 0), 1, 1)

        self.player = self.non_flying_player

        self.shader.set_projection_matrix(self.player.projection_matrix.get_matrix())

        self.player.draw(self.shader)

        self.clock = pygame.time.Clock()
        self.clock.tick()

        self.keys = defaultdict(lambda: False)

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

        self.id = None
        self.exiting = False

        self.networking = Networking(self)

    def init_objects(self):
        self.sphere = Sphere(24, 48)

        self.lights = [Light(Vector(-0.3, 0, -0.3), Color(3, 3, 3), Color(1, 1, 1), Color(0.5, 0.5, 0.5), 1.0),
                       Light(Vector(0, 80, 0), Color(2, 2, 2), Color(2, 2, 0.5), Color(0.5, 0.5, 0.25), 300.0)]#

        self.player_light = Light(Vector(0, 0, 0), Color(1, 1, 1), Color(1, 1, 1), Color(0.5, 0.5, 0.5), 5.0)
        self.fence_leftpost = Object(Vector(0, 0, 5), Vector(0, 0, 0), Vector(1, 1, 1), self.fence_leftpost_model,
                                     static=True)
        self.player_object = Object(Vector(-5, 0, -5), Vector(0, 0, 0), Vector(0.5, 0.5, 0.5), self.player_model)
        # self.houses = Object(Vector(10, 0.3, 10), Vector(0, 0, 0), Vector(0.5, 0.5, 0.5), self.houses_model,static=True)

        self.map = Object(Vector(0, 0, 0), Vector(0, 0, 0), Vector(0.5, 0.5, 0.5), self.map_model,
                          static=True)
        self.skybox_model = Cube()


        # self.level = Level(self.grass_patch_model, self.ground_model, self.fence_leftpost_model, self.skybox_model,
        #                   self.tex_id_skybox)

        self.rock = Object(Vector(0, 0, 5), Vector(0, 0, 0), Vector(10, 10, 10), self.rock_model)
        rpg = Gun(Vector(0.3, -0.1, -0.2), Vector(0, -90, 0), Vector(0.5, 0.5, 0.5), self.rpg_model)
        self.player.gun = rpg

        self.bullets = []
        self.new_rocket = None
        self.fired = False

        self.current = Collider(Vector(0, 0, 0), Vector(1, 1, 1))

        self.colliders = [
                        # Fences
                        Collider(Vector(-25, 0, 0), Vector(0.5, 5, 55)),
                        Collider(Vector(25, 0, 0), Vector(0.5, 5, 55)),
                        Collider(Vector(0, 0, -23.8), Vector(55, 5, 0.5)),
                        Collider(Vector(0, 2, 25.2), Vector(55, 5, 0.5)),

                        # House
                        Collider(Vector(-0.9890000000000153, 0.9039999999999999, -5.564),
                                Vector(6.597999999999904, 1.98999999999999, 1.677000000000001)),
                        Collider(Vector(0.09999999999999999, 0.09200000000000007, 0),
                                Vector(9.050999999999839, 0.15099999999999922, 8.937999999999864))
                        ]

        if USE_NETWORKING:
            self.networking.start()  # Comment this out, if testing locally

        self.network_rockets = {}
        self.network_players = {}

        self.testing_player = NetworkPlayer(Vector(-10, 0, -10), Vector(0, 0, 0),
                                                 Vector(.5, .5, .5), self.player_model)

    def create_network_rocket(self, id, pos, rot):
        new_rocket = Rocket(pos, rot, Vector(1, 1, 1), self.rocket_model)
        self.network_rockets[id] = new_rocket

    def create_network_player(self, id, pos, rot):
        new_player = NetworkPlayer(pos, rot, Vector(NETWORK_PLAYER_MODEL_WIDTH, NETWORK_PLAYER_MODEL_HEIGHT, NETWORK_PLAYER_MODE_DEPTH), self.player_model)
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

        # self.testing_player.pos.x += 1 * delta_time
        # self.testing_player.update(delta_time)

        if not self.keys[K_LSHIFT]:
            if self.keys[K_LEFT] and not self.keys[K_LCTRL]:
                self.current.pos.x -= 1 * delta_time
            elif self.keys[K_RIGHT] and not self.keys[K_LCTRL]:
                self.current.pos.x += 1 * delta_time

            if self.keys[K_LEFT] and self.keys[K_LCTRL]:
                self.current.pos.z -= 1 * delta_time
            elif self.keys[K_RIGHT] and self.keys[K_LCTRL]:
                self.current.pos.z += 1 * delta_time

            if self.keys[K_DOWN]:
                self.current.pos.y -= 1 * delta_time
            elif self.keys[K_UP]:
                self.current.pos.y += 1 * delta_time

        else:
            if self.keys[K_LEFT] and not self.keys[K_LCTRL]:
                self.current.size.x -= 1 * delta_time
            elif self.keys[K_RIGHT] and not self.keys[K_LCTRL]:
                self.current.size.x += 1 * delta_time

            if self.keys[K_LEFT] and self.keys[K_LCTRL]:
                self.current.size.z -= 1 * delta_time
            elif self.keys[K_RIGHT] and self.keys[K_LCTRL]:
                self.current.size.z += 1 * delta_time

            if self.keys[K_DOWN]:
                self.current.size.y -= 1 * delta_time
            elif self.keys[K_UP]:
                self.current.size.y += 1 * delta_time


        # self.cube.update(delta_time)
        # self.teeth.update(delta_time)
        colliders = [*self.colliders, self.current]

        if self.networking.active:
            for _, player in self.network_players.items():
                colliders.append(player.collider)

        self.player.update(delta_time, self.keys, colliders)
        self.player_light.pos = self.player.top_pos

        if not self.networking.active:
            temp = self.bullets.copy()
            for bullet in temp:
                if bullet.kill:
                    self.bullets.remove(bullet)
                else:
                    bullet.update(delta_time, [*self.colliders, self.current])

        else:
            for id, player in self.network_players.items():
                player.update(delta_time)

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
        # self.testing_player.draw(self.shader)

        if DRAW_COLLIDERS:
            for collider in self.colliders:
                collider.draw(self.shader)
            self.current.draw(self.shader)

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
                    player.collider.draw(self.shader)
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

                if event.key == K_v:
                    if self.player == self.flying_player:
                        self.non_flying_player.pos = self.player.pos
                        self.non_flying_player.x_rotation = self.player.x_rotation
                        self.non_flying_player.y_rotation = self.player.y_rotation
                        self.player = self.non_flying_player
                    else:
                        self.flying_player.pos = self.player.pos
                        self.flying_player.x_rotation = self.player.x_rotation
                        self.flying_player.y_rotation = self.player.y_rotation
                        self.player = self.flying_player

                elif event.key == K_RETURN:
                    self.colliders.append(self.current.copy())

                elif event.key == K_BACKSPACE:
                    self.current = self.colliders.pop(-1)

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

        for collider in self.colliders:
            print(str(collider) + ",")

    def start(self):
        self.program_loop()


if __name__ == "__main__":
    GraphicsProgram3D().start()
