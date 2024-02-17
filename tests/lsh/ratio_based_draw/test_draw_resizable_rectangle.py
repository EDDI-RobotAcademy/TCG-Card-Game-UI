from OpenGL import GL

import tkinter
import unittest

from OpenGL.GL import *
from OpenGL.GLU import *
from pyopengltk import OpenGLFrame

class ResizableRectangle(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.width = self.winfo_screenwidth()
        self.height = self.winfo_screenheight()

        self.bind("<Configure>", self.on_resize)

    def initgl(self):
        glClearColor(1.0, 1.0, 1.0, 1.0)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, self.width, self.height, 0)

        # aspect_ratio = self.width / self.height
        #
        # if self.width > self.height:
        #     gluOrtho2D(0, self.width, self.height / aspect_ratio, 0)
        # else:
        #     gluOrtho2D(0, self.width * aspect_ratio, self.height, 0)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def draw_rectangle2(self):
        glColor3f(0.0, 1.0, 0.0)

        # glBegin(GL_QUADS)
        # glVertex2f(100, 100)
        # glVertex2f(400, 100)
        # glVertex2f(400, 400)
        # glVertex2f(100, 400)
        # glEnd()

        # x = 1848, y = 1016 => x = 1386, y = 752
        # convert x = 100 / 1848 * 1386 => 75.065
        # convert y = 100 / 1016 * 752 => 74.015

        # aspect_ratio = self.width / self.height
        # rectangle_width = min(self.width, self.height) / 2
        # rectangle_height = rectangle_width / aspect_ratio

        # (100, 100) (400, 400)
        # 1848 / 1016 first ratio
        # 1386 / 752  second ratio

        # 1500 / 1000 first ratio
        # 1000 / 500  second ratio

        # 100 * 500 / 1000 => 50
        # 400 * 500 / 1000 => 200
        # (100, 100), (100, 400), (400, 400), (400, 100) => x length = 300, y length = 300
        # 1500 : 300 = 5 : 1
        # (50, 50),   (50, 200),  (200, 200), (200, 50)  => x_length = 150, y length = 150
        # 1000: 150 = 6.67 : 1


        x_center = self.width / 2
        y_center = self.height / 2

        print(f"current total x = {self.width}")
        print(f"current total y = {self.height}")

        # # origin x coordinate / origin_total_width * changed_total_width
        # print(f"convert x = 100 / 1848 * 1386 = {100 / 1848 * 1386}")
        # # origin y coordinate / origin_total_height * changed_total_height
        # print(f"convert y = 100 / 1016 * 752 = {100 / 1016 * 752}")
        #
        # # origin x coordinate / origin_total_width * changed_total_width
        # print(f"convert x = 400 / 1848 * 1386 = {400 / 1848 * 1386}")
        # # origin y coordinate / origin_total_height * changed_total_height
        # print(f"convert y = 400 / 1016 * 752 = {400 / 1016 * 752}")

        print(f"convert x = 100 / 1848 * 1386 = {100 / 1848 * 1386}")
        # origin y coordinate / origin_total_height * changed_total_height
        print(f"convert y = 100 / 1016 * 752 = {100 / 1016 * 752}")

        # origin x coordinate / origin_total_width * changed_total_width
        print(f"convert x = 400 / 1848 * 1386 = {400 / 1848 * 1386}")
        # origin y coordinate / origin_total_height * changed_total_height
        print(f"convert y = 400 / 1016 * 752 = {400 / 1016 * 752}")

        glBegin(GL_QUADS)
        glVertex2f(100 / 1848 * 1386, 100 / 1016 * 752)
        glVertex2f(400 / 1848 * 1386, 100 / 1016 * 752)
        glVertex2f(400 / 1848 * 1386, 400 / 1016 * 752)
        glVertex2f(100 / 1848 * 1386, 400 / 1016 * 752)
        glEnd()

    # def draw_rectangle(self):
    #     glColor3f(0.0, 1.0, 0.0)
    #
    #     aspect_ratio = self.width / self.height
    #
    #     original_coordinates = [(100, 100), (400, 100), (400, 400), (100, 400)]
    #
    #     if self.width < 1848:
    #         adjusted_coordinates = []
    #         for x, y in original_coordinates:
    #             adjusted_x = x / 1920 * self.width
    #             adjusted_y = y / 1080 * self.height
    #             adjusted_coordinates.append((adjusted_x, adjusted_y))
    #     else:
    #         adjusted_coordinates = original_coordinates
    #
    #     glBegin(GL_QUADS)
    #     for x, y in adjusted_coordinates:
    #         glVertex2f(x, y)
    #     glEnd()

    def draw_rectangle(self):
        glColor3f(0.0, 1.0, 0.0)

        aspect_ratio = self.width / self.height

        original_coordinates = [(100, 100), (400, 100), (400, 400), (100, 400)]

        adjusted_coordinates = [(x / 1920 * self.width, y / 1080 * self.height) for x, y in original_coordinates]

        glBegin(GL_QUADS)
        for x, y in adjusted_coordinates:
            glVertex2f(x, y)
        glEnd()

    def reshape(self, width, height):
        print(f"Reshaping window to width={width}, height={height}")
        self.width = width
        self.height = height
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        gluOrtho2D(0, width, height, 0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()



    def on_resize(self, event):
        print("Handling resize event")
        self.reshape(event.width, event.height)
        self.redraw()

    def redraw(self):
        self.tkMakeCurrent()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.draw_rectangle()

        self.tkSwapBuffers()

class TestResizableRectangle(unittest.TestCase):
    def test_resizable_rectangle(self):
        root = tkinter.Tk()
        root.geometry(f"{1920}x{1080}-0-0")
        root.deiconify()

        resizable_rectangle = ResizableRectangle(root)
        resizable_rectangle.pack(fill=tkinter.BOTH, expand=1)

        def animate():
            resizable_rectangle.redraw()
            root.after(33, animate)

        root.after(0, animate)

        root.mainloop()

if __name__ == '__main__':
    unittest.main()
