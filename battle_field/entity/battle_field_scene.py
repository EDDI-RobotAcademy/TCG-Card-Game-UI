from battle_field.entity.battle_field_background import BattleFieldBackground
from battle_field.infra.battle_field_repository import BattleFieldRepository
from battle_field_muligun.entity.background.battle_field_muligun_background import BattleFieldMuligunBackground


class BattleFieldScene:
    def __init__(self):
        self.battle_field_background = None

    def create_battle_field_cene(self, width, height):
        print(f"create_battle_field_scene() -> width: {width}, height: {height}")
        self.create_battle_field_background(width, height)

    def create_battle_field_background(self, width, height):
        print(f"create_battle_field_background() -> width: {width}, height: {height}")
        self.battle_field_background = BattleFieldBackground()
        self.battle_field_background.init_shapes(width, height)

    def get_battle_field_background(self):
        print("get_battle_field_background()")
        return self.battle_field_background.get_battle_field_background_shape_list()

