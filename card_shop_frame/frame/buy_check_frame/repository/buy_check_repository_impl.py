from battle_field_fixed_card.fixed_field_card import FixedFieldCard
from card_shop_frame.frame.buy_check_frame.entity.buy_check_frame import BuyCheckFrame
from card_shop_frame.frame.buy_check_frame.repository.buy_check_repository import BuyCheckRepository
from opengl_battle_field_pickable_card.pickable_card import PickableCard


class BuyCheckRepositoryImpl(BuyCheckRepository):
    __instance = None
    __transmitIpcChannel = None
    __receiveIpcChannel = None
    __randomCardList = None

    total_width = None
    total_height = None

    random_buy_card_object_list = []

    x_left_base_ratio = 0.211
    x_right_base_ratio = 0.784
    y_top_base_ratio = 0.2416
    y_bottom_base_ratio = 0.593

    need_to_redraw = False

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def set_total_window_size(self, width, height):
        self.total_width = width
        self.total_height = height

    def set_need_to_redraw(self, need_to_redraw):
        self.need_to_redraw = need_to_redraw

    def get_need_to_redraw(self):
        return self.need_to_redraw

    def createBuyCheckFrame(self, rootWindow):
        print("BuyCheckRepositoryImpl: createBuyCheckFrame()")
        buyCheckFrame = BuyCheckFrame(rootWindow)

        return buyCheckFrame

    def get_next_card_position(self, index):
        # TODO: 배치 간격 고려
        # 10개 배치 (위 5, 아래 5)
        card_width_ratio = 105 / self.total_width
        place_index = index % 5

        if index > 4:
            current_y = self.total_height * self.y_bottom_base_ratio
        else:
            current_y = self.total_height * self.y_top_base_ratio

        base_x = self.total_width * self.x_left_base_ratio
        x_increment = (self.x_right_base_ratio - self.x_left_base_ratio + card_width_ratio) / 5.0
        next_x = base_x + self.total_width * (x_increment * place_index)
        return (next_x, current_y)

    def create_random_buy_list(self):
        random_buy_list = self.getRandomCardList()
        print(f"create_random_buy_list: {random_buy_list}")

        for index, card_id in enumerate(random_buy_list):
            print(f"index: {index}, card_number: {card_id}")
            new_card = PickableCard(local_translation=self.get_next_card_position(index))
            # new_card.init_random_buy_card(card_id)
            new_card.init_random_buy_card(card_id)
            new_card.set_index(index)
            self.random_buy_card_object_list.append(new_card)

    def clear_random_buy_card_object_list(self):
        self.random_buy_card_object_list = []

    def get_random_buy_card_object_list(self):
        return self.random_buy_card_object_list

    def requestUseGameMoney(self, UseGameMoneyRequest):
        print(f"BuyCheckRepositoryImpl: requestCheckGameMoney() -> {UseGameMoneyRequest}")
        self.__transmitIpcChannel.put(UseGameMoneyRequest)
        return self.__receiveIpcChannel.get()

    def requestBuyRandomCard(self, buyRandomCardRequest):
        print(f"BuyCheckRepositoryImpl: requestBuyRandomCard() -> {buyRandomCardRequest}")

        self.__transmitIpcChannel.put(buyRandomCardRequest)
        return self.__receiveIpcChannel.get()

    def saveTransmitIpcChannel(self, transmitIpcChannel):
        print("BuyCheckRepositoryImpl: saveTransmitIpcChannel()")
        self.__transmitIpcChannel = transmitIpcChannel

    def saveReceiveIpcChannel(self, receiveIpcChannel):
        print("BuyCheckRepositoryImpl: saveReceiveIpcChannel()")
        self.__receiveIpcChannel = receiveIpcChannel

    def setRandomCardList(self, randomCardList):
        print("BuyCheckRepositoryImpl: setRandomCardList()")
        self.__randomCardList = randomCardList
        print(f"{self.__randomCardList}")

    def clearRandomCardList(self):
        self.__randomCardList = []

    def getRandomCardList(self):
        print("BuyCheckRepositoryImpl: getRandomCardList()")
        return self.__randomCardList
