from opengl_shape.oval import Oval
from opengl_shape.rectangle import Rectangle


class SkillFocusPanel:

    def __init__(self):
        self.skill_focus_panel = None
        self.skill_background_panel = None

        self.total_width = None
        self.total_height = None

        self.width_ratio = 1
        self.height_ratio = 1

        skill_background_panel_alpha = 0

    def set_total_window_size(self, width, height):
        self.total_width = width
        self.total_height = height

    def get_width_ratio(self):
        return self.width_ratio

    def set_width_ratio(self, width_ratio):
        self.width_ratio = width_ratio

    def get_height_ratio(self):
        return self.height_ratio

    def set_height_ratio(self, height_ratio):
        self.height_ratio = height_ratio

    def change_local_translation(self, _translation):
        self.local_translation = _translation

    def get_skill_background_panel(self):
        return self.skill_background_panel

    def clear_every_skill_focus_panel(self):
        self.clear_skill_background_panel()
        self.clear_skill_focus_panel()

    def clear_skill_background_panel(self):
        del self.skill_background_panel
        self.skill_background_panel = None

    def get_skill_focus_panel(self):
        return self.skill_focus_panel

    def clear_skill_focus_panel(self):
        del self.skill_focus_panel
        self.skill_focus_panel = None

    def create_skill_background_panel(self):
        rectangle_color = (0.0, 0.0, 0.0, 0.0)

        self.skill_background_panel = Rectangle(
            rectangle_color,
            [
                (0, 0),
                (self.total_width, 0),
                (self.total_width, self.total_height),
                (0, self.total_height)
            ],
            (0, 0),
            (0, 0))

    def create_skill_focus_panel(self):
        oval_color = (0.0, 0.0, 0.0, 0.0)

        # 0.326836
        # 0.202

        # 0.4854
        # 0.3

        # 0.6472
        # 0.4

        # 0.872 - 0.138 = 0.734
        # 0.734 - 0.6472 = 0.0868 -> 0.0868 / 2 = 0.0434
        # 0.138 + 0.0434 = 0.1814
        # 0.872 - 0.0434 = 0.8286
        # 0.246 - 0.099 = 0.147
        # 0.448 + 0.099 = 0.547

        # (0.8286 - 0.1814) / 2 = 0.3236
        # (0.547 - 0.147) / 2 = 0.2
        # center x = 0.505
        # center y = 0.347
        # local_translation = (0.505, 0.347)
        # radius_x = 0.2
        # radius_y = 0.3236

        # 1848, 1016
        # local_translation_x = self.total_width * 0.505
        # local_translation_y = self.total_height * 0.347
        #
        # radius_x = self.total_width * 0.2
        # radius_y = self.total_height * 0.3236
        #
        # local_translation = (local_translation_x, local_translation_y)
        # center = local_translation
        #
        # left_x_point = self.total_width * 0.138
        # right_x_point = self.total_width * 0.872
        # top_y_point = self.total_height * 0.246
        # bottom_y_point = self.total_height * 0.448

        local_translation_x = self.total_width * 0.505
        local_translation_y = self.total_height * 0.347

        radius_x = self.total_width * 0.4
        radius_y = self.total_height * 0.2

        local_translation = (local_translation_x, local_translation_y)
        center = local_translation

        # left_x_point = self.total_width * 0.138
        # right_x_point = self.total_width * 0.872
        # top_y_point = self.total_height * 0.246
        # bottom_y_point = self.total_height * 0.448

        # Oval(color=(1.0, 1.0, 1.0, 1.0),
        #      center=self.center,
        #      radius_x=self.radius_x,
        #      radius_y=self.radius_y,
        #      local_translation=self.local_translation,
        #      global_translation=self.global_translation)

        self.skill_focus_panel = Oval(
            oval_color,
            center=center,
            radius_x=radius_x,
            radius_y=radius_y)

        self.skill_focus_panel.set_draw_border(False)
