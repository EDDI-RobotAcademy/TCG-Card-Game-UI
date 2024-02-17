import math

from opengl_shape.oval import Oval
from opengl_shape.shape import Shape
from OpenGL import GL

import tkinter
import unittest

from OpenGL.GL import *
from OpenGL.GLU import *
from pyopengltk import OpenGLFrame

from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage
from opengl_shape.rectangle import Rectangle


class ImageOvalElementRefactor(Shape):
    def __init__(self, image_data, center, radius_x, radius_y, global_translation=(0, 0), local_translation=(0, 0)):
        super().__init__([center], global_translation, local_translation)
        self.radius_x = radius_x
        self.radius_y = radius_y
        self.center = center
        self.image_data = image_data
        self.is_visible = True
        self.texture_id = None

    def set_visible(self, visible):
        self.is_visible = visible

    def get_visible(self):
        return self.is_visible

    def draw(self):
        if self.get_visible():
            white_oval = Oval(color=(1.0, 1.0, 1.0, 1.0),
                              center=self.center,
                              radius_x=self.radius_x,
                              radius_y=self.radius_y,
                              local_translation=self.local_translation,
                              global_translation=self.global_translation)
            white_oval.draw()

            image_info = self.image_data

            if image_info is not None:
                width, height, image_data = image_info

                if self.texture_id is None:
                    self.texture_id = glGenTextures(1)
                    glBindTexture(GL.GL_TEXTURE_2D, self.texture_id)
                    glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGB, width, height, 0, GL.GL_RGB, GL.GL_UNSIGNED_BYTE,
                                 image_data)
                    glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR)
                    glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)

                GL.glEnable(GL.GL_TEXTURE_2D)
                GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture_id)

                glBegin(GL_TRIANGLE_FAN)
                glColor3f(1.0, 1.0, 1.0)

                for i in range(361):
                    angle = i * math.pi / 180.0
                    x = self.radius_x * math.cos(angle) + self.center[0] + self.global_translation[0] + \
                        self.local_translation[0] - 1
                    y = self.radius_y * math.sin(angle) + self.center[1] + self.global_translation[1] + \
                        self.local_translation[1] - 1
                    glTexCoord2f(0.5 + 0.5 * math.cos(angle), 0.5 + 0.5 * math.sin(angle))
                    glVertex2f(x, y)

                glEnd()
                GL.glDisable(GL.GL_TEXTURE_2D)


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


class OpponentHandPanel:
    __pre_drawed_image_instance = PreDrawedImage.getInstance()

    def __init__(self, local_translation=(0, 0), scale=1):
        self.pre_drawed_your_hand = None
        self.shapes = []
        self.local_translation = local_translation
        self.scale = scale

        self.pickable_card_list = []

    def change_local_translation(self, _translation):
        self.local_translation = _translation

    def get_opponent_hand_panel_shapes(self):
        return self.shapes

    def get_pickable_card_list(self):
        return self.pickable_card_list

    def add_shape(self, shape):
        shape.local_translate(self.local_translation)
        self.shapes.append(shape)

    def create_hand_panel(self, image_data, vertices):
        hand_panel = ImageRectangleElementRefactor(image_data=image_data,
                                                   vertices=vertices)
        self.add_shape(hand_panel)

    def init_shapes(self):
        self.__pre_drawed_image_instance.pre_draw_opponent_hand_panel()

        self.create_hand_panel(image_data=self.__pre_drawed_image_instance.get_pre_draw_opponent_hand_panel(),
                               vertices=[(300, 100), (1600, 100), (1600, 250), (300, 250)])


class OpponentUnitField:
    __pre_drawed_image_instance = PreDrawedImage.getInstance()

    def __init__(self, local_translation=(0, 0), scale=1):
        self.pre_drawed_your_hand = None
        self.shapes = []
        self.local_translation = local_translation
        self.scale = scale

        self.pickable_card_list = []

    def change_local_translation(self, _translation):
        self.local_translation = _translation

    def get_opponent_unit_field_shapes(self):
        return self.shapes

    def get_pickable_card_list(self):
        return self.pickable_card_list

    def add_shape(self, shape):
        shape.local_translate(self.local_translation)
        self.shapes.append(shape)

    def create_unit_field(self, image_data, vertices):
        unit_field = ImageRectangleElementRefactor(image_data=image_data,
                                                   vertices=vertices)
        self.add_shape(unit_field)

    def init_shapes(self):
        self.__pre_drawed_image_instance.pre_draw_opponent_unit_field()

        self.create_unit_field(image_data=self.__pre_drawed_image_instance.get_pre_draw_opponent_unit_field(),
                               vertices=[(300, 350), (1600, 350), (1600, 500), (300, 500)])


