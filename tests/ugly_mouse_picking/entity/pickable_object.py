from OpenGL.GL import *

class PickableObject:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.selected = False

    def draw(self):
        if self.selected:
            glColor3f(1.0, 0.0, 0.0)
        else:
            glColor3f(0.0, 1.0, 0.0)

        glBegin(GL_QUADS)
        glVertex2f(self.x, self.y)
        glVertex2f(self.x + self.width, self.y)
        glVertex2f(self.x + self.width, self.y + self.height)
        glVertex2f(self.x, self.y + self.height)
        glEnd()

    def is_point_inside(self, point):
        return self.x <= point[0] <= self.x + self.width and self.y <= point[1] <= self.y + self.height

    def update_position(self, x, y):
        self.x = x
        self.y = y