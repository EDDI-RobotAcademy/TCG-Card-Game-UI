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
