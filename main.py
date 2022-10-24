
# from OpenGL.GL import *
# from OpenGL.GLU import *

import pygame
from pygame.locals import *

from collections import defaultdict

from Game.Level import Level
from Game.Object import Teeth, RotatingCube, Object
from Game.Player import FlyingPlayer, Player
from OpenGLCore.Shaders import *
from Core.Matrices import *
from OpenGLCore import ojb_3D_loading
from Core.Constants import *
from Core.Color import Color


class GraphicsProgram3D:
    def __init__(self):

        pygame.init()
        pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF)

        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)

        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_BLEND)

        self.shader = Shader3D()
        self.shader.use()

        self.model_matrix = ModelMatrix()

        # self.projection_view_matrix = ProjectionViewMatrix()
        # self.shader.set_projection_view_matrix(self.projection_view_matrix.get_matrix())

        self.player = Player(Vector(0, 0, 0), 1, 1)
        # self.player = FlyingPlayer(Vector(0, 0, 0), 1, 1)
        self.shader.set_projection_matrix(self.player.projection_matrix.get_matrix())

        self.player.draw(self.shader)

        self.clock = pygame.time.Clock()
        self.clock.tick()

        self.angle = 0

        self.keys = defaultdict(lambda: False)

        self.teeth_object_model = ojb_3D_loading.load_obj_file(MODELS_PATH, "mouth.obj")
        self.grass_object_model = ojb_3D_loading.load_obj_file(MODELS_PATH, "grass_with_texture.obj")
        self.grass_patch_model = ojb_3D_loading.load_obj_file(MODELS_PATH, "grass_patch.obj")
        self.rock_model = ojb_3D_loading.load_obj_file(MODELS_PATH, "rock.obj")
        self.ground_model = ojb_3D_loading.load_obj_file(MODELS_PATH, "grass-plain.obj")
        self.rpg_model = ojb_3D_loading.load_obj_file(MODELS_PATH, "launcher.obj")

        self.tex_id_cock = ojb_3D_loading.load_texture(TEXTURES_PATH + "/test.png")
        self.tex_id_vag = ojb_3D_loading.load_texture(TEXTURES_PATH + "/test2.png")
        self.tex_id_tits = ojb_3D_loading.load_texture(TEXTURES_PATH + "/test3.png")
        self.tex_id_aids = ojb_3D_loading.load_texture(TEXTURES_PATH + "/test4.png")
        self.tex_id_phobos = ojb_3D_loading.load_texture(TEXTURES_PATH + "/phobos.png")
        self.tex_id_earth = ojb_3D_loading.load_texture(TEXTURES_PATH + "/earth.jpg")
        self.tex_id_earth_spec = ojb_3D_loading.load_texture(TEXTURES_PATH + "/earth_spec.png")

        self.fr_ticker = 0
        self.fr_sum = 0

    def init_objects(self):
        cube = Cube()
        self.cube = RotatingCube(Vector(-3, 0, -3), Vector(1, 1, 1), self.tex_id_cock, self.tex_id_aids, cube)

        self.sphere = Sphere(24, 48)

        # self.grass = [Object(Vector(0, 0, 0), Vector(0, 0, 0), Vector(1, 1, 1), self.grass_patch_model)]
        # self.ground = Object(Vector(0, 0, 0), Vector(0, 0, 0), Vector(10, 10, 10), self.ground_model)

        self.level = Level(self.grass_patch_model, self.ground_model)

        self.teeth = Teeth(Vector(-5, 0, 5), Vector(0, 0, 0), Vector(20, 20, 20), self.teeth_object_model)
        self.rock = Object(Vector(0, 0, 5), Vector(0, 0, 0), Vector(10, 10, 10), self.rock_model)
        self.rpg = Object(Vector(5, 0, 0), Vector(0, 0, 0), Vector(1, 1, 1), self.rpg_model)

    def update(self):
        delta_time = self.clock.tick() / 1000.0
        self.fr_sum += delta_time
        self.fr_ticker += 1
        if self.fr_sum > 1.0:
            print(self.fr_ticker / self.fr_sum)
            self.fr_sum = 0
            self.fr_ticker = 0

        self.cube.update(delta_time)
        self.teeth.update(delta_time)
        self.player.update(delta_time, self.keys)

        # pygame.mouse.set_pos((WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

    def draw_cube_objects(self):
        self.cube.draw(self.shader)

    def draw_rotating_spheres(self):
        for i in range(8):
            self.model_matrix.push_matrix()
            self.model_matrix.add_rotation(self.rotation * 0.73 + (i*100) * pi / 4.0, 0, 0)
            self.model_matrix.add_translation(0, 5, 0)
            self.model_matrix.add_scale(1.0, 1.0, 1.0)
            self.model_matrix.add_rotation(-(self.rotation * 0.73 + (i*100) * pi / 4.0), 0, 0)
            self.shader.set_model_matrix(self.model_matrix.matrix)

            self.shader.set_material_diffuse_color(Color(1.0, 1.0, 1.0))
            self.shader.set_material_ambient_color(Color(0.1, 0.1, 0.1))
            self.sphere.draw(self.shader)
            self.model_matrix.pop_matrix()

    def draw_models(self):
        self.level.draw(self.shader)
        self.teeth.draw(self.shader)
        self.rock.draw(self.shader)
        self.rpg.draw(self.shader)

    def draw_sphere_objects(self):
        self.shader.set_using_diffuse_texture(1.0)
        self.shader.set_using_specular_texture(1.0)

        self.model_matrix.push_matrix()
        self.model_matrix.add_scale(3, 3, 3)
        self.model_matrix.add_rotation(0, self.rotation * 0.2, 180)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.shader.set_material_diffuse_color(Color(1, 1, 1))
        self.shader.set_material_specular_color(Color(1, 1, 1))
        self.shader.set_material_ambient_color(Color(0, 0, 0))
        self.shader.set_shininess(50)

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_earth)
        self.shader.set_texture_diffuse(0)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_earth_spec)
        self.shader.set_texture_specular(1)

        self.sphere.draw(self.shader)
        self.model_matrix.pop_matrix()

        self.draw_rotating_spheres()

    def display(self):
        glEnable(GL_DEPTH_TEST)

        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)

        # self.shader.set_view_matrix(self.view_matrix.get_matrix())
        # self.shader.set_camera_position(self.view_matrix.eye.x, self.view_matrix.eye.y, self.view_matrix.eye.z)

        self.player.draw(self.shader)

        self.shader.set_light_position(*self.player.top_pos.to_array(), 0)
        self.shader.set_light_diffuse(1, 1, 1, 0)
        self.shader.set_light_specular(1, 1, 1, 0)
        self.shader.set_light_ambient(0.5, 0.5, 0.5, 0)
        self.shader.set_light_amount(1)

        self.draw_cube_objects()
        # self.draw_sphere_objects()
        self.draw_models()

        pygame.display.flip()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Quitting!")
                self.exiting = True
            elif event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    print("Escaping!")
                    self.exiting = True
                self.keys[event.key] = True

            elif event.type == pygame.KEYUP:
                self.keys[event.key] = False

    def program_loop(self):
        self.exiting = False
        self.init_objects()
        while not self.exiting:

            self.events()
            self.update()
            self.display()

        # OUT OF GAME LOOP
        pygame.quit()

    def start(self):
        self.program_loop()


if __name__ == "__main__":
    GraphicsProgram3D().start()