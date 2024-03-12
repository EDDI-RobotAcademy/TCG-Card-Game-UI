from common.card_type import CardType
from opengl_battle_field_card_controller.legacy.card_controller import LegacyCardController
from opengl_battle_field_energy.energy_card import EnergyCard
from opengl_battle_field_energy.legacy.energy_card import LegacyEnergyCard
from opengl_battle_field_environment.environment_card import EnvironmentCard
from opengl_battle_field_environment.legacy.environment_card import LegacyEnvironmentCard
from opengl_battle_field_item.item_card import ItemCard
from opengl_battle_field_item.legacy.item_card import LegacyItemCard
from opengl_battle_field_support.legacy.support_card import LegacySupportCard
from opengl_battle_field_support.support_card import SupportCard
from opengl_battle_field_token.token_card import TokenCard
from opengl_battle_field_tool.tool_card import ToolCard
from opengl_battle_field_trap.trap_card import TrapCard
from opengl_battle_field_unit.legacy.unit_card import LegacyUnitCard

circle_radius = 20

class LegacyCardControllerImpl(LegacyCardController):
    __instance = None
    __cardTypeTable = {}

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

            cls.__instance.__cardTypeTable [
                CardType.UNIT.value] = cls.__instance.unitCardInitShapes

            cls.__instance.__cardTypeTable[
                CardType.ITEM.value] = cls.__instance.itemCardInitShapes

            cls.__instance.__cardTypeTable[
                CardType.TRAP.value] = cls.__instance.trapCardInitShapes

            cls.__instance.__cardTypeTable[
                CardType.SUPPORT.value] = cls.__instance.supportCardInitShapes

            cls.__instance.__cardTypeTable[
                CardType.TOOL.value] = cls.__instance.toolCardInitShapes

            cls.__instance.__cardTypeTable[
                CardType.ENERGY.value] = cls.__instance.energyCardInitShapes

            cls.__instance.__cardTypeTable[
                CardType.ENVIRONMENT.value] = cls.__instance.environmentCardInitShapes

            cls.__instance.__cardTypeTable[
                CardType.TOKEN.value] = cls.__instance.tokenCardInitShapes

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    # TODO: 네이밍 이슈 존재함
    def getCardTypeTable(self, card_type):
        print("cardType을 찾아 옵니다")
        if self.__cardTypeTable[card_type] is not None:
            return self.__cardTypeTable[card_type]
        else:
            print(f"이 카드 타입({card_type}) 를 처리 할 수 있는 함수가 없습니다.")

    def unitCardInitShapes(self, local_translation, card_number, rectangle_height, rectangle_width):
        print("unitCardInitShapes 생성")
        unitCard = LegacyUnitCard(local_translation)
        print("카드 생성")
        unitCard.init_shapes(circle_radius, card_number, rectangle_height, rectangle_width)
        print("모양 생성")
        return unitCard.get_shapes()

    def itemCardInitShapes(self, local_translation, card_number, rectangle_height, rectangle_width):
        print("itemCardInitShapes 생성")
        itemCard = LegacyItemCard(local_translation)
        print("카드 생성")
        itemCard.init_shapes(circle_radius, card_number, rectangle_height, rectangle_width)
        print("모양 생성")
        return itemCard.get_shapes()

    def trapCardInitShapes(self, local_translation, card_number, rectangle_height, rectangle_width):
        print("trapCardInitShapes 생성")
        trapCard = TrapCard(local_translation)
        print("카드 생성")
        trapCard.init_shapes(circle_radius, card_number, rectangle_height, rectangle_width)
        print("모양 생성")
        return trapCard.get_shapes()

    def supportCardInitShapes(self, local_translation, card_number, rectangle_height, rectangle_width):
        print("supplyCardInitShapes 생성")
        supportCard = LegacySupportCard(local_translation)
        print("카드 생성")
        supportCard.init_shapes(circle_radius, card_number, rectangle_height, rectangle_width)
        print("모양 생성")
        return supportCard.get_shapes()

    def toolCardInitShapes(self, local_translation, card_number, rectangle_height, rectangle_width):
        print("toolCardInitShapes 생성")
        toolCard = ToolCard(local_translation)
        print("카드 생성")
        toolCard.init_shapes(circle_radius, card_number, rectangle_height, rectangle_width)
        print("모양 생성")
        return toolCard.get_shapes()

    def energyCardInitShapes(self, local_translation, card_number, rectangle_height, rectangle_width):
        print("energyCardInitShapes 생성")
        energyCard = LegacyEnergyCard(local_translation)
        print("카드 생성")
        energyCard.init_shapes(circle_radius, card_number, rectangle_height, rectangle_width)
        print("모양 생성")
        return energyCard.get_shapes()

    def environmentCardInitShapes(self, local_translation, card_number, rectangle_height, rectangle_width):
        print("environmentCardInitShapes 생성")
        environmentCard = LegacyEnvironmentCard(local_translation)
        print("카드 생성")
        environmentCard.init_shapes(circle_radius, card_number, rectangle_height, rectangle_width)
        print("모양 생성")
        return environmentCard.get_shapes()

    def tokenCardInitShapes(self, local_translation, card_number, rectangle_height, rectangle_width):
        print("tokenCardInitShapes 생성")
        tokenCard = TokenCard(local_translation)
        print("카드 생성")
        tokenCard.init_shapes(circle_radius, card_number, rectangle_height, rectangle_width)
        print("모양 생성")
        return tokenCard.get_shapes()