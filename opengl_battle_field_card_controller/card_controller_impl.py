from common.card_type import CardType
from opengl_battle_field_card_controller.card_controller import CardController
from opengl_battle_field_energy.energy_card import EnergyCard
from opengl_battle_field_environment.environment_card import EnvironmentCard
from opengl_battle_field_item.item_card import ItemCard
from opengl_battle_field_support.support_card import SupportCard
from opengl_battle_field_tool.tool_card import ToolCard
from opengl_battle_field_trap.trap_card import TrapCard


class CardControllerImpl(CardController):
    __instance = None
    __cardTypeTable = {}

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

            cls.__cardTypeTable[
                CardType.ITEM.value] = cls.__instance.itemCardInitShapes

            cls.__cardTypeTable[
                CardType.TRAP.value] = cls.__instance.trapCardInitShapes

            cls.__cardTypeTable[
                CardType.SUPPORT.value] = cls.__instance.supportCardInitShapes

            cls.__cardTypeTable[
                CardType.TOOL.value] = cls.__instance.toolCardInitShapes

            cls.__cardTypeTable[
                CardType.ENERGY.value] = cls.__instance.energyCardInitShapes

            cls.__cardTypeTable[
                CardType.ENVIRONMENT.value] = cls.__instance.environmentCardInitShapes


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
        print("unitCardInitShapes 생성")
        itemCard = ItemCard(local_translation)
        itemCard.init_shapes()
        return itemCard.get_shapes()

    def trapCardInitShapes(self, local_translation):
        print("trapCardInitShapes 생성")
        trapCard = TrapCard(local_translation)
        trapCard.init_shapes()
        return trapCard.get_shapes()

    def supportCardInitShapes(self, local_translation):
        print("supplyCardInitShapes 생성")
        supportCard = SupportCard(local_translation)
        supportCard.init_shapes()
        return supportCard.get_shapes()

    def toolCardInitShapes(self, local_translation):
        print("toolCardInitShapes 생성")
        toolCard = ToolCard(local_translation)
        toolCard.init_shapes()
        return toolCard.get_shapes()

    def energyCardInitShapes(self, local_translation):
        print("energyCardInitShapes 생성")
        energyCard = EnergyCard(local_translation)
        energyCard.init_shapes()
        return energyCard.get_shapes()

    def environmentCardInitShapes(self, local_translation):
        print("environmentCardInitShapes 생성")
        environmentCard = EnvironmentCard(local_translation)
        environmentCard.init_shapes()
        return environmentCard.get_shapes()