from tests.ljs.ugly_test_result_frame.entity.battle_result_frame import BattleResultFrame


class TestResultFrameService:
    __instance = None

    # __fakeBattleFieldFrame = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__battle_result_frame = BattleResultFrame
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def create_battle_result_frame(self, rootWindow, switchFrameWithMenuName):

        battle_result_frame = self.__battle_result_frame(master=rootWindow)

        return battle_result_frame