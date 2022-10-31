import math

from Core.Color import Color
from Core.Matrices import ModelMatrix
from Core.Vector import Vector
from OpenGL.GL import *

from OpenGLCore.Base3DObjects import Cube


class Object:
    def __init__(self, pos: Vector, rotation: Vector, scale: Vector, object_model, collider: "Collider"=None, static=False):
        self.pos = pos
        self.rotation = rotation
        self.scale = scale
        self.object_model = object_model
        self.model_matrix = ModelMatrix()

        self.static = static

        self.collider = collider

        if static:
            self.model_matrix.add_translation(*self.pos.to_array())
            self.model_matrix.add_rotation(*self.rotation.to_array())
            self.model_matrix.add_scale(*self.scale.to_array())

    def update(self, delta_time):
        pass

    def collide(self, pos, radius):
        return self.collider.collide_player(pos, radius)

    def draw(self, shader):
        if not self.static:
            self.model_matrix.push_matrix()

            self.model_matrix.add_translation(*self.pos.to_array())
            self.model_matrix.add_rotation(*self.rotation.to_array())
            self.model_matrix.add_scale(*self.scale.to_array())

            shader.set_model_matrix(self.model_matrix.matrix)
            self.object_model.draw(shader)
            self.model_matrix.pop_matrix()
        else:
            shader.set_model_matrix(self.model_matrix.matrix)
            self.object_model.draw(shader)


class Collider:
    def __init__(self, pos: Vector, size: Vector):
        self.pos = pos
        # self.pos.y += size.y
        self.size = size

        self.yes = ObjectCube(pos, Vector(0, 0, 0), size,
                              Color(1, 1, 1,), Color(1, 1, 1),
                              Color(1, 1, 1,), 10, Cube())

    def __str__(self):
        return f"Collider(Vector({self.pos.x}, {self.pos.y}, {self.pos.z}), Vector({self.size.x}, {self.size.y}, {self.size.z}))"

    def copy(self):
        return Collider(self.pos.copy(), self.size.copy())

    @property
    def minX(self):
        return self.pos.x - self.size.x / 2

    @property
    def maxX(self):
        return self.pos.x + self.size.x / 2

    @property
    def minY(self):
        return self.pos.y - self.size.y / 2

    @property
    def maxY(self):
        return self.pos.y + self.size.y / 2

    @property
    def minZ(self):
        return self.pos.z - self.size.z / 2

    @property
    def maxZ(self):
        return self.pos.z + self.size.z / 2

    def sphere_collide(self, pos, radius):
        x = max(self.minX, min(pos.x, self.maxX))
        y = max(self.minY, min(pos.y, self.maxY))
        z = max(self.minZ, min(pos.z, self.maxZ))

        distance = math.sqrt(
            (x - pos.x) * (x - pos.x) +
            (y - pos.y) * (y - pos.y) +
            (z - pos.z) * (z - pos.z)
        )

        if distance < radius:
            vec = pos - Vector(x, y, z)
            try:
                vec.normalize()
            except ZeroDivisionError:
                pass

            vec.mul(radius)

            return Vector(x, y, z), vec
        return pos, Vector(0, 0, 0)

    def is_in_collider(self, pos):
        return self.minX <= pos.x <= self.maxX and \
                self.minY <= pos.y <= self.maxY and \
                self.minZ <= pos.z <= self.maxZ

    def update(self, move_vec):
        self.pos += move_vec

    def draw(self, shader):
        self.yes.draw(shader)


class Teeth(Object):
    def __init__(self, pos, rotation, scale, object_model):
        super(Teeth, self).__init__(pos, rotation, scale, object_model)

    def update(self, delta_time):
        self.rotation.y += 10 * delta_time


class ObjectCube:
    def __init__(self, pos: Vector, rotation: Vector, scale: Vector,
                        diffuse_color: Color, specular_color: Color, ambient_color: Color, shininess: float,
                        cube: Cube, diffuse_texture_id: int = None, specular_texture_id: int = None, static=False):

        self.pos = pos
        self.rotation = rotation
        self.scale = scale

        self.diffuse_color = diffuse_color
        self.specular_color = specular_color
        self.ambient_color = ambient_color
        self.shininess = shininess

        self.diffuse_texture_id = diffuse_texture_id
        self.specular_texture_id = specular_texture_id

        self.model_matrix = ModelMatrix()

        self.cube = cube

        self.static = static

        if static:
            self.model_matrix.add_translation(*self.pos.to_array())
            self.model_matrix.add_rotation(*self.rotation.to_array())
            self.model_matrix.add_scale(*self.scale.to_array())

    def update(self, delta_time):
        pass

    def draw(self, shader):
        shader.set_using_diffuse_texture(1.0)
        shader.set_using_specular_texture(1.0)

        if self.diffuse_texture_id:
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, self.diffuse_texture_id)
            shader.set_texture_diffuse(0)
        else:
            shader.set_using_diffuse_texture(0.0)

        if self.specular_texture_id:
            glActiveTexture(GL_TEXTURE1)
            glBindTexture(GL_TEXTURE_2D, self.specular_texture_id)
            shader.set_texture_specular(1)
        else:
            shader.set_using_specular_texture(0.0)

        if not self.static:
            self.model_matrix.push_matrix()
            self.model_matrix.add_translation(*self.pos.to_array())
            self.model_matrix.add_rotation(*self.rotation.to_array())
            self.model_matrix.add_scale(*self.scale.to_array())
            shader.set_model_matrix(self.model_matrix.matrix)
            shader.set_material_diffuse_color(self.diffuse_color)
            shader.set_material_specular_color(self.specular_color)
            shader.set_material_ambient_color(self.ambient_color)
            shader.set_shininess(self.shininess)
            self.cube.draw(shader)
            self.model_matrix.pop_matrix()
        else:
            shader.set_model_matrix(self.model_matrix.matrix)
            shader.set_material_diffuse_color(self.diffuse_color)
            shader.set_material_specular_color(self.specular_color)
            shader.set_material_ambient_color(self.ambient_color)
            shader.set_shininess(self.shininess)
            self.cube.draw(shader)


class RotatingCube(ObjectCube):
    def __init__(self, pos, scale, diffuse_texture_id: int, specular_texture_id: int, cube: Cube):
        super(RotatingCube, self).__init__(pos, Vector(0, 0, 0), scale, Color(1, 1, 1), Color(1, 1, 1), Color(.1, .1, .1), 10, cube, diffuse_texture_id, specular_texture_id)

    def update(self, delta_time):
        self.rotation.x += 100 * delta_time
        self.rotation.y += 100 * delta_time


class NetworkPlayer(Object):
    def __init__(self, pos: Vector, rotation: Vector, scale: Vector, object_model):
        super(NetworkPlayer, self).__init__(pos, rotation, scale, object_model)

        self.updated = True
