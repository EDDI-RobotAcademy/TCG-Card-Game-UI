class MyCardMainScene:
    def __init__(self):
        self.my_card_background = [] # 카드 전체 배경 화면, 사이드에 있는 나의 덱 화면
        self.text_list = [] # 'My Card', '나의 덱'
        self.button_list = [] # 버튼 도형
        self.card_list = [] # 나타낼 카드 리스트

        self.next_button = None
        self.prev_button = None

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

    def add_card_list(self, card):
        self.card_list.append(card)

    def get_card_list(self):
        return self.card_list