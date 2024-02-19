class SupportCardHandler:
    __instance = None

    # 에너지 부스트(2), 덱 드로우(20), 유닛 검색(30), 상대 필드 에너지 파괴(36)
    __supportCardHandlerTable = {}

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

            cls.__instance.__supportCardHandlerTable[2] = cls.__instance.energy_boost_from_deck_as_possible
            cls.__instance.__supportCardHandlerTable[20] = cls.__instance.draw_card_from_deck
            cls.__instance.__supportCardHandlerTable[30] = cls.__instance.search_unit_from_deck
            cls.__instance.__supportCardHandlerTable[36] = cls.__instance.destroy_opponent_field_energy
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def getSupportCardHandler(self, card_id):
        print("cardType을 찾아 옵니다")
        if self.__supportCardHandlerTable[card_id] is not None:
            return self.__supportCardHandlerTable[card_id]
        else:
            print(f"이 카드 타입({card_id}) 를 처리 할 수 있는 함수가 없습니다.")

    def energy_boost_from_deck_as_possible(self):
        print("에너지 부스팅")
        pass

    def draw_card_from_deck(self):
        print("덱에서 드로우")
        pass

    def search_unit_from_deck(self):
        print("덱에서 유닛 검색")
        pass

    def destroy_opponent_field_energy(self):
        print("상대의 필드 에너지를 파괴합니다")
        pass
