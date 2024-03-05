import tkinter as tk
import unittest

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from pyopengltk import OpenGLFrame

class battleFieldTimer(OpenGLFrame):
    def __init__(self):
        super().__init__()
        self.timer = 0

    def initgl(self):
        glClearColor(0.0, 0.0, 0.0, 0.0)
        gluOrtho2D(-1.0, 1.0, -1.0, 1.0)

    def redraw(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glColor3f(1.0, 1.0, 1.0)

        self.render_number(self.timer)
        self.after(1000, self.update_timer)

    def render_number(self, timer):

        pass

    def update_timer(self):
        self.timer -= 1
        #if self.timer == 0:  <-0 될 시 어떻게 할지






class TestBattleFieldTimer(unittest.TestCase):

    def test_time_frame(self):
        root = tk.Tk()
        root.title("TestTimer")
        root.geometry("1920x1080")
        root.configure(background="#151515")
        #app = battleFieldTimer(root)
        app.pack(fill=tk.BOTH, expand=tk.YES)
        app.animate = True
        app.after(0, app.initgl)
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
