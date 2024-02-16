import os

from pyopengltk import OpenGLFrame
from OpenGL import GL, GLU

from tests.lsh.battle_field_unit_card_frame.entity.battle_field_unit_card_scene import BattleFieldUnitCardScene
from tests.lsh.battle_field_unit_card_frame.entity.circle import Circle
from tests.lsh.battle_field_unit_card_frame.entity.image_item import ImageItem
from tests.lsh.battle_field_unit_card_frame.entity.rectangle import Rectangle
from tests.lsh.battle_field_unit_card_frame.renderer.battle_field_unit_card_frame_renderer import BattleFieldUnitCardFrameRenderer


class BattleFieldUnitCardFrame(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.domain_scene = BattleFieldUnitCardScene()

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.width = screen_width
        self.height = screen_height

        self.bind("<Configure>", self.on_resize)

        self.init_shapes()

        current_directory = os.getcwd()
        print("현재 디렉토리:", current_directory)

        self.domain_scene.add_image(
            ImageItem(
                path="../../local_storage/card_images/card1.png",
                position=(25, 25),
                size=(300, 300),
                translation=(0, 0)))

        equip_image = ImageItem(
                path="../../local_storage/card_images/equip_white.jpeg",
                position=(390, 30),
                size=(40, 40),
                translation=(0, 0))
        self.domain_scene.add_image(equip_image)
        equip_image.set_visible(False)

        self.renderer = BattleFieldUnitCardFrameRenderer(self.domain_scene, self)

    def init_shapes(self):
        equip_card = Rectangle(
            color=(0.6, 0.4, 0.6, 1.0),
            vertices=[(0, 0), (350, 0), (350, 500), (0, 500)],
            local_translation=(20, 20))
        equip_card.set_draw_gradient(True)
        self.domain_scene.add_shape(equip_card)

        # equip_effect = Rectangle(
        #     color=(1.0, 1.0, 1.0, 1.0),
        #     vertices=[(0, 0), (40, 0), (40, 40), (0, 40)],
        #     translation=(390, 30))
        # equip_effect.set_draw_gradient(True)
        # self.domain_scene.add_shape(equip_effect)

        unit_card = Rectangle(
            color=(0.0, 0.78, 0.34, 1.0),
            vertices=[(0, 0), (350, 0), (350, 500), (0, 500)],
            translation=(0, 0))
        unit_card.set_draw_gradient(True)
        self.domain_scene.add_shape(unit_card)

        circle_radius = 30
        circle_center_coordinates = [(0, 0), (350, 0), (350, 500), (0, 500)]
        for center in circle_center_coordinates:
            circle = Circle(
                    color=(1.0, 0.33, 0.34, 1.0),
                    center=center,
                    radius=circle_radius,
                    translation=(0, 0))
            self.domain_scene.add_shape(circle)

        equip_card.set_visible(False)

    def apply_translation(self, translation):
        for shape in self.domain_scene.shapes:
            print("shape translate")
            shape.translate(translation)

        for image in self.domain_scene.images:
            image.translate(translation)

    def initgl(self):
        GL.glClearColor(1.0, 1.0, 1.0, 0.0)
        GL.glOrtho(0, self.width, self.height, 0, -1, 1)

    def toggle_visibility(self):
        equip_card = self.domain_scene.shapes[0]
        equip_card.set_visible(not equip_card.get_visible())

        equip_image = self.domain_scene.images[1]
        equip_image.set_visible(not equip_image.get_visible())

        self.redraw()

    def reshape(self, width, height):
        GL.glViewport(0, 0, width, height)
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GLU.gluOrtho2D(0, width, height, 0)
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()

    def on_resize(self, event):
        self.reshape(event.width, event.height)

    def redraw(self):
        self.apply_translation((50, 50))
        self.renderer.render()

