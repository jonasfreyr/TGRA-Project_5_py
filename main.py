
# from OpenGL.GL import *
# from OpenGL.GLU import *

import pygame
from pygame.locals import *

from Shaders import *
from Core.Matrices import *

class GraphicsProgram3D:
    def __init__(self):

        pygame.init()
        pygame.display.set_mode((800 ,600), pygame.OPENGL |pygame.DOUBLEBUF)

        self.shader = Shader3D()
        self.shader.use()

        self.model_matrix = ModelMatrix()

        # self.projection_view_matrix = ProjectionViewMatrix()
        # self.shader.set_projection_view_matrix(self.projection_view_matrix.get_matrix())

        self.view_matrix = ViewMatrix()
        self.projection_matrix = ProjectionMatrix()

        self.projection_matrix.set_perspective(90, 16/9, 1, 100)

        self.shader.set_view_matrix(self.view_matrix.get_matrix())
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())

        self.cube = Cube()
        self.sphere = Sphere(12,24)

        self.clock = pygame.time.Clock()
        self.clock.tick()

        self.angle = 0

        self.UP_key_down = False  ## --- ADD CONTROLS FOR OTHER KEYS TO CONTROL THE CAMERA --- ##
        self.DOWN_key_down = False
        self.LEFT_key_down = False
        self.RIGHT_key_down = False

        self.W_key_down = False  ## --- ADD CONTROLS FOR OTHER KEYS TO CONTROL THE CAMERA --- ##
        self.S_key_down = False
        self.A_key_down = False
        self.D_key_down = False

        self.K_q = False
        self.K_e = False
        self.K_r = False
        self.K_f = False

        self.white_background = False

        self.rotation = 0

        self.tex_id_cock = self.load_texture("Textures/test.png")
        self.tex_id_vag = self.load_texture("Textures/test2.png")
        self.tex_id_tits = self.load_texture("Textures/test3.png")
        self.tex_id_aids = self.load_texture("Textures/test4.png")

    def load_texture(self, path):
        surface = pygame.image.load(path)
        tex_string = pygame.image.tostring(surface, "RGBA", True)
        width = surface.get_width()
        height = surface.get_height()
        tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, tex_string)

        return tex_id

    def update(self):
        delta_time = self.clock.tick() / 1000.0

        if self.UP_key_down:
            self.view_matrix.pitch(100 * delta_time)
        elif self.DOWN_key_down:
            self.view_matrix.pitch(-100 * delta_time)
        if self.LEFT_key_down:
            self.view_matrix.yaw(-100 * delta_time)
        elif self.RIGHT_key_down:
            self.view_matrix.yaw(100 * delta_time)

        if self.W_key_down:
            self.view_matrix.slide(0, 0, -1 * delta_time)
        elif self.S_key_down:
            self.view_matrix.slide(0, 0, 1 * delta_time)
        if self.A_key_down:
            self.view_matrix.slide(-1 * delta_time, 0, 0)
        elif self.D_key_down:
            self.view_matrix.slide(1 * delta_time, 0, 0)

        if self.K_q:
            self.view_matrix.roll(100 * delta_time)
        elif self.K_e:
            self.view_matrix.roll(-100 * delta_time)

        if self.K_r:
            self.view_matrix.slide(0, 1 * delta_time, 0)
        elif self.K_f:
            self.view_matrix.slide(0, -1 * delta_time, 0)

        self.rotation += 100 * delta_time

    def pyramid(self):
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(0, -3, 0)
        self.model_matrix.add_scale(10, 0.1, 10)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.shader.set_material_diffuse(1, 0, 0)
        self.shader.set_material_specular(1, 1, 1)
        self.shader.set_material_ambient(.1, 0, 0)
        self.shader.set_shininess(10)

        self.cube.draw()
        self.model_matrix.pop_matrix()

        self.model_matrix.push_matrix()

        self.model_matrix.add_translation(0, 2, 0)

        level_colors = [(1, 1, 1),
                        (0, 1, 1),
                        (1, 0, 1),
                        (1, 1, 0),
                        (0, 0, 1)]

        cube_amount = 5
        self.model_matrix.add_rotation(self.rotation, 0, 0)
        for level in range(cube_amount):
            for cube in range(level +1):
                self.model_matrix.push_matrix()
                self.model_matrix.add_translation(cube, -level, 0)
                self.shader.set_model_matrix(self.model_matrix.matrix)
                self.shader.set_material_diffuse(*level_colors[level])

                amcol = list(map(lambda x: x/10, level_colors[level]))
                self.shader.set_material_specular(*level_colors[level])
                self.shader.set_material_ambient(*amcol)
                self.shader.set_shininess(3)
                self.cube.draw()
                self.model_matrix.pop_matrix()

            self.model_matrix.add_translation(-0.5, 0, 0)

        self.model_matrix.pop_matrix()

    def draw_cube_objects(self):
        self.cube.set_vertices(self.shader)

        # self.shader.set_texture_diffuse(self.tex_id)

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_cock)
        self.shader.set_texture_diffuse(0)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_aids)
        self.shader.set_texture_specular(1)


        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(0, 0, -3)
        self.model_matrix.add_scale(1, 1, 1)
        self.model_matrix.add_rotation(self.rotation, self.rotation, 0)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.shader.set_material_diffuse(1, 1, 1)
        self.shader.set_material_specular(1, 1, 1)
        self.shader.set_material_ambient(0.1, 0.1, 0.1)
        self.shader.set_shininess(10)
        self.cube.draw()
        self.model_matrix.pop_matrix()

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_vag)
        self.shader.set_texture_diffuse(0)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.tex_id_tits)
        self.shader.set_texture_specular(1)

        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(0, 3, -3)
        self.model_matrix.add_scale(1, 1, 1)
        self.model_matrix.add_rotation(self.rotation, self.rotation, 0)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.shader.set_material_diffuse(1, 1, 1)
        self.shader.set_material_specular(1, 1, 1)
        self.shader.set_material_ambient(0.1, 0.1, 0.1)
        self.shader.set_shininess(10)
        self.cube.draw()
        self.model_matrix.pop_matrix()

        # self.pyramid()

    def draw_rotating_spheres(self):
        for i in range(8):
            self.model_matrix.push_matrix()
            self.model_matrix.add_rotation(self.rotation * 0.73 +i * pi/4.0, 0, 0)
            self.model_matrix.add_translation(0,5,0)
            self.model_matrix.add_rotation(-(self.rotation *0.73 +i * pi/4.0), 0, 0)
            self.model_matrix.add_scale(3.0,3.0,3.0)
            self.shader.set_model_matrix(self.model_matrix.matrix)

            self.shader.set_material_diffuse(1.0,1.0,1.0)
            self.sphere.draw(self.shader)
            self.model_matrix.pop_matrix()

    def draw_sphere_objects(self):
        self.sphere.set_vertices(self.shader)

        self.model_matrix.push_matrix()
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.shader.set_material_diffuse(1, 1, 0)
        self.shader.set_material_specular(1, 1, 1)
        self.shader.set_material_ambient(.1, .1, 0)
        self.shader.set_shininess(50)

        self.sphere.draw(self.shader)
        
        self.model_matrix.pop_matrix()

        self.draw_rotating_spheres()

    def display(self):
        glEnable(
            GL_DEPTH_TEST)  ### --- NEED THIS FOR NORMAL 3D BUT MANY EFFECTS BETTER WITH glDisable(GL_DEPTH_TEST) ... try it! --- ###

        if self.white_background:
            glClearColor(1.0, 1.0, 1.0, 1.0)
        else:
            glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(
            GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  ### --- YOU CAN ALSO CLEAR ONLY THE COLOR OR ONLY THE DEPTH --- ###

        glViewport(0, 0, 800, 600)

        self.shader.set_view_matrix(self.view_matrix.get_matrix())

        self.shader.set_camera_position(self.view_matrix.eye.x, self.view_matrix.eye.y, self.view_matrix.eye.z)

        self.shader.set_light_position(0, 0, 0, 0)
        self.shader.set_light_diffuse(1, 1, 1, 0)
        self.shader.set_light_specular(1, 1, 1, 0)
        self.shader.set_light_ambient(0.5, 0.5, 0.5, 0)

        self.shader.set_light_amount(1)

        self.draw_cube_objects()
        # self.draw_sphere_objects()

        pygame.display.flip()

    def program_loop(self):
        exiting = False
        while not exiting:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Quitting!")
                    exiting = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        print("Escaping!")
                        exiting = True

                    if event.key == K_UP:
                        self.UP_key_down = True
                    elif event.key == K_DOWN:
                        self.DOWN_key_down = True
                    elif event.key == K_LEFT:
                        self.LEFT_key_down = True
                    elif event.key == K_RIGHT:
                        self.RIGHT_key_down = True
                    elif event.key == K_w:
                        self.W_key_down = True  ## --- ADD CONTROLS FOR OTHER KEYS TO CONTROL THE CAMERA --- ##
                    elif event.key == K_s:
                        self.S_key_down = True
                    elif event.key == K_a:
                        self.A_key_down = True
                    elif event.key == K_d:
                        self.D_key_down = True
                    elif event.key == K_q:
                        self.K_q = True
                    elif event.key == K_e:
                        self.K_e = True
                    elif event.key == K_r:
                        self.K_r = True
                    elif event.key == K_f:
                        self.K_f = True

                elif event.type == pygame.KEYUP:
                    if event.key == K_UP:
                        self.UP_key_down = False
                    elif event.key == K_DOWN:
                        self.DOWN_key_down = False
                    elif event.key == K_LEFT:
                        self.LEFT_key_down = False
                    elif event.key == K_RIGHT:
                        self.RIGHT_key_down = False
                    elif event.key == K_w:
                        self.W_key_down = False  ## --- ADD CONTROLS FOR OTHER KEYS TO CONTROL THE CAMERA --- ##
                    elif event.key == K_s:
                        self.S_key_down = False
                    elif event.key == K_a:
                        self.A_key_down = False
                    elif event.key == K_d:
                        self.D_key_down = False
                    elif event.key == K_q:
                        self.K_q = False
                    elif event.key == K_e:
                        self.K_e = False
                    elif event.key == K_r:
                        self.K_r = False
                    elif event.key == K_f:
                        self.K_f = False

            self.update()
            self.display()

        # OUT OF GAME LOOP
        pygame.quit()

    def start(self):
        self.program_loop()


if __name__ == "__main__":
    GraphicsProgram3D().start()