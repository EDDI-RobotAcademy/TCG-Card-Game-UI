from battle_field_muligun.state.current_hand import CurrentHandState
from opengl_battle_field_pickable_card.legacy.pickable_card import LegacyPickableCard
from opengl_battle_field_pickable_card.pickable_card import PickableCard


class MuligunYourHandRepository:
    __instance = None

    current_hand_state = CurrentHandState()
    current_hand_card_list = []
    current_hand_card_x_position = []
    select_change_card_id_list = []
    card_dic = {}

    x_base_muligun = 90 # 멀리건에서의 맨 처음 카드 위치.
    is_opponent_mulligan_done = False
    is_my_mulligan_done = False
    is_doing_mulligan = True
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def find_index_by_selected_object(self, selected_object):
        for index, card in enumerate(self.current_hand_card_list):
            if card == selected_object:
                return index
        return -1

    def save_current_hand_state(self, hand_list):
        self.current_hand_state.add_to_hand_list(hand_list)
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
            new_card.set_card_number(card_number)
            new_card.init_card_scale(card_number)
            self.current_hand_card_list.append(new_card)


    # 인덱스로 선택한 카드 지우기.
    def delete_select_card(self, select_card_list):

        hand_card_state = self.get_current_hand_state() # 카드 number
        hand_card_list = self.get_current_hand_card_list() # 카드 object

        for card_number, card_object in zip(hand_card_state, hand_card_list):
            self.card_dic[card_object] = card_number

        card_dic = self.get_card_dic()
        print(f"card_dic: {card_dic}")

        for card_object in select_card_list.values():
            hand_card_list.remove(card_object)
            if card_object in card_dic.keys():
                hand_card_state.remove(card_dic.get(card_object))

        print(f"<after> 상태: {hand_card_state}, 오브젝트: {hand_card_list}")

    def create_muligun_hand_unit_card(self, card_id):
        index = len(self.current_hand_card_list)
        print(f"create_muligun_hand_unit_card() -> card_id: {card_id}, index: {index}")
        new_card = PickableCard(local_translation=self.get_start_hand_card_position(index), scale=300)
        new_card.set_card_number(card_id)
        print("PickableCard 생성자 호출")
        new_card.init_card_scale(card_id)
        print("new_card.init_card_scale(card_id)")
        # new_card.set_index(index)
        self.current_hand_card_list.append(new_card)
        print("self.current_hand_card_list.append(new_card)")

        self.current_hand_state.add_to_hand(card_id)
        print(f"current_hand_state list: {self.get_current_hand_state()}")

    # def remove_card_by_multiple_index(self, card_index_list):
    #     print(f"remove_card_by_multiple_index -> card_index_list: {card_index_list}")
    #     print(f"len(self.current_hand_card_list) = {len(self.current_hand_card_list)}")
    #
    #     for index in sorted(card_index_list, reverse=True):
    #         if 0 <= index < len(self.current_hand_card_list):
    #             removed_card = self.current_hand_card_list.pop(index)
    #             self.current_hand_state.remove_hand_by_index(index)
    #             print(f"Removed card at index {index}: {removed_card}")
    #         else:
    #             print(f"Invalid index: {index}. No card removed for this index.")
    #
    #     print(
    #         f"Removed cards at indices {card_index_list} -> current_hand_list: {self.current_hand_card_list}, current_hand_state: {self.get_current_hand_state()}"
    #     )

    def remove_card_by_multiple_index(self, card_index_list):
        print(f"remove_card_by_multiple_index -> card_index_list: {card_index_list}")
        print(f"len(self.current_hand_card_list) = {len(self.current_hand_card_list)}")

        self.current_hand_card_list[:] = [
            card for index, card in enumerate(self.current_hand_card_list) if index not in card_index_list
        ]

        for index in sorted(card_index_list, reverse=True):
            self.current_hand_state.remove_hand_by_index(index)

        print(
            f"Removed cards at indices {card_index_list} -> current_hand_list: {self.current_hand_card_list}, current_hand_state: {self.get_current_hand_state()}"
        )

    def replace_hand_card_position(self):
        current_y = 260
        x_increment = 360

        for index, current_hand_card in enumerate(self.current_hand_card_list):
            next_x = self.x_base_muligun + x_increment * index
            local_translation = (next_x, current_y)

            # tool_card = current_hand_card.get_tool_card()
            # tool_card.local_translate(local_translation)

            pickable_card_base = current_hand_card.get_pickable_card_base()
            pickable_card_base.local_translate(local_translation)

            for attached_shape in pickable_card_base.get_attached_shapes():
                attached_shape.local_translate(local_translation)

    def get_card_dic(self):
        return self.card_dic



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
        current_y = 260
        x_increment = 360
        next_x = self.x_base_muligun + x_increment * index
        return (next_x, current_y)

    def get_current_hand_card_list(self):
        return self.current_hand_card_list

    def set_is_opponent_mulligan(self, mulligan_done):
        self.is_opponent_mulligan_done = mulligan_done

    def get_is_opponent_mulligan(self):
        return self.is_opponent_mulligan_done

    def set_is_my_mulligan(self, mulligan_done):
        self.is_my_mulligan_done = mulligan_done

    def get_is_my_mulligan(self):
        return self.is_my_mulligan_done

    def saveTransmitIpcChannel(self, transmitIpcChannel):
        print("BattleFieldMeligunFrameRepositoryImpl: saveTransmitIpcChannel()")
        self.__transmitIpcChannel = transmitIpcChannel

    def saveReceiveIpcChannel(self, receiveIpcChannel):
        print("BattleFieldMeligunFrameRepositoryImpl: saveReceiveIpcChannel()")
        self.__receiveIpcChannel = receiveIpcChannel

    def requestMuligun(self, muligunRequest):
        self.__transmitIpcChannel.put(muligunRequest)
        print("여기까지 왔냐?")
        return self.__receiveIpcChannel.get()

    def requestCheckOpponentMuligun(self, checkOpponentMuligunRequest):
        self.__transmitIpcChannel.put(checkOpponentMuligunRequest)
        print("상대 멀리건 확인 요청")
        return self.__receiveIpcChannel.get()

    def requestBattleStart(self, battleStartRequest):
        self.__transmitIpcChannel.put(battleStartRequest)
        return self.__receiveIpcChannel.get()

