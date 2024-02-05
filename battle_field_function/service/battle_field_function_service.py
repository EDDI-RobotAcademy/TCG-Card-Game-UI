import abc


class BattleFieldFunctionService(abc.ABC):

    @abc.abstractmethod
    def injectTransmitIpcChannel(self, transmitIpcChannel):
        pass

    @abc.abstractmethod
    def injectReceiveIpcChannel(self, receiveIpcChannel):
        pass

    @abc.abstractmethod
    def surrender(self, switchFrameWithMenuName):
        pass

    @abc.abstractmethod
    def mulligan(self, cardCount):
        pass

    @abc.abstractmethod
    def unitAttack(self, target):
        pass

    @abc.abstractmethod
    def turnEnd(self):
        pass

    @abc.abstractmethod
    def useEnvironmentCard(self, cardNumber):
        pass

    @abc.abstractmethod
    def useEnergyCard(self):
        pass

    @abc.abstractmethod
    def useSpecialEnergyCard(self, cardNumber):
        pass

    @abc.abstractmethod
    def useItemCard(self, cardNumber):
        pass

    @abc.abstractmethod
    def useSupportCard(self, cardNumber):
        pass

    @abc.abstractmethod
    def useToolCard(self, cardNumber):
        pass

    @abc.abstractmethod
    def useTrapCard(self, cardNumber):
        pass

    @abc.abstractmethod
    def useUnitCard(self, cardNumber):
        pass