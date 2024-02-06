import abc


class BattleFieldFunctionRepository(abc.ABC):

    @abc.abstractmethod
    def saveRoomNumber(self, roomNumber):
        pass

    @abc.abstractmethod
    def getRoomNumber(self):
        pass

    @abc.abstractmethod
    def saveTransmitIpcChannel(self, transmitIpcChannel):
        pass

    @abc.abstractmethod
    def saveReceiveIpcChannel(self, receiveIpcChannel):
        pass

    @abc.abstractmethod
    def requestSurrender(self, surrenderRequest):
        pass

    @abc.abstractmethod
    def requestTurnEnd(self, turnEndRequest):
        pass

    @abc.abstractmethod
    def requestUseUnitCard(self, useUnitCardRequest):
        pass

    @abc.abstractmethod
    def requestUnitAttack(self, unitAttackRequest):
        pass

    @abc.abstractmethod
    def requestUseEnergyCard(self, useEnergyCardRequest):
        pass

    @abc.abstractmethod
    def requestUseSpecialEnergyCard(self, useSpecialEnergyCardRequest):
        pass

    @abc.abstractmethod
    def requestUseEnvironmentCard(self, useEnvironmentCardRequest):
        pass

    @abc.abstractmethod
    def requestUseItemCard(self, useItemCardRequest):
        pass


    @abc.abstractmethod
    def requestUseSupportCard(self, useSupportCardRequest):
        pass

    @abc.abstractmethod
    def requestUseToolCard(self, useToolCardRequest):
        pass

    @abc.abstractmethod
    def requestUseTrapCard(self, useTrapCardRequest):
        pass




