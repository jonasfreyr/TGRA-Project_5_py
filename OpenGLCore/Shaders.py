
from OpenGL.GL import *
import OpenGL.GLU

from math import * # trigonometry

import sys

from OpenGLCore.Base3DObjects import *
from Core.Constants import *

class Shader3D:
    def __init__(self):
        vert_shader = glCreateShader(GL_VERTEX_SHADER)
        shader_file = open(SHADERS_PATH + "/simple3D.vert")
        glShaderSource(vert_shader,shader_file.read())
        shader_file.close()
        glCompileShader(vert_shader)
        result = glGetShaderiv(vert_shader, GL_COMPILE_STATUS)
        if (result != 1): # shader didn't compile
            print("Couldn't compile vertex shader\nShader compilation Log:\n" + str(glGetShaderInfoLog(vert_shader)))

        frag_shader = glCreateShader(GL_FRAGMENT_SHADER)
        shader_file = open(SHADERS_PATH + "/simple3D.frag")
        glShaderSource(frag_shader,shader_file.read())
        shader_file.close()
        glCompileShader(frag_shader)
        result = glGetShaderiv(frag_shader, GL_COMPILE_STATUS)
        if (result != 1): # shader didn't compile
            print("Couldn't compile fragment shader\nShader compilation Log:\n" + str(glGetShaderInfoLog(frag_shader)))

        self.renderingProgramID = glCreateProgram()
        glAttachShader(self.renderingProgramID, vert_shader)
        glAttachShader(self.renderingProgramID, frag_shader)
        result = glLinkProgram(self.renderingProgramID)
        # if (result != None):
        print("Couldn't link program\nProgram link Log:\n" + str(glGetProgramInfoLog(self.renderingProgramID)))

        self.positionLoc			= glGetAttribLocation(self.renderingProgramID, "a_position")
        glEnableVertexAttribArray(self.positionLoc)

        self.normalLoc = glGetAttribLocation(self.renderingProgramID, "a_normal")
        glEnableVertexAttribArray(self.normalLoc)

        self.uvLoc = glGetAttribLocation(self.renderingProgramID, "a_uv")
        glEnableVertexAttribArray(self.uvLoc)

        ## ADD CODE HERE ##

        self.modelMatrixLoc			= glGetUniformLocation(self.renderingProgramID, "u_model_matrix")
        # self.projectionViewMatrixLoc			= glGetUniformLocation(self.renderingProgramID, "u_projection_view_matrix")

        self.projectionMatrixLoc = glGetUniformLocation(self.renderingProgramID, "u_projection_matrix")
        self.viewMatrixLoc = glGetUniformLocation(self.renderingProgramID, "u_view_matrix")

        self.numOfLightsLoc = glGetUniformLocation(self.renderingProgramID, "u_NUM_OF_LIGHTS")

        # self.colorLoc = glGetUniformLocation(self.renderingProgramID, "u_color")

        # self.lightPosLoc = glGetUniformLocation(self.renderingProgramID, "u_light_positions")
        # self.lightDifLoc = glGetUniformLocation(self.renderingProgramID, "u_light_diffuse")
        self.matDifLoc = glGetUniformLocation(self.renderingProgramID, "u_material_diffuse")

        self.cameraPosLoc = glGetUniformLocation(self.renderingProgramID, "u_camera_position")
        # self.lightSpecLoc = glGetUniformLocation(self.renderingProgramID, "u_light_specular")
        self.matSpecLoc = glGetUniformLocation(self.renderingProgramID, "u_material_specular")
        self.shininessLoc = glGetUniformLocation(self.renderingProgramID, "u_shininess")

        # self.lightAmbientLoc = glGetUniformLocation(self.renderingProgramID, "u_light_ambient")
        self.matAmbientLoc = glGetUniformLocation(self.renderingProgramID, "u_material_ambient")

        self.lightAmountLoc = glGetUniformLocation(self.renderingProgramID, "light_amount")

        self.textureDifLoc = glGetUniformLocation(self.renderingProgramID, "u_tex01")
        self.textureSpecLoc = glGetUniformLocation(self.renderingProgramID, "u_tex02")

        self.usingDifTexLoc = glGetUniformLocation(self.renderingProgramID, "u_using_diffuse_texture")
        self.usingSpecTexLoc = glGetUniformLocation(self.renderingProgramID, "u_using_specular_texture")

        self.setViewLoc = glGetUniformLocation(self.renderingProgramID, "u_draw_view_mat")

        self.setCalcLights = glGetUniformLocation(self.renderingProgramID, "u_calculate_lights")

    def use(self):
        try:
            glUseProgram(self.renderingProgramID)
        except OpenGL.error.GLError:
            print(glGetProgramInfoLog(self.renderingProgramID))
            raise

    def set_model_matrix(self, matrix_array):
        glUniformMatrix4fv(self.modelMatrixLoc, 1, True, matrix_array)

    def set_projection_matrix(self, matrix_array):
        glUniformMatrix4fv(self.projectionMatrixLoc, 1, True, matrix_array)

    def set_view_matrix(self, matrix_array):
        glUniformMatrix4fv(self.viewMatrixLoc, 1, True, matrix_array)


    ## remove
    def set_position_attribute(self, vertex_array):
        # glUniform1f(self.usingTexLoc, 0.0)
        glVertexAttribPointer(self.positionLoc, 3, GL_FLOAT, False, 0, vertex_array)

    def set_normal_attribute(self, vertex_array):
        glVertexAttribPointer(self.normalLoc, 3, GL_FLOAT, False, 0, vertex_array)
    ##

    def set_attribute_buffers(self, vertex_buffer_id):
        # glUniform1f(self.usingTexLoc, 0.0)
        glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_id)
        glVertexAttribPointer(self.positionLoc, 3, GL_FLOAT, False, 6 * sizeof(GLfloat), OpenGL.GLU.ctypes.c_void_p(0))
        glVertexAttribPointer(self.normalLoc, 3, GL_FLOAT, False, 6 * sizeof(GLfloat), OpenGL.GLU.ctypes.c_void_p(3 * sizeof(GLfloat)))

    def set_attribute_buffer_with_uv(self, vertex_buffer_id):
        glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_id)
        glVertexAttribPointer(self.positionLoc, 3, GL_FLOAT, False, 8 * sizeof(GLfloat), OpenGL.GLU.ctypes.c_void_p(0))
        glVertexAttribPointer(self.normalLoc, 3, GL_FLOAT, False, 8 * sizeof(GLfloat),
                              OpenGL.GLU.ctypes.c_void_p(3 * sizeof(GLfloat)))
        glVertexAttribPointer(self.uvLoc, 2, GL_FLOAT, False, 8 * sizeof(GLfloat), OpenGL.GLU.ctypes.c_void_p(6 * sizeof(GLfloat)))

    def set_using_diffuse_texture(self, using):
        glUniform1f(self.usingDifTexLoc, using)

    def set_using_specular_texture(self, using):
        glUniform1f(self.usingSpecTexLoc, using)

    def set_uv_attribute(self, vertex_array):
        glVertexAttribPointer(self.uvLoc, 2, GL_FLOAT, False, 0, vertex_array)

    ## Diffuse
    def set_light_position(self, x, y, z, i):
        loc = glGetUniformLocation(self.renderingProgramID, f"u_light_positions[{i}]")
        glUniform4f(loc, x, y, z, 1.0)

    def set_material_diffuse(self, r, g, b, a=1.0):
        glUniform4f(self.matDifLoc, r, g, b, a)

    def set_material_diffuse_color(self, color):
        glUniform4f(self.matDifLoc, color.r, color.g, color.b, 1.0)

    def set_light_diffuse(self, r, g, b, i):
        loc = glGetUniformLocation(self.renderingProgramID, f"u_light_diffuses[{i}]")
        glUniform4f(loc, r, g, b, 1.0)

    ## Specular
    def set_camera_position(self, x, y, z):
        glUniform4f(self.cameraPosLoc, x, y, z, 1.0)

    def set_light_specular(self, r, g, b, i):
        loc = glGetUniformLocation(self.renderingProgramID, f"u_light_speculars[{i}]")
        glUniform4f(loc, r, g, b, 1.0)

    def set_material_specular(self, r, g, b):
        glUniform4f(self.matSpecLoc, r, g, b, 1.0)

    def set_material_specular_color(self, color):
        glUniform4f(self.matSpecLoc, color.r, color.g, color.b, 1.0)

    def set_shininess(self, shininess):
        glUniform1f(self.shininessLoc, shininess)

    ## Ambient
    def set_light_ambient(self, r, g, b, i):
        loc = glGetUniformLocation(self.renderingProgramID, f"u_light_ambients[{i}]")
        glUniform4f(loc, r, g, b, 1.0)

    def set_material_ambient(self, r, g, b):
        glUniform4f(self.matAmbientLoc, r, g, b, 1.0)

    def set_material_ambient_color(self, color):
        glUniform4f(self.matAmbientLoc, color.r, color.g, color.b, 1.0)

    def set_light_amount(self, amount):
        glUniform1i(self.lightAmountLoc, amount)

    def set_light_dist(self, distance, i):
        loc = glGetUniformLocation(self.renderingProgramID, f"u_light_dists[{i}]")
        glUniform1f(loc, distance)

    def set_texture_diffuse(self, number):
        glUniform1i(self.textureDifLoc, number)

    def set_texture_specular(self, number):
        glUniform1i(self.textureSpecLoc, number)

    def set_view(self, i):
        glUniform1f(self.setViewLoc, i)

    def set_calculate_lights(self, i):
        glUniform1f(self.setCalcLights, i)
