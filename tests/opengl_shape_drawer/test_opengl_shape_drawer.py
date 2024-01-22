import tkinter
import unittest

from battle_field_unit_card_frame.frame.battle_field_unit_card_frame import BattleFieldUnitCardFrame
from opengl_shape_drawer.service.opengl_shape_drawer_service_impl import OpenglShapeDrawerServiceImpl


class TestOpenGLShapeDrawer(unittest.TestCase):

    def test_opengl_shaper_create_rectangle(self):
        opengl_shape_drawer_service = OpenglShapeDrawerServiceImpl.getInstance()
        rectangle_id = opengl_shape_drawer_service.create_rectangle(
            color=(0.6, 0.4, 0.6, 1.0),
            vertices=[(0, 0), (350, 0), (350, 500), (0, 500)]
        )

        shape = opengl_shape_drawer_service.get_shape_drawer_scene()
        print(f"shape: {shape}")

        self.assertTrue(rectangle_id is not None)
        self.assertTrue(opengl_shape_drawer_service.get_shape_drawer_scene() is not None)



if __name__ == '__main__':
    unittest.main()