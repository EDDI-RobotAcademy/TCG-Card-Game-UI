class MyDeckRegisterScene:
    def __init__(self):
        self.alpha_rectangle = [] # 검정 투명 화면
        self.my_deck_background = [] # 덱 배경 화면
        self.text_list = [] # '덱 생성', '입력 하시오' 텍스트
        self.button_list = [] # 되돌아 가기, 확인 버튼
        self.text_box = [] # 입력 창
        self.deck_name_list = [] # 입력 창에 입력 받은 내용 저장
        self.deck_button_list = [] # 생성된 덱 버튼

    def add_alpha_rectangle(self, alpha_rectangle):
        self.alpha_rectangle.append(alpha_rectangle)

    def get_alpha_rectangle(self):
        return self.alpha_rectangle

    def add_my_deck_background(self, rectangle):
        self.my_deck_background.append(rectangle)

    def get_my_deck_background(self):
        return self.my_deck_background

    def add_text_list(self, text):
        self.text_list.append(text)

    def get_text_list(self):
        return self.text_list

    def add_button_list(self, button):
        self.button_list.append(button)

    def get_button_list(self):
        return self.button_list

    def add_text_box(self, box):
        self.text_box.append(box)

    def get_text_box(self):
        return self.text_box

    def add_deck_name_list(self, deck_name):
        self.deck_name_list.append(deck_name)

    def get_deck_name_list(self):
        return self.deck_name_list

    def add_deck_button_list(self, button):
        self.deck_button_list.append(button)

    def get_deck_button_list(self):
        return self.deck_button_list
