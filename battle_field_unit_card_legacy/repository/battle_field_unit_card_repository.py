import abc


class BattleFieldUnitCardRepository(abc.ABC):
    @abc.abstractmethod
    def create_battle_field_unit_card(self, shapes):
        pass