class YourHandPanel:
    __pre_drawed_image_instance = PreDrawedImage.getInstance()

    def __init__(self, local_translation=(0, 0), scale=1):
        self.pre_drawed_your_hand = None
        self.shapes = []
        self.local_translation = local_translation
        self.scale = scale

        self.pickable_card_list = []

    def change_local_translation(self, _translation):
        self.local_translation = _translation

    def get_your_hand_panel_shapes(self):
        return self.shapes

    def get_pickable_card_list(self):
        return self.pickable_card_list

    def add_shape(self, shape):
        shape.local_translate(self.local_translation)
        self.shapes.append(shape)

    def create_hand_panel(self, image_data, vertices):
        hand_panel = ImageRectangleElementRefactor(image_data=image_data,
                                                   vertices=vertices)
        self.add_shape(hand_panel)

    def init_shapes(self):
        self.__pre_drawed_image_instance.pre_draw_your_hand_panel()

        self.create_hand_panel(image_data=self.__pre_drawed_image_instance.get_pre_draw_your_hand_panel(),
                               vertices=[(300, 830), (1600, 830), (1600, 980), (300, 980)])


class YourUnitField:
    __pre_drawed_image_instance = PreDrawedImage.getInstance()

    def __init__(self, local_translation=(0, 0), scale=1):
        self.pre_drawed_your_hand = None
        self.shapes = []
        self.local_translation = local_translation
        self.scale = scale

        self.pickable_card_list = []

    def change_local_translation(self, _translation):
        self.local_translation = _translation

    def get_your_unit_field_shapes(self):
        return self.shapes

    def get_pickable_card_list(self):
        return self.pickable_card_list

    def add_shape(self, shape):
        shape.local_translate(self.local_translation)
        self.shapes.append(shape)

    def create_unit_field(self, image_data, vertices):
        unit_field = ImageRectangleElementRefactor(image_data=image_data,
                                                   vertices=vertices)
        self.add_shape(unit_field)

    def init_shapes(self):
        self.__pre_drawed_image_instance.pre_draw_your_unit_field()
        # (300, 800), (1600, 800), (1600, 950), (300, 950)
        self.create_unit_field(image_data=self.__pre_drawed_image_instance.get_pre_draw_your_unit_field(),
                               vertices=[(300, 580), (1600, 580), (1600, 730), (300, 730)])


class PreDrawedBattleFieldFrameRefactor(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.width = screen_width
        self.height = screen_height

        self.opponent_hand_panel = OpponentHandPanel()
        self.opponent_hand_panel.init_shapes()
        self.opponent_hand_panel_shapes = self.opponent_hand_panel.get_opponent_hand_panel_shapes()

        self.opponent_unit_field = OpponentUnitField()
        self.opponent_unit_field.init_shapes()
        self.opponent_unit_field_shapes = self.opponent_unit_field.get_opponent_unit_field_shapes()

        self.your_hand_panel = YourHandPanel()
        self.your_hand_panel.init_shapes()
        self.your_hand_panel_shapes = self.your_hand_panel.get_your_hand_panel_shapes()

        self.your_unit_field = YourUnitField()
        self.your_unit_field.init_shapes()
        self.your_unit_field_shapes = self.your_unit_field.get_your_unit_field_shapes()

        self.bind("<Configure>", self.on_resize)

    # def initgl(self):
    #     glClearColor(1.0, 1.0, 1.0, 0.0)
    #     glOrtho(0, self.width, self.height, 0, -1, 1)

    def initgl(self):
        glClearColor(1.0, 1.0, 1.0, 0.0)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, self.width, self.height, 0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def reshape(self, width, height):
        print(f"Reshaping window to width={width}, height={height}")
        self.width = width
        self.height = height
        aspect_ratio = width / height

        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        if aspect_ratio > 1.0:
            gluOrtho2D(0, width, height / aspect_ratio, 0)
        else:
            gluOrtho2D(0, width * aspect_ratio, height, 0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def on_resize(self, event):
        print("Handling resize event")
        self.reshape(event.width, event.height)

    def redraw(self):
        self.tkMakeCurrent()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        for opponent_hand_panel_shape in self.opponent_hand_panel_shapes:
            opponent_hand_panel_shape.draw()

        for opponent_unit_field_shape in self.opponent_unit_field_shapes:
            opponent_unit_field_shape.draw()

        for your_hand_panel_shape in self.your_hand_panel_shapes:
            your_hand_panel_shape.draw()

        for your_unit_field_shape in self.your_unit_field_shapes:
            your_unit_field_shape.draw()

        self.tkSwapBuffers()



class TestRatioBasedDraw(unittest.TestCase):

    def test_ratio_based_draw(self):
        root = tkinter.Tk()
        root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}-0-0")
        root.deiconify()

        pre_drawed_battle_field_frame = PreDrawedBattleFieldFrameRefactor(root)
        pre_drawed_battle_field_frame.pack(fill=tkinter.BOTH, expand=1)
        root.update_idletasks()

        def animate():
            pre_drawed_battle_field_frame.redraw()
            # root.after(17, animate)
            root.after(33, animate)

        root.after(0, animate)

        root.mainloop()


if __name__ == '__main__':
    unittest.main()
