import unittest

from OpenGL.GL import *
from OpenGL.GLUT import *


class TestRatioBasedDraw(unittest.TestCase):
    def draw_cube(self):
        glutSolidCube(1)

    def display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.draw_cube()
        glutSwapBuffers()

    def reshape(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(-2, 2, -2, 2, -10, 10)  # 직교 투영 설정
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def test_start_ratio_drawing(self):
        glutInit()
        glutInitWindowSize(800, 600)
        glutCreateWindow("PyOpenGL Cube")

        glEnable(GL_DEPTH_TEST)

        glutDisplayFunc(self.display)
        glutReshapeFunc(self.reshape)

        glutMainLoop()

if __name__ == '__main__':
    unittest.main()
