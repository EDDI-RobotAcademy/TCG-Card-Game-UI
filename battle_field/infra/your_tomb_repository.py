from battle_field.state.current_tomb import CurrentTombState
from battle_field_fixed_card.fixed_field_card import FixedFieldCard


class YourTombRepository:
    __instance = None

    current_tomb_state = CurrentTombState()
    # TODO: 무덤 보기 기능에서 카드 객체 빨리 그리기 위해 필요함
    current_tomb_unit_list = []
    current_tomb_unit_x_position = []

    x_base = 400

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def save_current_tomb_state(self, hand_card_id):
        self.current_tomb_state.place_unit_to_tomb(hand_card_id)
        print(f"Saved current tomb_card state: {hand_card_id}")

    def get_current_tomb_state(self):
        return self.current_tomb_state.get_current_tomb_unit_list()

    def create_tomb_card(self, card_id):
        index = len(self.current_tomb_unit_list)
        print(f"create_tomb_card() -> index: {index}, card_id: {card_id}")
        new_card = FixedFieldCard(local_translation=self.get_next_card_position(index))
        new_card.init_card(card_id)
        # new_card.set_index(index)
        self.current_tomb_unit_list.append(new_card)

        self.save_current_tomb_state(card_id)

    def create_tomb_card_list(self):
        current_tomb_card = self.get_current_tomb_state()
        print(f"current_tomb_card: {current_tomb_card}")

        for index, card_number in enumerate(current_tomb_card):
            print(f"index: {index}, card_number: {card_number}")
            new_card = FixedFieldCard(local_translation=self.get_next_card_position(index))
            new_card.init_card(card_number)
            new_card.set_index(index)
            self.current_tomb_unit_list.append(new_card)

    def get_current_tomb_unit_list(self):
        return self.current_tomb_unit_list

    def get_next_card_position(self, index):
        # TODO: 배치 간격 고려
        current_y = 300
        x_increment = 170
        next_x = self.x_base + x_increment * index
        return (next_x, current_y)

    def place_card_in_tomb(self, unit_card_id):
        self.current_tomb_unit_list.append(unit_card_id)

    def saveReceiveIpcChannel(self, receiveIpcChannel):
        self.__receiveIpcChannel = receiveIpcChannel

    def saveTransmitIpcChannel(self, transmitIpcChannel):
        self.__transmitIpcChannel = transmitIpcChannel

    def clear_every_resource(self):
        self.current_tomb_state = CurrentTombState()

        self.current_tomb_unit_list = []
        self.current_tomb_unit_x_position = []
