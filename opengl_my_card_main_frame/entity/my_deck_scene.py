class MyDeckScene:
    def __init__(self):
        self.deck_background = [] # 덱 배경 화면
        self.deck_name_list = []  # 만든 덱 이름 화면에 띄워야 함
        self.button_list = []  # 뒤로 가기, 앞으로 가기 버튼

    def add_deck_background(self, deck_rectangle):
        self.deck_background.append(deck_rectangle)

    def get_deck_background(self):
        return self.deck_background

    def add_deck_name_list(self, deck_name):
        self.deck_name_list.append(deck_name)

    def get_deck_name_list(self):
        return self.deck_name_list

    def add_button_list(self, button):
        self.button_list.append(button)

    def get_button_list(self):
        return self.button_list