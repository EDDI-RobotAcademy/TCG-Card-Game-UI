from math import ceil

from battle_field.state.current_hand import CurrentHandState
from battle_field.state.your_hand_page import YourHandPage
from image_shape.circle_image import CircleImage
from opengl_battle_field_pickable_card.pickable_card import PickableCard
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage


class LegacyYourHandRepository:
    __instance = None

    preDrawedImageInstance = PreDrawedImage.getInstance()

    total_width = None
    total_height = None

    current_hand_state = CurrentHandState()
    current_hand_card_list = []
    current_hand_card_x_position = []
    your_hand_page_list = []

    x_base = 0
    x_base_muligun = 120  # 멀리건에서의 맨 처음 카드 위치.

    __transmitIpcChannel = None
    __receiveIpcChannel = None

    current_page = 0

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

    def save_current_hand_state(self, hand_list):
        self.current_hand_state.add_to_hand(hand_list)
        print(f"Saved current hand state: {hand_list}")

        # self.make_hand_card_list_location(len(hand_list))

    # def make_hand_card_list_location(self, card_length):
    #     current_x = self.x_base
    #     increment_x_position = 135
    #
    #     for i in range(card_length):
    #         self.current_hand_card_x_position.append((current_x + increment_x_position * i, 830))

    def get_current_hand_state(self):
        return self.current_hand_state.get_current_hand()

    def create_additional_hand_card_list(self, card_list):
        current_hand_card_list_length = len(self.current_hand_card_list)

        self.save_current_hand_state(card_list)

        for index, card_id in enumerate(card_list):
            print(f"index: {index}, card_number: {card_id}")
            initial_position = self.get_next_card_position(current_hand_card_list_length + index)
            new_card = PickableCard(local_translation=initial_position)
            new_card.init_card(card_id)
            # new_card.set_initial_position(initial_position)
            self.current_hand_card_list.append(new_card)

    def create_hand_card_list(self):
        current_hand = self.get_current_hand_state()
        print(f"current_hand: {current_hand}")

        for index, card_number in enumerate(current_hand):
            print(f"index: {index}, card_number: {card_number}")
            initial_position = self.get_next_card_position(index)
            new_card = PickableCard(local_translation=initial_position)
            new_card.init_card(card_number)
            # new_card.set_initial_position(initial_position)
            self.current_hand_card_list.append(new_card)

    def remove_card_by_index(self, card_placed_index):
        if 0 <= card_placed_index < len(self.current_hand_card_list):
            del self.current_hand_card_list[card_placed_index]
            self.current_hand_state.remove_hand_by_index(card_placed_index)

            # self.current_hand_card_list.insert(card_placed_index, None)

            print(
                f"Removed card index {card_placed_index} -> current_hand_list: {self.current_hand_card_list}, current_hand_state: {self.get_current_hand_state()}")
        else:
            print(f"Invalid index: {card_placed_index}. 지울 것이 없다.")

    # 멀리건 화면에서의 카드 리스트
    def create_hand_card_list_muligun(self):
        current_hand = self.get_current_hand_state()
        print(f"current_hand: {current_hand}")

        for index, card_number in enumerate(current_hand):
            print(f"index: {index}, card_number: {card_number}")
            initial_position = self.get_start_hand_card_position(index)
            new_card = PickableCard(local_translation=initial_position, scale=300)
            new_card.init_card_scale(card_number)
            self.current_hand_card_list.append(new_card)

    def remove_card_by_id(self, card_id):
        card_list = self.get_current_hand_card_list()

        for card in card_list:
            if card.get_card_number() == card_id:
                card_list.remove(card)

        self.current_hand_state.remove_from_hand(card_id)

        print(
            f"after clear -> current_hand_list: {self.current_hand_card_list}, current_hand_state: {self.get_current_hand_state()}")

    def remove_card_by_multiple_index(self, card_index_list):
        for index in sorted(card_index_list, reverse=True):
            if 0 <= index < len(self.current_hand_card_list):
                # Remove the card from the list
                del self.current_hand_card_list[index]

                # Update the state to remove the card at the corresponding index
                self.current_hand_state.remove_hand_by_index(index)
            else:
                print(f"Invalid index: {index}. No card removed for this index.")

        print(
            f"Removed cards at indices {card_index_list} -> current_hand_list: {self.current_hand_card_list}, current_hand_state: {self.get_current_hand_state()}")

    # 1848 기준 -> 1848 - 105 * 5 + 170 * 4 = 643
    # 643 / 2 = 321.5
    # 321.5 / 1848 = 17.4% => 0.174
    def get_next_card_position(self, index):
        # TODO: 배치 간격 고려
        current_y = 830
        x_increment = 170
        next_x = self.x_base + x_increment * index
        return (next_x, current_y)

    # 멀리건 화면에서 카드 배치
    def get_start_hand_card_position(self, index):
        current_y = 300
        x_increment = 340
        next_x = self.x_base_muligun + x_increment * index
        return (next_x, current_y)

    def get_current_hand_card_list(self):
        return self.current_hand_card_list

    def replace_hand_card_position(self):
        current_y = 830
        x_increment = 170

        current_hand = self.get_current_hand_state()
        for index, current_hand_card in enumerate(self.current_hand_card_list):
            try:
                next_x = self.x_base + x_increment * index
                local_translation = (next_x, current_y)
                # print(f"replace_hand_card_position -> local_translation: {local_translation}")

                tool_card = current_hand_card.get_tool_card()
                tool_card.local_translate(local_translation)
                # tool_intiial_vertices = tool_card.get_initial_vertices()
                # tool_card.update_vertices(tool_intiial_vertices)

                pickable_card_base = current_hand_card.get_pickable_card_base()
                pickable_card_base.local_translate(local_translation)

                for attached_shape in pickable_card_base.get_attached_shapes():
                    # if isinstance(attached_shape, CircleImage):
                    #     # TODO: 동그라미는 별도 처리해야함
                    #     attached_circle_shape_initial_center = attached_shape.get_initial_center()
                    #     attached_shape.update_circle_vertices(attached_circle_shape_initial_center)
                    #     continue

                    attached_shape.local_translate(local_translation)
                    # attached_shape_intiial_vertices = attached_shape.get_initial_vertices()
                    # attached_shape.update_vertices(attached_shape_intiial_vertices)

                # current_hand_card.change_local_translation((next_x, current_y)

            except Exception as e:
                print(f"Error creating card: {e}")
                pass


    def find_index_by_selected_object(self, selected_object):
        for index, card in enumerate(self.current_hand_card_list):
            if card == selected_object:
                return index
        return -1

    def next_your_hand_page(self):
        if self.current_page == len(self.your_hand_page_list) - 1:
            return

        self.current_page += 1

    def prev_your_hand_page(self):
        if self.current_page == 0:
            return

        self.current_page -= 1

    def get_current_your_hand_page(self):
        return self.current_page

    def get_current_page_your_hand_list(self):
        return self.your_hand_page_list[self.get_current_your_hand_page()].get_your_hand_page_card_object_list()

    def build_your_hand_page(self):
        your_hand_list = self.get_current_hand_state()

        num_cards_per_page = 5
        num_pages = ceil(len(your_hand_list) / num_cards_per_page)

        for page_index in range(num_pages):
            start_index = page_index * num_cards_per_page
            end_index = (page_index + 1) * num_cards_per_page
            current_your_hand_page = your_hand_list[start_index:end_index]

            current_page = YourHandPage()
            current_page.set_total_window_size(self.total_width, self.total_height)
            current_page.add_hand_to_page(current_your_hand_page)
            current_page.set_hand_page_number(page_index + 1)
            self.create_hand_card_list()

            self.your_hand_page_list.append(current_page)

    def requestDrawCardByUseSupportCard(self, drawCardRequest):
        # todo : 테스트용 코드입니다. 추후에 아래의 put/get 방식으로 변경할 필요가 있습니다.
        return [93, 93, 93]
        # self.__transmitIpcChannel.put(drawCardRequest)
        # return self.__receiveIpcChannel.get()

    def saveReceiveIpcChannel(self, receiveIpcChannel):
        self.__receiveIpcChannel = receiveIpcChannel

    def saveTransmitIpcChannel(self, transmitIpcChannel):
        self.__transmitIpcChannel = transmitIpcChannel

    # TODO: 현재는 테스트용인데 구조가 좋지 않으므로 변경이 필요함
    def request_fake_muligun(self, muligun_request):
        self.__transmitIpcChannel.put(muligun_request)
        return self.__receiveIpcChannel.get()
