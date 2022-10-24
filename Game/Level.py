from math import *
import random
import numpy
from OpenGL.GL import *
from Core.Color import Material
from Core.Constants import *
from OpenGLCore import ojb_3D_loading

from Game.Object import Teeth, RotatingCube, Object
from Core.Vector import *


class Level:
    def __init__(self, grass_patch_model, grass_plane_model, plane_scale=2, grass_scale=1, grass_amount=20):
        self.plane_size = Vector(plane_scale, plane_scale, plane_scale)
        self.plane_scale = 2
        self.grass_scale = grass_scale

        self.grass_amount = grass_amount
        self.map_size = self.plane_scale * WORLD_WIDTH

        self.floor_tile_array = []
        self.grass_array = []

        self.GRA(grass_patch_model, grass_plane_model)

    def GRA(self, grass_patch_model, grass_plane_model):
        self.generate_floor(grass_plane_model)
        self.generate_grass(grass_patch_model)

    def generate_floor(self, grass_plane_model):

        for i in range(WORLD_WIDTH):
            for k in range(WORLD_DEPTH):
                # pos, rotation, scale, object_model
                new_floor_tile = Object(
                    Vector(i * self.plane_scale, 0, k * self.plane_scale),
                    Vector(0, 0, 0),
                    Vector(0.6666, 0.6666, 0.6666),
                    grass_plane_model,
                    True
                )

                self.floor_tile_array.append(new_floor_tile)

    def generate_grass(self, grass_patch_model):
        for i in range(self.grass_amount):
            # change positions here

            random_coordinates = random.sample(range(0, self.map_size), 2)
            new_grass = Object(Vector(random_coordinates[0], 0, random_coordinates[1]),
                               Vector(0, 0, 0),
                               Vector(5, 5, 5),
                               grass_patch_model,
                               True)
            self.grass_array.append(new_grass)

    def draw(self, shader):
        for tile in self.floor_tile_array:
            tile.draw(shader)

        for grass in self.grass_array:
            grass.draw(shader)
