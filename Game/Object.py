from Core.Color import Color
from Core.Matrices import ModelMatrix
from Core.Vector import Vector
from OpenGL.GL import *

from OpenGLCore.Base3DObjects import Cube


class Object:
    def __init__(self, pos: Vector, rotation: Vector, scale: Vector, object_model, static=False, do_rotation_first=False):
        self.pos = pos
        self.rotation = rotation
        self.scale = scale
        self.object_model = object_model
        self.model_matrix = ModelMatrix()

        self.do_rotation_first = do_rotation_first
        self.static = static

        if static:
            if not do_rotation_first:
                self.model_matrix.add_translation(*self.pos.to_array())
                self.model_matrix.add_scale(*self.scale.to_array())
                self.model_matrix.add_rotation(*self.rotation.to_array())
            else:
                self.model_matrix.add_rotation(*self.rotation.to_array())
                self.model_matrix.add_translation(*self.pos.to_array())
                self.model_matrix.add_scale(*self.scale.to_array())

    def update(self, delta_time):
        pass

    def draw(self, shader):
        if not self.static:
            self.model_matrix.push_matrix()
            if not self.do_rotation_first:
                self.model_matrix.add_translation(*self.pos.to_array())
                self.model_matrix.add_scale(*self.scale.to_array())
                self.model_matrix.add_rotation(*self.rotation.to_array())
            else:
                self.model_matrix.add_rotation(*self.rotation.to_array())
                self.model_matrix.add_translation(*self.pos.to_array())
                self.model_matrix.add_scale(*self.scale.to_array())

            shader.set_model_matrix(self.model_matrix.matrix)
            self.object_model.draw(shader)
            self.model_matrix.pop_matrix()
        else:
            shader.set_model_matrix(self.model_matrix.matrix)
            self.object_model.draw(shader)


class Teeth(Object):
    def __init__(self, pos, rotation, scale, object_model):
        super(Teeth, self).__init__(pos, rotation, scale, object_model)

    def update(self, delta_time):
        self.rotation.y += 10 * delta_time


class ObjectCube:
    def __init__(self, pos: Vector, rotation: Vector, scale: Vector,
                        diffuse_color: Color, specular_color: Color, ambient_color: Color, shininess: float,
                        cube: Cube, diffuse_texture_id: int = None, specular_texture_id: int = None):

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

        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(*self.pos.to_array())
        self.model_matrix.add_scale(*self.scale.to_array())
        self.model_matrix.add_rotation(*self.rotation.to_array())
        shader.set_model_matrix(self.model_matrix.matrix)
        shader.set_material_diffuse_color(self.diffuse_color)
        shader.set_material_specular_color(self.specular_color)
        shader.set_material_ambient_color(self.ambient_color)
        shader.set_shininess(self.shininess)
        self.cube.draw(shader)
        self.model_matrix.pop_matrix()


class RotatingCube(ObjectCube):
    def __init__(self, pos, scale, diffuse_texture_id: int, specular_texture_id: int, cube: Cube):
        super(RotatingCube, self).__init__(pos, Vector(0, 0, 0), scale, Color(1, 1, 1), Color(1, 1, 1), Color(.1, .1, .1), 10, cube, diffuse_texture_id, specular_texture_id)

    def update(self, delta_time):
        self.rotation.x += 100 * delta_time
        self.rotation.y += 100 * delta_time
