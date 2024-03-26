class MyCardMainScene:
    def __init__(self):
        self.my_card_background = [] # 카드 전체 배경 화면, 사이드에 있는 나의 덱 화면
        self.text_list = [] # 'My Card', '나의 덱'
        self.button_list = [] # 버튼 도형
        self.card_list = [] # 나타낼 카드 리스트

        self.next_button = None
        self.prev_button = None

        self.go_back_button = None
        self.prepare_message = None
        self.ok_button = None

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

    def add_next_button(self, button):
        self.next_button = button

    def get_next_button(self):
        return self.next_button

    def add_prev_button(self, button):
        self.prev_button = button

    def get_prev_button(self):
        return self.prev_button

    def add_go_back_button(self, button):
        self.go_back_button = button

    def get_go_back_button(self):
        return self.go_back_button

    def add_create_deck_button(self, button):
        self.create_deck_button = button

    def get_create_deck_button(self):
        return self.create_deck_button

    def add_card_list(self, card):
        self.card_list.append(card)

    def get_card_list(self):
        return self.card_list

    def add_prepare_message(self, prepare_message):
        self.prepare_message = prepare_message

    def get_prepare_message(self):
        return self.prepare_message

    def add_ok_button(self, button):
        self.ok_button = button

    def get_ok_button(self):
        return self.ok_button