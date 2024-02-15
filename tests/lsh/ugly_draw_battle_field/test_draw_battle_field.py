from opengl_shape.shape import Shape
from OpenGL import GL

import tkinter
import unittest

from OpenGL.GL import *
from OpenGL.GLU import *
from pyopengltk import OpenGLFrame

from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage
from opengl_shape.rectangle import Rectangle


class ImageRectangleElementRefactor(Shape):
    def __init__(self, image_data, vertices, global_translation=(0, 0), local_translation=(0, 0)):
        super().__init__(vertices, global_translation, local_translation)
        self.image_data = image_data
        self.is_visible = True

    def set_visible(self, visible):
        self.is_visible = visible

    def get_visible(self):
        return self.is_visible

    def draw(self):
        if self.get_visible():
            white_rect = Rectangle(color=(1.0, 1.0, 1.0, 1.0),
                                   vertices=self.vertices,
                                   global_translation=self.global_translation,
                                   local_translation=self.local_translation)
            white_rect.draw()

            image_data = self.image_data
            texture_ids = GL.glGenTextures(1)

            GL.glBindTexture(GL.GL_TEXTURE_2D, texture_ids)
            GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
            GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
            GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGBA, image_data.shape[1], image_data.shape[0],
                            0, GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, image_data)

            GL.glEnable(GL.GL_TEXTURE_2D)
            GL.glBindTexture(GL.GL_TEXTURE_2D, texture_ids)

            GL.glBegin(GL.GL_QUADS)
            GL.glTexCoord2f(0, 0)

            GL.glVertex2f(self.vertices[0][0] + self.local_translation[0] + self.global_translation[0],
                          self.vertices[0][1] + self.local_translation[1] + self.global_translation[1])

            GL.glTexCoord2f(1, 0)
            GL.glVertex2f(self.vertices[1][0] + self.local_translation[0] + self.global_translation[0],
                          self.vertices[1][1] + self.local_translation[1] + self.global_translation[1])

            GL.glTexCoord2f(1, 1)
            GL.glVertex2f(self.vertices[2][0] + self.local_translation[0] + self.global_translation[0],
                          self.vertices[2][1] + self.local_translation[1] + self.global_translation[1])

            GL.glTexCoord2f(0, 1)
            GL.glVertex2f(self.vertices[3][0] + self.local_translation[0] + self.global_translation[0],
                          self.vertices[3][1] + self.local_translation[1] + self.global_translation[1])
            GL.glEnd()

            GL.glDisable(GL.GL_TEXTURE_2D)


class Tomb:
    __pre_drawed_image_instance = PreDrawedImage.getInstance()

    def __init__(self, local_translation=(0, 0), scale=1):
        self.pre_drawed_tomb = None
        self.shapes = []
        self.local_translation = local_translation
        self.scale = scale

    def get_tomb_shapes(self):
        return self.shapes

    def change_local_translation(self, _translation):
        self.local_translation = _translation

    def add_shape(self, shape):
        shape.local_translate(self.local_translation)
        self.shapes.append(shape)

    def create_tomb(self, image_data, vertices):
        tomb_illustration = ImageRectangleElementRefactor(image_data=image_data,
                                                          vertices=vertices)
        self.add_shape(tomb_illustration)

    def init_shapes(self):
        self.__pre_drawed_image_instance.pre_draw_tomb()

        self.create_tomb(image_data=self.__pre_drawed_image_instance.get_pre_draw_tomb(),
                         vertices=[(50, 50), (200, 50), (200, 250), (50, 250)])


class LostZone:
    __pre_drawed_image_instance = PreDrawedImage.getInstance()

    def __init__(self, local_translation=(0, 0), scale=1):
        self.pre_drawed_lost_zone = None
        self.shapes = []
        self.local_translation = local_translation
        self.scale = scale

    def get_lost_zone_shapes(self):
        return self.shapes

    def change_local_translation(self, _translation):
        self.local_translation = _translation

    def add_shape(self, shape):
        shape.local_translate(self.local_translation)
        self.shapes.append(shape)

    def create_lost_zone(self, image_data, vertices):
        lost_zone_illustration = ImageRectangleElementRefactor(image_data=image_data,
                                                               vertices=vertices)
        self.add_shape(lost_zone_illustration)

    def init_shapes(self):
        self.__pre_drawed_image_instance.pre_draw_lost_zone()

        self.create_lost_zone(image_data=self.__pre_drawed_image_instance.get_pre_draw_lost_zone(),
                              vertices=[(1670, 290), (1870, 290), (1870, 490), (1670, 490)])


class Trap:
    __pre_drawed_image_instance = PreDrawedImage.getInstance()

    def __init__(self, local_translation=(0, 0), scale=1):
        self.pre_drawed_trap = None
        self.shapes = []
        self.local_translation = local_translation
        self.scale = scale

    def get_trap_shapes(self):
        return self.shapes

    def change_local_translation(self, _translation):
        self.local_translation = _translation

    def add_shape(self, shape):
        shape.local_translate(self.local_translation)
        self.shapes.append(shape)

    def create_trap(self, image_data, vertices):
        trap_illustration = ImageRectangleElementRefactor(image_data=image_data,
                                                          vertices=vertices)
        self.add_shape(trap_illustration)

    def init_shapes(self):
        self.__pre_drawed_image_instance.pre_draw_trap()

        self.create_trap(image_data=self.__pre_drawed_image_instance.get_pre_draw_trap(),
                         vertices=[(1400, 200), (1600, 200), (1600, 400), (1400, 400)])


class PreDrawedBattleFieldFrameRefactor(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.width = screen_width
        self.height = screen_height

        self.tomb = Tomb()
        self.tomb.init_shapes()
        self.tomb_shapes = self.tomb.get_tomb_shapes()

        self.lost_zone = LostZone()
        self.lost_zone.init_shapes()
        self.lost_zone_shapes = self.lost_zone.get_lost_zone_shapes()

        self.trap = Trap()
        self.trap.init_shapes()
        self.trap_shapes = self.trap.get_trap_shapes()

        self.bind("<Configure>", self.on_resize)

    def initgl(self):
        glClearColor(1.0, 1.0, 1.0, 0.0)
        glOrtho(0, self.width, self.height, 0, -1, 1)

    def reshape(self, width, height):
        print(f"Reshaping window to width={width}, height={height}")
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, width, height, 0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def on_resize(self, event):
        print("Handling resize event")
        self.reshape(event.width, event.height)

    def redraw(self):
        self.tkMakeCurrent()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        for tomb_shape in self.tomb_shapes:
            tomb_shape.draw()

        for lost_zone_shape in self.lost_zone_shapes:
            lost_zone_shape.draw()

        for trap_shape in self.trap_shapes:
            trap_shape.draw()

        self.tkSwapBuffers()



class TestPreDrawedImage(unittest.TestCase):

    def test_pre_drawed_image_refactor(self):
        root = tkinter.Tk()
        root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}-0-0")
        root.deiconify()

        pre_drawed_battle_field_frame = PreDrawedBattleFieldFrameRefactor(root)
        pre_drawed_battle_field_frame.pack(fill=tkinter.BOTH, expand=1)
        root.update_idletasks()

        def animate():
            pre_drawed_battle_field_frame.redraw()
            root.after(17, animate)

        root.after(0, animate)

        root.mainloop()


if __name__ == '__main__':
    unittest.main()