from Core.Color import Color
from Core.Constants import *
from Core.Vector import Vector
from Game.Object import Object, Collider, ObjectCube
from OpenGLCore.Base3DObjects import Cube


class Gun(Object):
    def __init__(self, pos: Vector, rotation: Vector, scale: Vector, object_model):
        super(Gun, self).__init__(pos, rotation, scale, object_model)

    def draw(self, shader):
        shader.set_view(0.0)
        super(Gun, self).draw(shader)
        shader.set_view(1.0)


class Rocket(Object):
    def __init__(self, pos: Vector, rotation: Vector, scale: Vector, object_model):
        super(Rocket, self).__init__(pos, rotation, scale, object_model)

        self.vel = Vector(0, 0, 0)

        self.life_time = 0
        self.kill = False

        self.testing = ObjectCube(pos, rotation, Vector(ROCKET_WIDTH, ROCKET_HEIGHT, ROCKET_DEPTH), Color(1, 1, 1), Color(1, 1, 1), Color(.1, .1, .1), 10, Cube())

        self.updated = True

    def set_vel(self, look_pos):
        self.vel = look_pos.copy()
        self.vel.normalize()
        self.vel *= ROCKET_SPEED
        pass

    @property
    def corners(self):
        return [self.pos]

    def update(self, delta_time, colliders):
        if self.life_time >= ROCKET_LIFE_TIME:
            self.kill = True
            return

        for collider in colliders:
            for corner in self.corners:
                if collider.is_in_collider(corner):
                    self.kill = True
                    return

        self.pos += self.vel * delta_time

        if self.pos.y <= 0:
            self.kill = True

        self.life_time += delta_time

    def draw(self, shader):
        if self.kill: return
        super(Rocket, self).draw(shader)

        self.testing.draw(shader)

