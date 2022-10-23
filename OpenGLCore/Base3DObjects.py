from math import *

import numpy
from OpenGL.GL import *


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
