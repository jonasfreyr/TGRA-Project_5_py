from math import *

import numpy
from OpenGL.GL import *


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)


class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def __len__(self):
        return sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def __str__(self):
        return f"V(x: {self.x}, y: {self.y}, z: {self.z})"

    def normalize(self):
        length = self.__len__()
        self.x /= length
        self.y /= length
        self.z /= length

    def set(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        return Vector(self.y*other.z - self.z*other.y, self.z*other.x - self.x*other.z, self.x*other.y - self.y*other.x)

class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def __str__(self):
        return f"C({self.r}, {self.g}, {self.b})"

class Material:
    def __init__(self, diffuse = None, specular = None, ambient = None,shininess = None):
        self.diffuse = Color(0.0, 0.0, 0.0) if diffuse == None else diffuse
        self.specular = Color(0.0, 0.0, 0.0) if specular == None else specular
        self.shininess = 1 if shininess == None else shininess
        self.ambient = Color(0.0, 0.0, 0.0) if ambient == None else ambient



class Cube:
    def __init__(self):
        self.position_array = [-0.5, -0.5, -0.5,
                            -0.5, 0.5, -0.5,
                            0.5, 0.5, -0.5,
                            0.5, -0.5, -0.5,
                            -0.5, -0.5, 0.5,
                            -0.5, 0.5, 0.5,
                            0.5, 0.5, 0.5,
                            0.5, -0.5, 0.5,
                            -0.5, -0.5, -0.5,
                            0.5, -0.5, -0.5,
                            0.5, -0.5, 0.5,
                            -0.5, -0.5, 0.5,
                            -0.5, 0.5, -0.5,
                            0.5, 0.5, -0.5,
                            0.5, 0.5, 0.5,
                            -0.5, 0.5, 0.5,
                            -0.5, -0.5, -0.5,
                            -0.5, -0.5, 0.5,
                            -0.5, 0.5, 0.5,
                            -0.5, 0.5, -0.5,
                            0.5, -0.5, -0.5,
                            0.5, -0.5, 0.5,
                            0.5, 0.5, 0.5,
                            0.5, 0.5, -0.5]
        self.normal_array = [0.0, 0.0, -1.0,
                            0.0, 0.0, -1.0,
                            0.0, 0.0, -1.0,
                            0.0, 0.0, -1.0,
                            0.0, 0.0, 1.0,
                            0.0, 0.0, 1.0,
                            0.0, 0.0, 1.0,
                            0.0, 0.0, 1.0,
                            0.0, -1.0, 0.0,
                            0.0, -1.0, 0.0,
                            0.0, -1.0, 0.0,
                            0.0, -1.0, 0.0,
                            0.0, 1.0, 0.0,
                            0.0, 1.0, 0.0,
                            0.0, 1.0, 0.0,
                            0.0, 1.0, 0.0,
                            -1.0, 0.0, 0.0,
                            -1.0, 0.0, 0.0,
                            -1.0, 0.0, 0.0,
                            -1.0, 0.0, 0.0,
                            1.0, 0.0, 0.0,
                            1.0, 0.0, 0.0,
                            1.0, 0.0, 0.0,
                            1.0, 0.0, 0.0]

        self.uv_array = [
            0.0, 0.0,
            0.0, 1.0,
            1.0, 1.0,
            1.0, 0.0,

            0.0, 0.0,
            0.0, 1.0,
            1.0, 1.0,
            1.0, 0.0,

            0.0, 0.0,
            0.0, 1.0,
            1.0, 1.0,
            1.0, 0.0,

            0.0, 0.0,
            0.0, 1.0,
            1.0, 1.0,
            1.0, 0.0,

            0.0, 0.0,
            0.0, 1.0,
            1.0, 1.0,
            1.0, 0.0,

            0.0, 0.0,
            0.0, 1.0,
            1.0, 1.0,
            1.0, 0.0
        ]

    def set_vertices(self, shader):
        shader.set_position_attribute(self.position_array)
        shader.set_normal_attribute(self.normal_array)
        shader.set_uv_attribute(self.uv_array)

    def draw(self, shader):
        glDrawArrays(GL_TRIANGLE_FAN, 0, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 4, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 8, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 12, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 16, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 20, 4)


class OptiCube:
    def __init__(self):
        vertex_array = [    -0.5, -0.5, -0.5,      0.0, 0.0, -1.0,
                            -0.5, 0.5, -0.5,        0.0, 0.0, -1.0,
                            0.5, 0.5, -0.5,         0.0, 0.0, -1.0,
                            0.5, -0.5, -0.5,        0.0, 0.0, -1.0,
                            -0.5, -0.5, 0.5,        0.0, 0.0, 1.0,
                            -0.5, 0.5, 0.5,         0.0, 0.0, 1.0,
                            0.5, 0.5, 0.5,          0.0, 0.0, 1.0,
                            0.5, -0.5, 0.5,         0.0, 0.0, 1.0,
                            -0.5, -0.5, -0.5,       0.0, -1.0, 0.0,
                            0.5, -0.5, -0.5,        0.0, -1.0, 0.0,
                            0.5, -0.5, 0.5,         0.0, -1.0, 0.0,
                            -0.5, -0.5, 0.5,        0.0, -1.0, 0.0,
                            -0.5, 0.5, -0.5,        0.0, 1.0, 0.0,
                            0.5, 0.5, -0.5,         0.0, 1.0, 0.0,
                            0.5, 0.5, 0.5,          0.0, 1.0, 0.0,
                            -0.5, 0.5, 0.5,         0.0, 1.0, 0.0,
                            -0.5, -0.5, -0.5,       -1.0, 0.0, 0.0,
                            -0.5, -0.5, 0.5,        -1.0, 0.0, 0.0,
                            -0.5, 0.5, 0.5,         -1.0, 0.0, 0.0,
                            -0.5, 0.5, -0.5,        -1.0, 0.0, 0.0,
                            0.5, -0.5, -0.5,        1.0, 0.0, 0.0,
                            0.5, -0.5, 0.5,         1.0, 0.0, 0.0,
                            0.5, 0.5, 0.5,          1.0, 0.0, 0.0,
                            0.5, 0.5, -0.5,         1.0, 0.0, 0.0]

        self.uv_array = [
            0.0, 0.0,
            0.0, 1.0,
            1.0, 1.0,
            1.0, 0.0,

            0.0, 0.0,
            0.0, 1.0,
            1.0, 1.0,
            1.0, 0.0,

            0.0, 0.0,
            0.0, 1.0,
            1.0, 1.0,
            1.0, 0.0,

            0.0, 0.0,
            0.0, 1.0,
            1.0, 1.0,
            1.0, 0.0,

            0.0, 0.0,
            0.0, 1.0,
            1.0, 1.0,
            1.0, 0.0,

            0.0, 0.0,
            0.0, 1.0,
            1.0, 1.0,
            1.0, 0.0
        ]

        self.vertex_buffer_id = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer_id)
        glBufferData(GL_ARRAY_BUFFER, numpy.array(vertex_array, dtype='float32'), GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

    def set_vertices(self, shader):
        shader.set_uv_attribute(self.uv_array)

    def draw(self, shader):
        shader.set_attribute_buffers(self.vertex_buffer_id)
        glDrawArrays(GL_TRIANGLE_FAN, 0, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 4, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 8, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 12, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 16, 4)
        glDrawArrays(GL_TRIANGLE_FAN, 20, 4)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

class OriginalSphere:
    def __init__(self, stacks=12, slices=24):
        self.vertex_array = []
        self.slices = slices
        stack_interval = pi / stacks
        slice_interval = 2.0 * pi / slices
        self.vertex_count = 0

        for stack_count in range(stacks):
            stack_angle = stack_count * stack_interval
            for slice_count in range(slices + 1):
                slice_angle = slice_count * slice_interval
                self.vertex_array.append(sin(stack_angle) * cos(slice_angle))
                self.vertex_array.append(cos(stack_angle))
                self.vertex_array.append(sin(stack_angle) * sin(slice_angle))

                self.vertex_array.append(sin(stack_angle + stack_interval) * cos(slice_angle))
                self.vertex_array.append(cos(stack_angle + stack_interval))
                self.vertex_array.append(sin(stack_angle + stack_interval) * sin(slice_angle))
                self.vertex_count += 2
    def draw(self, shader):
        shader.set_position_attribute(self.vertex_array)
        shader.set_normal_attribute(self.vertex_array)
        for i in range(0, self.vertex_count, (self.slices + 1) * 2):
            glDrawArrays(GL_TRIANGLE_STRIP, i, (self.slices + 1) * 2)


class OptiSphere:
    def __init__(self, stacks=12, slices=24):
        vertex_array = []
        self.slices = slices
        stack_interval = pi / stacks
        slice_interval = 2.0 * pi / slices
        self.vertex_count = 0

        for stack_count in range(stacks):
            stack_angle = stack_count * stack_interval
            for slice_count in range(slices + 1):
                slice_angle = slice_count * slice_interval

                for _ in range(2):
                    vertex_array.append(sin(stack_angle) * cos(slice_angle))
                    vertex_array.append(cos(stack_angle))
                    vertex_array.append(sin(stack_angle) * sin(slice_angle))

                vertex_array.append(slice_count / slices)
                vertex_array.append(stack_count / stacks)

                for _ in range(2):
                    vertex_array.append(sin(stack_angle + stack_interval) * cos(slice_angle))
                    vertex_array.append(cos(stack_angle + stack_interval))
                    vertex_array.append(sin(stack_angle + stack_interval) * sin(slice_angle))

                vertex_array.append(slice_count / slices)
                vertex_array.append((stack_count + 1) / stacks)

                self.vertex_count += 2

        self.vertex_buffer_id = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer_id)
        glBufferData(GL_ARRAY_BUFFER, numpy.array(vertex_array, dtype='float32'), GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        vertex_array = None  # El Garbo collector

    def draw(self, shader):
        shader.set_attribute_buffer_with_uv(self.vertex_buffer_id)
        for i in range(0, self.vertex_count, (self.slices + 1) * 2):
            glDrawArrays(GL_TRIANGLE_STRIP, i, (self.slices + 1) * 2)

        glBindBuffer(GL_ARRAY_BUFFER, 0)


class MeshModel:
    def __init__(self):
        self.vertex_arrays = dict()
        # self.index_arrays = dict()
        self.mesh_materials = dict()
        self.materials = dict()
        self.vertex_counts = dict()
        self.vertex_buffer_ids = dict()

    def add_vertex(self, mesh_id, position, normal, uv):
        if mesh_id not in self.vertex_arrays:
            self.vertex_arrays[mesh_id] = []
            self.vertex_counts[mesh_id] = 0
        self.vertex_arrays[mesh_id] += [position.x, position.y, position.z, normal.x, normal.y, normal.z, uv.x, uv.y]
        self.vertex_counts[mesh_id] += 1

    def set_mesh_material(self, mesh_id, mat_id):
        self.mesh_materials[mesh_id] = mat_id

    def add_material(self, mat_id, mat):
        self.materials[mat_id] = mat

    def set_opengl_buffers(self):
        for mesh_id in self.mesh_materials.keys():
            self.vertex_buffer_ids[mesh_id] = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer_ids[mesh_id])
            glBufferData(GL_ARRAY_BUFFER, numpy.array(self.vertex_arrays[mesh_id], dtype='float32'), GL_STATIC_DRAW)
            glBindBuffer(GL_ARRAY_BUFFER, 0)

    def draw(self, shader):
        for mesh_id, mesh_material in self.mesh_materials.items():
            material = self.materials[mesh_material]
            shader.set_material_diffuse_color(material.diffuse)
            shader.set_material_specular_color(material.specular)
            # shader.set_material_ambient_color(material.ambient)
            shader.set_shininess(material.shininess)
            shader.set_attribute_buffer_with_uv(self.vertex_buffer_ids[mesh_id])
            glDrawArrays(GL_TRIANGLES, 0, self.vertex_counts[mesh_id])
            glBindBuffer(GL_ARRAY_BUFFER, 0)


def lerp(v1: Vector, v2: Vector, t: float) -> Vector:
    temp_1 = v1 * (1 - t)
    temp_2 = v2 * t

    return temp_1 + temp_2


if __name__ == '__main__':
    t = 0.75
    P1 = Vector(15, 5, 2)
    P2 = Vector(10, 2, 2)
    P3 = Vector(5, 7, 2)
    P4 = Vector(0, 0, 2)

    P12 = lerp(P1, P2, t)
    P23 = lerp(P2, P3, t)
    P34 = lerp(P3, P4, t)

    print("P12:", P12)
    print("P23:", P23)
    print("P34:", P34)

    P1223 = lerp(P12, P23, t)
    P2334 = lerp(P23, P34, t)

    print("P1223:", P1223)
    print("P2334:", P2334)

    Final = lerp(P1223, P2334, t)

    print("Final:", Final)