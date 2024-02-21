from battle_field.entity.battle_field_environment import BattleFieldEnvironment
from battle_field.entity.opponent_deck import OpponentDeck
from battle_field.entity.opponent_hand_panel import OpponentHandPanel
from battle_field.entity.opponent_lost_zone import OpponentLostZone
from battle_field.entity.opponent_main_character import OpponentMainCharacter
from battle_field.entity.opponent_tomb import OpponentTomb
from battle_field.entity.opponent_trap import OpponentTrap
from battle_field.entity.opponent_unit_field import OpponentUnitField
from battle_field.entity.turn_end_button import TurnEndButton
from battle_field.entity.your_deck import YourDeck
from battle_field.entity.your_hand_panel import YourHandPanel
from battle_field.entity.your_lost_zone import YourLostZone
from battle_field.entity.your_main_character import YourMainCharacter
from battle_field.entity.your_tomb import YourTomb
from battle_field.entity.your_trap import YourTrap
from battle_field.entity.your_unit_field import YourUnitField
from battle_field.infra.battle_field_repository import BattleFieldRepository
from battle_field_muligun.entity.background.battle_field_muligun_background import BattleFieldMuligunBackground


class BattleFieldMuligunScene:
    __battle_field_repository = BattleFieldRepository.getInstance()

    def __init__(self):
        self.battle_field_muligun_background = None

    def create_battle_field_muligun_scene(self, width, height):
        print(f"create_battle_field_muligun_scene() -> width: {width}, height: {height}")
        self.create_battle_field_muligun_background(width, height)

    def create_battle_field_muligun_background(self, width, height):
        print(f"create_battle_field_muligun_background() -> width: {width}, height: {height}")
        self.battle_field_muligun_background = BattleFieldMuligunBackground()
        self.battle_field_muligun_background.init_shapes(width, height)

    def get_battle_field_muligun_background(self):
        print("get_battle_field_muligun_background()")
        return self.battle_field_muligun_background.get_battle_field_muligun_background_shape_list()

