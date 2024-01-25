from OpenGL import GL
from my_deck_construction_frame.frame.my_deck_construction_frame import MyDeckConstructionFrame

class MyDeckConstructionFrameRenderer:
    def __init__(self, my_deck_construction_frame: MyDeckConstructionFrame):
        self.my_deck_construction_frame = my_deck_construction_frame

    def render(self):
        self.my_deck_construction_frame.tkMakeCurrent()
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        self.my_deck_construction_frame.draw_frame()
        self.my_deck_construction_frame.tkSwapBuffers()