import tkinter
import tkinter as tk
import unittest
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from pyopengltk import OpenGLFrame
from screeninfo import get_monitors


class RectDrawingApp(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        self.init_monitor_specification()
        self.state = "tilt_left"

        self.bind("<Configure>", self.on_resize)

    def initgl(self):
        glClearColor(1.0, 1.0, 1.0, 0.0)
        glOrtho(0, self.width, self.height, 0, -1, 1)

        self.rotation_angle = 0.0
        self.animation_speed = 0.0
        self.acceleration = 0.3
        self.target_angle_tilt_left = 45.0
        self.target_time_tilt_left = 1.2
        self.target_angle_counterclockwise = 45.0
        self.target_angle_clockwise = -30.0
        self.target_angle_reset = 0.0
        self.rotate_clockwise = False
        self.animation_started = False
        self.animation_completed = False

    def reshape(self, width, height):
        print(f"Reshaping window to width={width}, height={height}")

        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, width, height, 0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def on_resize(self, event):
        self.reshape(event.width, event.height)

    def redraw(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glLoadIdentity()

        glRotatef(self.rotation_angle, 0, 0, 1)

        glColor3f(0.0, 0.0, 0.0)

        glBegin(GL_POLYGON)
        glVertex2f(-0.5, -0.5)
        glVertex2f(0.5, -0.5)
        glVertex2f(0.5, 0.5)
        glVertex2f(-0.5, 0.5)
        glEnd()

        self.tkSwapBuffers()

    def animate_rotation(self):
        if self.state == "tilt_left":
            # w = (theta) / t
            #
            # w = w0 + alpha * t
            # theta = w0 * t + 0.5 * alpha * t^2 => 45 = 0 + 0.5 * alpha * t^2 => 45 = 0.5 * alpha * 1.2^2 => alpha = 62.5
            # 2 * alpha * theta = w^2 - w0^2
            alpha = 0.0625

            self.animation_speed += alpha
            self.rotation_angle += self.animation_speed

            if self.rotation_angle >= self.target_angle_tilt_left:
                self.state = "attack_right"
                self.animation_speed = 0.0

        elif self.state == "attack_right":
            alpha = 0.1025

            self.animation_speed += alpha
            self.rotation_angle -= self.animation_speed

            if self.rotation_angle <= self.target_angle_clockwise:
                self.state = "return_origin"

        elif self.state == "return_origin":
            # Use angular acceleration for smooth transition
            self.animation_speed += self.acceleration
            self.rotation_angle += self.animation_speed

            if self.rotation_angle >= self.target_angle_reset:
                self.rotation_angle = self.target_angle_reset
                self.state = "idle"
                self.animation_completed = True
                self.animation_speed = 0.0

        if not self.animation_completed:
            self.after(17, self.animate_rotation)

    def on_key_press(self, event):
        if event.keysym == 'r' and not self.animation_started:
            self.state = "tilt_left"
            self.animation_completed = False
            self.animate_rotation()

    def init_monitor_specification(self):
        monitors = get_monitors()
        target_monitor = monitors[2] if len(monitors) > 2 else monitors[0]

        self.width = target_monitor.width
        self.height = target_monitor.height

        self.is_reshape_not_complete = True

        self.current_width = self.width
        self.current_height = self.height

        self.prev_width = self.width
        self.prev_height = self.height

        self.width_ratio = 1.0
        self.height_ratio = 1.0

class TestAppWindowSecond(unittest.TestCase):
    def test_rotate_opengl_basic_second(self):
        root = tkinter.Tk()
        root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}-0-0")
        root.deiconify()

        pre_drawed_battle_field_frame = RectDrawingApp(root)
        pre_drawed_battle_field_frame.pack(fill=tkinter.BOTH, expand=1)
        root.update_idletasks()

        root.bind("<KeyPress>", pre_drawed_battle_field_frame.on_key_press)

        def animate():
            pre_drawed_battle_field_frame.redraw()
            root.after(17, animate)

        root.after(0, animate)

        root.mainloop()


if __name__ == '__main__':
    unittest.main()
