class BuyRandomCardScene:
    def __init__(self):
        self.my_card_background = [] # 카드 전체 배경 화면, 사이드에 있는 나의 덱 화면
        self.text_list = []
        self.button_list = []
        self.card_list = []

        self.buy_random_background = None
        self.go_to_back_button = None
        self.again_button = None
        self.try_again_screen = None
        self.yes_button = None
        self.no_button = None

    def add_buy_random_background(self, background):
        self.buy_random_background = background

    def get_buy_random_background(self):
        return self.buy_random_background

    def add_my_card_background(self, rectangle):
        self.my_card_background.append(rectangle)

    def get_my_card_background(self):
        return self.my_card_background

    def add_text_list(self, text):
        self.text_list.append(text)

    def get_text_list(self):
        return self.text_list

    def add_button_list(self, button):
        self.button_list.append(button)

    def get_button_list(self):
        return self.button_list

    def add_go_to_back_button(self, go_to_back_button):
        self.go_to_back_button = go_to_back_button

    def get_go_to_back_button(self):
        return self.go_to_back_button

    def add_again_button(self, again_button):
        self.again_button = again_button

    def get_again_button(self):
        return self.again_button

    def add_card_list(self, card):
        self.card_list.append(card)

    def get_card_list(self):
        return self.card_list

    def add_try_again_screen(self, try_again_screen):
        self.try_again_screen = try_again_screen

    def get_try_again_screen(self):
        return self.try_again_screen

    def add_yes_button(self, yes_button):
        self.yes_button = yes_button

    def get_yes_button(self):
        return self.yes_button

    def add_no_button(self, no_button):
        self.no_button = no_button

    def get_no_button(self):
        return self.no_button
