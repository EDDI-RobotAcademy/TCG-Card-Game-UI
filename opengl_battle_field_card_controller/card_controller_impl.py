from common.card_type import CardType
from opengl_battle_field_card_controller.card_controller import CardController
from opengl_battle_field_item.item_card import ItemCard


class CardControllerImpl(CardController):
    __instance = None
    __cardTypeTable = {}

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__cardTypeTable[
                CardType.ITEM.value] = cls.__instance.itemCardInitShapes


    def __init__(self):
        print("CardControllerImpl 생성")


    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def getCardTypeTable(self, cardType):
        print("cardType을 찾아 옵니다")
        if self.__cardTypeTable[cardType] is not None:
            return self.__cardTypeTable[cardType]
        else:
            print(f"이 카드 타입({cardType}) 를 처리 할 수 있는 함수가 없습니다.")

    def itemCardInitShapes(self, local_translation):
        print("unitCardInitShapes 실행")
        itemCard = ItemCard(local_translation)
        itemCard.init_shapes()
        return itemCard.get_shapes()
