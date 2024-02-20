from battle_field.infra.your_deck_repository import YourDeckRepository
from battle_field.infra.your_field_unit_repository import YourFieldUnitRepository


class SupportCardHandler:
    __instance = None

    # 에너지 부스트(2), 덱 드로우(20), 유닛 검색(30), 상대 필드 에너지 파괴(36)
    __supportCardHandlerTable = {}

    __yourDeckRepository = YourDeckRepository.getInstance()
    __yourFieldUnitRepository = YourFieldUnitRepository.getInstance()

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
        print(f"cardType을 찾아 옵니다 -> card_id: {card_id}")
        if self.__supportCardHandlerTable[card_id] is not None:
            return self.__supportCardHandlerTable[card_id]
        else:
            print(f"이 카드 타입({card_id}) 를 처리 할 수 있는 함수가 없습니다.")

    def energy_boost_from_deck_as_possible(self, target_unit_index):
        print("에너지 부스팅")

        print(f"deck state: {self.__yourDeckRepository.get_current_deck_state().get_current_deck()}")
        found_list = self.__yourDeckRepository.find_card_from_deck(93, 2)
        print(f"found_list: {found_list}")
        self.__yourFieldUnitRepository.attach_energy(target_unit_index, len(found_list))

        print(f"attached energy info: {self.__yourFieldUnitRepository.get_attached_energy_info().get_energy_at_index(target_unit_index)}")
        print(f"deck state: {self.__yourDeckRepository.get_current_deck_state().get_current_deck()}")

    def draw_card_from_deck(self):
        print("덱에서 드로우")
        return 3

    def search_unit_from_deck(self):
        print("덱에서 유닛 검색")
        pass

    def destroy_opponent_field_energy(self):
        print("상대의 필드 에너지를 파괴합니다")
        pass
