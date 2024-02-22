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

