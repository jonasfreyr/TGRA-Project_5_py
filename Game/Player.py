import pygame.mouse
from pygame.constants import *

from Core.Vector import Vector
from Core.Constants import *
from Core.Matrices import ViewMatrix, ProjectionMatrix
from Game.Gun import Rocket


class FlyingPlayer:
    def __init__(self, pos: Vector, height: float, radius: float):
        self.pos = pos
        self.height = height
        self.x_rotation = 0
        self.y_rotation = 0
        self.radius = radius

        self.view_matrix = ViewMatrix()
        self.projection_matrix = ProjectionMatrix()

        self.view_matrix.slide(pos.x, pos.y + height, pos.z)
        self.projection_matrix.set_perspective(FOV, WINDOW_WIDTH / WINDOW_HEIGHT, 0.1, 50)

    @property
    def top_pos(self):
        temp = self.pos.copy()
        temp.y += self.height
        return temp

    def update(self, delta_time, keys):
        if keys[K_UP]:
            self.view_matrix.pitch(100 * delta_time)
        elif keys[K_DOWN]:
            self.view_matrix.pitch(-100 * delta_time)
        if keys[K_LEFT]:
            self.view_matrix.yaw(-100 * delta_time)
        elif keys[K_RIGHT]:
            self.view_matrix.yaw(100 * delta_time)

        if keys[K_w]:
            self.view_matrix.slide(0, 0, -10 * delta_time)
        elif keys[K_s]:
            self.view_matrix.slide(0, 0, 10 * delta_time)
        if keys[K_a]:
            self.view_matrix.slide(-10 * delta_time, 0, 0)
        elif keys[K_d]:
            self.view_matrix.slide(10 * delta_time, 0, 0)

        if keys[K_q]:
            self.view_matrix.roll(100 * delta_time)
        elif keys[K_e]:
            self.view_matrix.roll(-100 * delta_time)

        if keys[K_r]:
            self.view_matrix.slide(0, 10 * delta_time, 0)
        elif keys[K_f]:
            self.view_matrix.slide(0, -10 * delta_time, 0)
    
    def draw(self, shader):
        self.pos = Vector(self.view_matrix.eye.x, self.view_matrix.eye.y, self.view_matrix.eye.z)
        shader.set_camera_position(self.pos.x, self.pos.y, self.pos.z)
        shader.set_view_matrix(self.view_matrix.get_matrix())


class Player:
    def __init__(self, pos: Vector, height: float, radius: float, gun, game):
        self.pos = pos
        self.height = height
        self.x_rotation = 0
        self.y_rotation = 0
        self.radius = radius

        self.game = game

        self.view_matrix = ViewMatrix()
        self.projection_matrix = ProjectionMatrix()

        self.view_matrix.slide(pos.x, pos.y + height, pos.z)
        self.projection_matrix.set_perspective(FOV, WINDOW_WIDTH / WINDOW_HEIGHT, 0.1, 50)

        self.__landed = True
        self.jump_vel = 0

        self.health = PLAYER_HEALTH

        self.gun = gun
        self.fire_time = ROCKET_FIRE_RATE

    @property
    def top_pos(self):
        temp = self.pos.copy()
        temp.y += self.height
        return temp

    def update(self, delta_time, keys):
        move_vec = Vector(0, 0, 0)

        mouse_click, _, _ = pygame.mouse.get_pressed()

        del_x, del_y = pygame.mouse.get_rel()

        self.x_rotation += del_x * PLAYER_MOUSE_SPEED * delta_time
        self.y_rotation -= del_y * PLAYER_MOUSE_SPEED * delta_time

        if self.y_rotation > PLAYER_MOUSE_MAX_MIN_Y_VALUE:
            self.y_rotation = PLAYER_MOUSE_MAX_MIN_Y_VALUE
        elif self.y_rotation < -PLAYER_MOUSE_MAX_MIN_Y_VALUE:
            self.y_rotation = -PLAYER_MOUSE_MAX_MIN_Y_VALUE

        if keys[K_w]:
            move_vec.z += -PLAYER_MOVEMENT_SPEED * delta_time
        elif keys[K_s]:
            move_vec.z += PLAYER_MOVEMENT_SPEED * delta_time

        if keys[K_a]:
            move_vec.x += -PLAYER_MOVEMENT_SPEED * delta_time
        elif keys[K_d]:
            move_vec.x += PLAYER_MOVEMENT_SPEED * delta_time

        if keys[K_SPACE] and self.__landed:
            self.__landed = False
            self.jump_vel = PLAYER_JUMP_FORCE

        if mouse_click and self.fire_time >= ROCKET_FIRE_RATE:
            self.fire_time = 0

            look_pos = Vector(0, 0, -1)
            look_pos.rotate2dXAxis(self.y_rotation)
            look_pos.rotate2d(self.x_rotation)

            self.game.shoot(look_pos)

        move_vec.rotate2d(self.x_rotation)

        self.pos += move_vec
        self.jump_vel -= GRAVITY * delta_time

        self.pos.y += self.jump_vel * delta_time

        if self.pos.y <= 0:
            self.pos.y = 0
            self.jump_vel = 0
            self.__landed = True

        self.update_camera()

        self.fire_time += delta_time

    def update_camera(self):
        temp = self.top_pos

        look_pos = Vector(0, 0, -1)
        look_pos.rotate2dXAxis(self.y_rotation)
        look_pos.rotate2d(self.x_rotation)

        self.view_matrix.look(temp, temp+look_pos, Vector(0, 1, 0))

    def draw(self, shader):
        pos = self.view_matrix.eye
        shader.set_camera_position(pos.x, pos.y, pos.z)
        shader.set_view_matrix(self.view_matrix.get_matrix())

        if self.gun:
            self.gun.draw(shader)
