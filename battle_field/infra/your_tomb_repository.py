from battle_field.state.current_tomb import CurrentTombState


class YourTombRepository:
    __instance = None

    current_tomb_state = CurrentTombState()
    # TODO: 무덤 보기 기능에서 카드 객체 빨리 그리기 위해 필요함
    current_tomb_unit_list = []

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
        print(f"Saved current field_unit state: {hand_card_id}")

    def get_current_tomb_state(self):
        return self.current_tomb_state

    def place_unit_in_tomb(self, unit_card_id):
        self.current_tomb_unit_list.append(unit_card_id)

    def saveReceiveIpcChannel(self, receiveIpcChannel):
        self.__receiveIpcChannel = receiveIpcChannel

    def saveTransmitIpcChannel(self, transmitIpcChannel):
        self.__transmitIpcChannel = transmitIpcChannel