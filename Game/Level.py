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
    def __init__(self, grass_patch_model, grass_plane_model, fence_model ,plane_scale=2, grass_scale=1, grass_amount=20):
        self.plane_size = Vector(plane_scale, plane_scale, plane_scale)
        self.plane_scale = 2
        self.grass_scale = grass_scale

        self.grass_amount = grass_amount
        self.map_size = self.plane_scale * WORLD_WIDTH

        self.floor_tile_array = []
        self.grass_array = []
        self.fence_array = []

        self.GRA(grass_patch_model, grass_plane_model, fence_model)

    def GRA(self, grass_patch_model, grass_plane_model,fence_model):
        self.generate_floor(grass_plane_model,fence_model)
        self.generate_grass(grass_patch_model)
        self.generate_fences(fence_model)

    def generate_floor(self, grass_plane_model, fence_model):
        for i in range(WORLD_WIDTH):
            new_fence = Object(
                    Vector(i * self.plane_scale + 0.8, 0, 0),
                    Vector(0, 0, 0),
                    Vector(0.39, 0.39, 0.39),
                    fence_model,
                    static=True
                )
            self.fence_array.append(new_fence)
            for k in range(WORLD_DEPTH):
                # pos, rotation, scale, object_model
                new_floor_tile = Object(
                    Vector(i * self.plane_scale, 0, k * self.plane_scale),
                    Vector(0, 0, 0),
                    Vector(0.6666, 0.6666, 0.6666),
                    grass_plane_model,
                    static=True
                )
                if (k == WORLD_DEPTH-1 ):
                    new_fence = Object(
                        Vector(i * self.plane_scale + 0.8, 0, k * self.plane_scale -1.5 ),
                        Vector(0, 0, 0),
                        Vector(0.39, 0.39, 0.39),
                        fence_model,
                        static=True
                    )
                elif(i == 0):
                    new_fence = Object(
                        Vector(i * self.plane_scale + 0.8, 0, k * self.plane_scale - 1.5),
                        Vector(0, 90, 0),
                        Vector(0.39, 0.39, 0.39),
                        fence_model,
                        static=True
                    )
                elif (i == WORLD_WIDTH - 1):
                    new_fence = Object(
                        Vector(i * self.plane_scale - 0.8, 0, k * self.plane_scale - 1.5),
                        Vector(0, 90, 0),
                        Vector(0.39, 0.39, 0.39),
                        fence_model,
                        static=True
                    )
                self.fence_array.append(new_fence)

                self.floor_tile_array.append(new_floor_tile)

    def generate_grass(self, grass_patch_model):
        for i in range(self.grass_amount):
            # change positions here

            random_coordinates = random.sample(range(0, self.map_size), 2)
            new_grass = Object(Vector(random_coordinates[0], 0, random_coordinates[1]),
                               Vector(0, 0, 0),
                               Vector(5, 5, 5),
                               grass_patch_model,
                               static=True)
            self.grass_array.append(new_grass)

    def generate_fences(self,fence_model):
        pass

    def draw(self, shader):
        for tile in self.floor_tile_array:
            tile.draw(shader)

        for fence in self.fence_array:
            fence.draw(shader)

        for grass in self.grass_array:
            grass.draw(shader)



