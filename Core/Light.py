from Core.Color import Color
from Core.Vector import Vector


class Light:
    def __init__(self, pos: Vector, diffuse: Color, specular: Color, ambient: Color, distance: float):
        self.pos = pos
        self.diffuse = diffuse
        self.specular = specular
        self.ambient = ambient
        self.distance = distance

    def draw(self, shader, i):
        shader.set_light_position(*self.pos.to_array(), i)
        shader.set_light_diffuse(*self.diffuse.to_array(), i)
        shader.set_light_specular(*self.specular.to_array(), i)
        shader.set_light_ambient(*self.ambient.to_array(), i)
        shader.set_light_dist(self.distance, i)
