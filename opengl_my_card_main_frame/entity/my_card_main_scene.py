class MyCardMainScene:
    def __init__(self):
        self.alpha_rectangle = []
        self.image_rectangle_element = []
        self.text_render = []
        self.text_box = []
        self.my_card_rectangle = []
        self.my_deck_rectangle = []
        self.button_list = []

    def add_alpha_rectangle(self, alpha_rectangle):
        self.alpha_rectangle.append(alpha_rectangle)

    def get_alpha_rectangle(self):
        return self.alpha_rectangle

    def add_image_rectangle(self, image_rectangle):
        self.image_rectangle_element.append(image_rectangle)

    def get_image_rectangle(self):
        return self.image_rectangle_element

    def add_text_render(self, text):
        self.text_render.append(text)

    def get_text_render(self):
        return self.text_render

    def add_text_box(self, box):
        self.text_box.append(box)

    def get_text_box(self):
        return self.text_box

    def add_my_card_rectangle(self, my_card_rectangle):
        self.my_card_rectangle.append(my_card_rectangle)

    def get_my_card_rectangle(self):
        return self.my_card_rectangle

    def add_my_deck_rectangle(self, my_deck_rectangle):
        self.my_deck_rectangle.append(my_deck_rectangle)

    def get_my_deck_rectangle(self):
        return self.my_deck_rectangle

    def add_button_list(self, button):
        self.button_list.append(button)

    def get_button_set(self):
        return self.button_list