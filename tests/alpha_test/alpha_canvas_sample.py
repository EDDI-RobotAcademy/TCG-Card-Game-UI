import tkinter as tk
from pyopengltk import OpenGLFrame
from OpenGL import GL, GLU, GLUT

class DarkenWindow(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.darkened = False
        self.darken_alpha = 0.0

    def initgl(self):
        GL.glClearColor(1.0, 1.0, 1.0, 0.0)
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        GL.glLoadIdentity()
        GLU.gluOrtho2D(0, self.width, self.height, 0)
        GLUT.glutInit()

    def redraw(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        GL.glColor4f(0.0, 0.0, 0.0, self.darken_alpha)
        GL.glBegin(GL.GL_QUADS)
        GL.glVertex2f(0, 0)
        GL.glVertex2f(self.width, 0)
        GL.glVertex2f(self.width, self.height)
        GL.glVertex2f(0, self.height)
        GL.glEnd()

        GL.glColor3f(1.0, 0.0, 0.0)
        GL.glBegin(GL.GL_QUADS)
        GL.glVertex2f(100, 100)
        GL.glVertex2f(300, 100)
        GL.glVertex2f(300, 300)
        GL.glVertex2f(100, 300)
        GL.glEnd()

        self.tkSwapBuffers()

    def make_screen_alpha(self):
        if self.darken_alpha < 1.0:
            self.darken_alpha += 0.1
            self.redraw()
            self.update_idletasks()

            self.after(100, self.make_screen_alpha)

def main():
    root = tk.Tk()
    window = DarkenWindow(root, width=400, height=400)
    window.pack(fill=tk.BOTH, expand=1)

    darken_button = tk.Button(root, text="Toggle Darken Screen", command=window.make_screen_alpha)
    darken_button.pack()

    root.mainloop()

if __name__ == "__main__":
    main()