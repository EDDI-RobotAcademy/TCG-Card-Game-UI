from opengl_pickable_shape.pickable_rectangle import PickableRectangle
from opengl_shape.rectangle import Rectangle


class TestCard:
    def __init__(self, window, battle_field, color = (0, 0, 0, 1.0),local_translation=(0, 0), scale=1, card_type=None):
        self.card_type = card_type
        self.color = color
        self.shapes = []
        self.tool = None
        self.local_translation = local_translation
        self.scale = scale
        self.window = window
        self.battle_field = battle_field
        self.pickable_card_base = None
        self.is_hand = True

    def get_pickable_card_shapes(self):
        return self.shapes
    def get_pickable_card_base(self):
        return self.pickable_card_base
    def add_shape(self, shape):
        shape.local_translate(self.local_translation)
        self.shapes.append(shape)


    def create_pickable_card_rectangle(self, color, vertices, local_translation):
        pickable_card_base = PickableRectangle(color=color,
                                               local_translation=local_translation,
                                               vertices=vertices)
        self.add_shape(pickable_card_base)
        pickable_card_base.set_draw_gradient(True)
        return pickable_card_base

    def move_to_field(self, field_x, field_y):
        self.is_hand = False
        self.shapes.clear()
        self.x1, self.x2, self.y1, self.y2 = field_x-50, field_x+50, field_y-100,field_y+100
        #self.pickable_card_base.set_visible=False
        self.pickable_card_base = (self.create_pickable_card_rectangle(color=self.color,
                                                                       local_translation=self.local_translation,
                vertices=[(self.x1, self.y1), (self.x2, self.y1), (self.x2, self.y2),(self.x1, self.y2)]),)
        
    def set_energy(self):
        self.shapes.clear()
        if self.tool is not None:
            self.add_shape(self.tool)

        self.color = (1,1,0,1)
        # self.pickable_card_base.set_visible=False
        self.pickable_card_base = (self.create_pickable_card_rectangle(color=self.color,
                                                                       local_translation=self.local_translation,
                vertices=[(self.x1, self.y1), (self.x2, self.y1), (self.x2, self.y2),(self.x1, self.y2)]),)

    def equip_tool(self):
        self.shapes.clear()
        self.tool = PickableRectangle(color=(0.7,0.1,0.3,1), local_translation=self.local_translation,
                         vertices=[(self.x1+20, self.y1), (self.x2+20, self.y1), (self.x2+20, self.y2), (self.x1+20, self.y2)])
        self.add_shape(self.tool)

        self.pickable_card_base = (self.create_pickable_card_rectangle(color=self.color,
                                                                       local_translation=self.local_translation,
                                                                       vertices=[(self.x1, self.y1), (self.x2, self.y1),
                                                                                 (self.x2, self.y2),
                                                                                 (self.x1, self.y2)]),)


    def move_to_tomb(self):
        self.shapes.clear()

    def init_shapes(self):
        self.pickable_card_base = (self.create_pickable_card_rectangle(color=self.color,
                                                                       local_translation=self.local_translation,
                                                                       vertices=[(100, 500), (200, 500), (200, 700), (100, 700)]))

        # self.pickable_card_base = (self.create_pickable_card_rectangle(color=(0, 0, 0, 1.0),
        #                                                                local_translation=self.local_translation,
        #                                                                vertices=[(220, 500), (320, 500), (320, 700), (220, 700)]))
        #
        # self.pickable_card_base = (self.create_pickable_card_rectangle(color=(0, 0, 0, 1.0),
        #                                                                local_translation=self.local_translation,
        #                                                                vertices=[(340, 500), (440, 500), (440, 700), (340, 700)]))
        #
        # self.pickable_card_base = (self.create_pickable_card_rectangle(color=(0, 0, 0, 1.0),
        #                                                                local_translation=self.local_translation,
        #                                                                vertices=[(460, 500), (560, 500), (560, 700), (460, 700)]))
        #
        # self.pickable_card_base = (self.create_pickable_card_rectangle(color=(0, 0, 0, 1.0),
        #                                                                local_translation=self.local_translation,
        #                                                                vertices=[(580, 500), (680, 500), (680, 700), (580, 700)]))
        #
