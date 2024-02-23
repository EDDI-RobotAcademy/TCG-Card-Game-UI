from battle_field_muligun.state.current_hand import CurrentHandState
from opengl_battle_field_pickable_card.pickable_card import PickableCard


class YourHandRepository:
    __instance = None

    current_hand_state = CurrentHandState()
    current_hand_card_list = []
    current_hand_card_x_position = []
    select_change_card_id_list = []

    x_base_muligun = 120 # 멀리건에서의 맨 처음 카드 위치.

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def save_current_hand_state(self, hand_list):
        self.current_hand_state.add_to_hand(hand_list)
        print(f"Saved current hand state: {hand_list}")


    def get_current_hand_state(self):
        return self.current_hand_state.get_current_hand()


    # 멀리건 화면에서의 카드 리스트
    def create_hand_card_list(self):
        current_hand = self.get_current_hand_state()
        print(f"current_hand: {current_hand}")

        for index, card_number in enumerate(current_hand):
            print(f"index: {index}, card_number: {card_number}")
            initial_position = self.get_start_hand_card_position(index)
            new_card = PickableCard(local_translation=initial_position, scale=300)
            new_card.init_card_scale(card_number)
            self.current_hand_card_list.append(new_card)


    # 인덱스로 선택한 카드 지우기.
    def delete_select_card(self, select_card_list):

        hand_card_state = self.get_current_hand_state() # 카드 number
        hand_card_list = self.get_current_hand_card_list() # 카드 object

        for index in sorted(select_card_list.keys(), reverse=True):

            hand_card_state.pop(index)
            hand_card_list.pop(index)

        print(f"after- 상태: {hand_card_state}, 오브젝트: {hand_card_list}")

    # 서버로 교체할 카드의 아이디를 보내주기 위해 저장.
    def select_card_id_list(self, select_card_list):
        id_list = self.select_change_card_id_list

        for card_object in select_card_list.values():
            id_list.append(id(card_object))


    def get_change_card_id_list(self):
        return self.select_change_card_id_list


    def remove_card_by_id(self, card_id):
        card_list = self.get_current_hand_card_list()

        for card in card_list:
            if card.get_card_number() == card_id:
                card_list.remove(card)

        self.current_hand_state.remove_from_hand(card_id)

        print(f"after clear -> current_hand_list: {self.current_hand_card_list}, current_hand_state: {self.get_current_hand_state()}")


    # 멀리건 화면에서 카드 배치
    def get_start_hand_card_position(self, index):
        current_y = 300
        x_increment = 340
        next_x = self.x_base_muligun + x_increment * index
        return (next_x, current_y)

    def get_current_hand_card_list(self):
        return self.current_hand_card_list

    def saveTransmitIpcChannel(self, transmitIpcChannel):
        print("BattleFieldMeligunFrameRepositoryImpl: saveTransmitIpcChannel()")
        self.__transmitIpcChannel = transmitIpcChannel

    def saveReceiveIpcChannel(self, receiveIpcChannel):
        print("BattleFieldMeligunFrameRepositoryImpl: saveReceiveIpcChannel()")
        self.__receiveIpcChannel = receiveIpcChannel

    def requestBattleDeckCard(self, battleDeckCardRequest):
        self.__transmitIpcChannel.put(battleDeckCardRequest)
        return self.__receiveIpcChannel.get()

    def requestMuligun(self, muligunRequest):
        self.__transmitIpcChannel.put(muligunRequest)
        return self.__receiveIpcChannel.get()
