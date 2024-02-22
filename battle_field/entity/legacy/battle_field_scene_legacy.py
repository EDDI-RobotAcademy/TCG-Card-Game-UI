from battle_field.entity.legacy.battle_field_environment import BattleFieldEnvironment
from battle_field.entity.legacy.opponent_deck import OpponentDeck
from battle_field.entity.legacy.opponent_hand_panel import OpponentHandPanel
from battle_field.entity.legacy.opponent_lost_zone import OpponentLostZone
from battle_field.entity.legacy.opponent_main_character import OpponentMainCharacter
from battle_field.entity.legacy.opponent_tomb import OpponentTomb
from battle_field.entity.legacy.opponent_trap import OpponentTrap
from battle_field.entity.legacy.opponent_unit_field import OpponentUnitField
from battle_field.entity.legacy.turn_end_button import TurnEndButton
from battle_field.entity.legacy.your_deck import YourDeck
from battle_field.entity.legacy.your_hand_panel import YourHandPanel
from battle_field.entity.legacy.your_lost_zone import YourLostZone
from battle_field.entity.legacy.your_main_character import YourMainCharacter
from battle_field.entity.legacy.your_tomb import YourTomb
from battle_field.entity.legacy.your_trap import YourTrap
from battle_field.entity.legacy.your_unit_field import YourUnitField
from battle_field.infra.battle_field_repository import BattleFieldRepository


class BattleFieldSceneLegacy:
    __battle_field_repository = BattleFieldRepository.getInstance()
    def __init__(self):
        self.opponent_tomb = None
        self.opponent_lost_zone = None
        self.opponent_trap = None
        self.opponent_deck = None
        self.opponent_main_character = None
        self.opponent_hand_panel = None

        self.your_tomb = None
        self.your_lost_zone = None
        self.your_trap = None
        self.your_deck = None
        self.your_main_character = None
        self.your_hand_panel = None

        self.battle_field_environment = None
        self.turn_end_button = None

    def create_battle_field_scene(self):
        self.create_opponent_tomb()
        self.create_opponent_lost_zone()
        self.create_opponent_trap()
        self.create_opponent_deck()
        self.create_opponent_main_character()
        self.create_opponent_hand_panel()
        self.create_opponent_unit_field()

        self.create_your_tomb()
        self.create_your_lost_zone()
        self.create_your_trap()
        self.create_your_deck()
        self.create_your_main_character()
        self.create_your_hand_panel()
        self.create_your_unit_field()

        self.create_battle_field_environment()
        self.create_turn_end_button()

    def create_opponent_tomb(self):
        self.opponent_tomb = OpponentTomb()
        self.opponent_tomb.init_shapes()

    def create_opponent_lost_zone(self):
        self.opponent_lost_zone = OpponentLostZone()
        self.opponent_lost_zone.init_shapes()

    def create_opponent_trap(self):
        self.opponent_trap = OpponentTrap()
        self.opponent_trap.init_shapes()

    def create_opponent_deck(self):
        self.opponent_deck = OpponentDeck()
        self.opponent_deck.init_shapes()

    def create_opponent_main_character(self):
        self.opponent_main_character = OpponentMainCharacter()
        self.opponent_main_character.init_opponent_main_character_shapes()

    def create_opponent_hand_panel(self):
        self.opponent_hand_panel = OpponentHandPanel()
        self.opponent_hand_panel.init_shapes()

    def create_opponent_unit_field(self):
        self.opponent_unit_field = OpponentUnitField()
        self.opponent_unit_field.init_shapes()

    def create_your_tomb(self):
        self.your_tomb = YourTomb()
        self.your_tomb.init_shapes()
        self.__battle_field_repository.add_battle_field_button(button=self.your_tomb)

    def create_your_lost_zone(self):
        self.your_lost_zone = YourLostZone()
        self.your_lost_zone.init_shapes()

    def create_your_trap(self):
        self.your_trap = YourTrap()
        self.your_trap.init_shapes()

    def create_your_deck(self):
        self.your_deck = YourDeck()
        self.your_deck.init_shapes()

    def create_your_main_character(self):
        self.your_main_character = YourMainCharacter()
        self.your_main_character.init_your_main_character_shapes()

    def create_your_hand_panel(self):
        self.your_hand_panel = YourHandPanel()
        self.your_hand_panel.init_shapes()

    def create_your_unit_field(self):
        self.your_unit_field = YourUnitField()
        self.your_unit_field.init_shapes()

    def create_battle_field_environment(self):
        self.battle_field_environment = BattleFieldEnvironment()
        self.battle_field_environment.init_shapes()

    def create_turn_end_button(self):
        self.turn_end_button = TurnEndButton()
        self.turn_end_button.init_shapes()
        self.__battle_field_repository.add_battle_field_button(button=self.turn_end_button)

    def get_opponent_tomb(self):
        return self.opponent_tomb.get_tomb_shapes()

    def get_opponent_lost_zone(self):
        return self.opponent_lost_zone.get_lost_zone_shapes()

    def get_opponent_trap(self):
        return self.opponent_trap.get_trap_shapes()

    def get_opponent_deck(self):
        return self.opponent_deck.get_opponent_deck_shapes()

    def get_opponent_main_character(self):
        return self.opponent_main_character.get_main_character_shapes()

    def get_opponent_hand_panel(self):
        return self.opponent_hand_panel.get_opponent_hand_panel_shapes()

    def get_opponent_unit_field(self):
        return self.opponent_unit_field.get_opponent_unit_field_shapes()

    def get_your_tomb(self):
        return self.your_tomb.get_tomb_shapes()

    def get_your_lost_zone(self):
        return self.your_lost_zone.get_lost_zone_shapes()

    def get_your_trap(self):
        return self.your_trap.get_trap_shapes()

    def get_your_deck(self):
        return self.your_deck.get_your_deck_shapes()

    def get_your_main_character(self):
        return self.your_main_character.get_main_character_shapes()

    def get_your_hand_panel(self):
        return self.your_hand_panel.get_your_hand_panel_shapes()

    def get_your_unit_field(self):
        return self.your_unit_field.get_your_unit_field_shapes()

    def get_battle_field_environment(self):
        return self.battle_field_environment.get_environment_shapes()

    def get_turn_end_button(self):
        return self.turn_end_button.get_turn_end_button_shapes()
