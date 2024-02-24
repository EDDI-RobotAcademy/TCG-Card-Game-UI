from tests.ljs.test_notify_function.test_battle_field_function.controller.battle_field_function_controller import BattleFieldFunctionController
from tests.ljs.test_notify_function.test_battle_field_function.service.battle_field_function_service_impl import BattleFieldFunctionServiceImpl


class BattleFieldFunctionControllerImpl(BattleFieldFunctionController):
    __instance = None
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__battleFieldFunctionService = BattleFieldFunctionServiceImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def callSurrender(self, switchFrameWithMenuName=None):
        self.__battleFieldFunctionService.surrender(switchFrameWithMenuName)

    def callShuffleDeck(self):
        pass

    def callFirstTurnDrawCard(self):
        pass

    def callDrawCard(self):
        pass

    def useCard(self, cardId):
        pass

    def callTurnEnd(self):
        self.__battleFieldFunctionService.turnEnd()

    def callGameEndReward(self):
        self.__battleFieldFunctionService.gameEndReward()