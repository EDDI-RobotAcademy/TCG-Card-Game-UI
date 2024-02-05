from OpenGL import GL
from OpenGL.GL import *
from OpenGL.GLU import *

from opengl_pickable_shape.pickable_rectangle import PickableRectangle


class CardFrameRenderer:
    def __init__(self, card_list, window):
        self.card_list = card_list
        self.window = window

    def render(self):
        self.window.tkMakeCurrent()

        for card in self.card_list:
            pickable_card_base = card.get_pickable_card_base()
            attached_tool_card = card.get_tool_card()
            attached_shape_list = pickable_card_base.get_attached_shapes()

            attached_tool_card.draw()

            for attached_shape in attached_shape_list:
                attached_shape.draw()

        self.window.tkSwapBuffers()