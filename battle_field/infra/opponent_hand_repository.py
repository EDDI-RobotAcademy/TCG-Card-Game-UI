from battle_field.state.current_opponent_hand import CurrentOpponentHandState
from battle_field_fixed_card.fixed_field_opponent_hand_card import FixedFieldOpponentHandCard
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage
class OpponentHandRepository:
    __instance = None

    preDrawedImageInstance = PreDrawedImage.getInstance()

    total_width = None
    total_height = None

    current_opponent_hand_state = CurrentOpponentHandState()
    current_opponent_hand_card_list = []
    current_opponent_hand_card_x_position = []

    x_base = 0

    __transmitIpcChannel = None
    __receiveIpcChannel = None


    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def set_x_base(self, x_base):
        self.x_base = x_base

    def set_total_window_size(self, width, height):
        self.total_width = width
        self.total_height = height

    def save_current_opponent_hand_state(self, hand_list):
        self.current_opponent_hand_state.add_to_opponent_hand(hand_list)
        print(f"Saved current opponent hand state: {hand_list}")

    def get_current_opponent_hand_state(self):
        return self.current_opponent_hand_state.get_current_opponent_hand()

    def get_current_opponent_hand_card_list(self):
        return self.current_opponent_hand_card_list

    def create_opponent_hand_card_list(self):
        current_opponent_hand = self.get_current_opponent_hand_state()
        print(f"current_opponent_hand: {current_opponent_hand}")

        for index, card_number in enumerate(current_opponent_hand):
            print(f"index: {index}, card_number: {card_number}")
            initial_position = self.get_start_opponent_card_position(index)
            new_card = FixedFieldOpponentHandCard(local_translation=initial_position)
            new_card.init_card()
            self.current_opponent_hand_card_list.append(new_card)

    def get_start_opponent_card_position(self, index):

        current_y = -100

        start = self.total_width * 0.2976
        end = self.total_width * 0.6997
        gap_width = (end - start - 525.0) / 4.0

        x_increment = 105 + gap_width
        place_index = index % 5

        self.x_base = start
        next_x = self.x_base + x_increment * place_index
        return (next_x, current_y)