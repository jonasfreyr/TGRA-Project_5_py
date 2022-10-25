from Core.Constants import ROCKET_SPEED, ROCKET_LIFE_TIME
from Core.Vector import Vector
from Game.Object import Object


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

        self.vel = rotation.copy()
        self.vel.normalize()
        self.vel *= ROCKET_SPEED

        self.life_time = 0
        self.kill = False

    def update(self, delta_time):
        if self.life_time >= ROCKET_LIFE_TIME:
            self.kill = True
            return

        self.pos += self.vel * delta_time

        self.life_time += delta_time

    def draw(self, shader):
        if self.kill: return
        super(Rocket, self).draw(shader)
