from Core.Color import Color
from Core.Constants import *
from Core.Vector import Vector
from Game.Object import Object, Collider, ObjectCube
from OpenGLCore.Base3DObjects import Cube


class Explosion(Object):
    def __init__(self, pos: Vector, rotation: Vector, scale: Vector, object_model):
        super(Explosion, self).__init__(pos, rotation, scale, object_model, False)

        self.life_time = 0
        self.kill = False

    def update(self, delta_time):
        self.life_time += delta_time

        if self.life_time >= EXPLOSION_LIFE_TIME:
            self.kill = True
            return

        scale = 1 - (self.life_time / EXPLOSION_LIFE_TIME)

        self.scale = Vector(scale, scale, scale)
