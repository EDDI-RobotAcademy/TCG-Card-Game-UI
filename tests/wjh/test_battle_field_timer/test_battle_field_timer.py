import tkinter as tk
import unittest

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from pyopengltk import OpenGLFrame

from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage
from opengl_shape.image_circle_element import ImageCircleElement

class battleFieldTimer(OpenGLFrame):
    __preDrawedImage = PreDrawedImage.getInstance()
    def __init__(self, local_translation=(0, 0)):
        super().__init__()
        self.timer = 5
        self.local_translation = local_translation

    def initgl(self):

        glClearColor(0.0, 0.0, 0.0, 0.0)
        gluOrtho2D(-1.0, 1.0, -1.0, 1.0)

    def redraw(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glColor3f(1.0, 1.0, 1.0)

        timer_image_position = (
            self.local_translation[0] - 0.5,  # x 좌표
            self.local_translation[1] + 0.5  # y 좌표
        )

        self.render_number(self.timer, timer_image_position)
        self.update_timer()
        if self.timer >= -1:
            self.after(1000, self.redraw)

    def render_number(self, timer, local_translation):
        # imagedata = self.__preDrawedImage.get_pre_draw_character_hp_image(number=timer)
        # ImageCircleElement(image_path=imagedata, center=(local_translation), radius=100)
        print(timer)

    def update_timer(self):
        self.timer -= 1
        if self.timer == -1:
            print("턴 종료 해줘")






class TestBattleFieldTimer(unittest.TestCase):

    def test_time_frame(self):
        root = tk.Tk()
        root.title("TestTimer")
        root.geometry("1920x1080")
        root.configure(background="#151515")
        app = battleFieldTimer()
        app.pack(fill=tk.BOTH, expand=tk.YES)
        root.mainloop()



if __name__ == '__main__':
    unittest.main()

        #
        # ljs/test_notify_function/test_motify_opponent_unit_spawn참고
        # def animate():
        #     pre_drawed_battle_field_frame.redraw()
        #     root.after(17, animate)
        #
        # root.after(0, animate)
        #
        # root.mainloop()
