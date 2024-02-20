import math
import random
import tkinter as tk
import unittest
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from pyopengltk import OpenGLFrame

class LightningSegment:
    def __init__(self, start, end, brightness=1.0):
        self.start = start
        self.end = end
        self.brightness = brightness

def average(point1, point2):
    return ((point1[0] + point2[0]) / 2, (point1[1] + point2[1]) / 2)

def normalize(vector):
    length = (vector[0]**2 + vector[1]**2)**0.5
    return (vector[0] / length, vector[1] / length)

def perpendicular(vector):
    return (-vector[1], vector[0])

def rotate(vector, angle):
    x = vector[0] * math.cos(angle) - vector[1] * math.sin(angle)
    y = vector[0] * math.sin(angle) + vector[1] * math.cos(angle)
    return (x, y)

def random_float(min_val, max_val):
    return random.uniform(min_val, max_val)

def generate_lightning(start_point, end_point, maximum_offset, num_generations, branch_probability, length_scale):
    segment_list = [LightningSegment(start_point, end_point)]
    offset_amount = maximum_offset

    for generation in range(num_generations):
        for segment in segment_list[:]:
            segment_list.remove(segment)

            mid_point = average(segment.start, segment.end)
            direction = normalize((segment.end[0] - segment.start[0], segment.end[1] - segment.start[1]))
            normal = perpendicular(direction)

            mid_point = (mid_point[0] + normal[0] * random_float(-offset_amount, offset_amount),
                         mid_point[1] + normal[1] * random_float(-offset_amount, offset_amount))

            segment_list.append(LightningSegment(segment.start, mid_point, segment.brightness))
            segment_list.append(LightningSegment(mid_point, segment.end, segment.brightness))

            if generation % 2 == 0 and random.random() < branch_probability:
                branch_direction = rotate(direction, random_float(-math.pi / 2, math.pi / 2))
                split_end = (mid_point[0] + branch_direction[0] * length_scale,
                             mid_point[1] + branch_direction[1] * length_scale)

                segment_list.append(LightningSegment(mid_point, split_end, segment.brightness * 0.5))

        offset_amount /= 2

    return segment_list

class RectDrawingApp(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.inner_left = -29.5
        self.inner_right = 29.5
        self.core_left = -29
        self.core_right = 29
        self.outer_left = -28.5
        self.outer_right = 28.5

    def initgl(self):
        glClearColor(0.0, 0.0, 0.0, 0.0)
        gluOrtho2D(-100.0, 100.0, -100.0, 100.0)

    def redraw(self):
        # 배경
        glClear(GL_COLOR_BUFFER_BIT)
        glColor3f(0, 0, 0)

        # 내부 선
        glBegin(GL_POLYGON)
        glVertex2f(self.inner_left, -50)
        glVertex2f(self.inner_right, -50)
        glVertex2f(self.inner_right, 50)
        glVertex2f(self.inner_left, 50)
        glEnd()

        # 중심 선
        glBegin(GL_POLYGON)
        glVertex2f(self.core_left, -50)
        glVertex2f(self.core_right, -50)
        glVertex2f(self.core_right, 50)
        glVertex2f(self.core_left, 50)
        glEnd()

        # 외부 선
        glBegin(GL_POLYGON)
        glVertex2f(self.outer_left, -50)
        glVertex2f(self.outer_right, -50)
        glVertex2f(self.outer_right, 50)
        glVertex2f(self.outer_left, 50)
        glEnd()

        lightning_segments_inner = generate_lightning((self.inner_left, -50), (self.inner_right, 50), 10, 5, 0.2, 0.7)
        lightning_segments_core = generate_lightning((self.core_left, -50), (self.core_right, 50), 10, 5, 0.2, 0.7)
        lightning_segments_outer = generate_lightning((self.outer_left, -50), (self.outer_right, 50), 10, 5, 0.2, 0.7)


        for segment in lightning_segments_inner:
            self.draw_lightning_segment(segment, (255, 255, 0))  # 내부 번개는 노란색으로 지정

        for segment in lightning_segments_core:
            self.draw_lightning_segment(segment, (255, 255, 255))  # 외부 번개는 흰색으로 지정

        for segment in lightning_segments_outer:
            self.draw_lightning_segment(segment, (255, 255, 0))  # 외부 번개는 노란색으로 지정

        self.tkSwapBuffers()

    def draw_lightning_segment(self, segment, color):
        glLineWidth(3)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glColor4fv(color + (segment.brightness,))

        glBegin(GL_LINE_STRIP)
        glVertex2f(segment.start[0], segment.start[1])
        glVertex2f(segment.end[0], segment.end[1])
        glEnd()

        glDisable(GL_BLEND)

class TestNeonLightning(unittest.TestCase):
    def test_neon_lightning(self):
        root = tk.Tk()
        root.title("OpenGL Rectangle Drawing")

        app = RectDrawingApp(root, width=800, height=800)
        app.pack(side="top", fill="both", expand=True)
        app.animate = 1
        root.mainloop()

if __name__ == '__main__':
    unittest.main()
