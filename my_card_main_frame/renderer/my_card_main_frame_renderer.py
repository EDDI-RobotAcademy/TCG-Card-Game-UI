from OpenGL import GL
from my_card_frame.frame.my_card_frame import MyCardFrame

class MyCardFrameRenderer:
    def __init__(self, my_card_frame: MyCardFrame):
        self.my_card_frame = my_card_frame

    def render(self):
        self.my_card_frame.tkMakeCurrent()
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        self.my_card_frame.redraw()
        self.my_card_frame.tkSwapBuffers()