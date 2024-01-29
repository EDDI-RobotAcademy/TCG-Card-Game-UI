import abc


class BattleFieldFunctionController(abc.ABC):

    @abc.abstractmethod
    def callSurrender(self, switchFrameWithMenuName):
        pass