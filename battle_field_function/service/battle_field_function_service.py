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
    def mulligan(self):
        pass

    @abc.abstractmethod
    def unitAttack(self):
        pass

    @abc.abstractmethod
    def turnEnd(self):
        pass

    @abc.abstractmethod
    def useEnvironmentCard(self):
        pass

    @abc.abstractmethod
    def useEnergyCard(self):
        pass

    @abc.abstractmethod
    def useSpecialEnergyCard(self):
        pass

    @abc.abstractmethod
    def useItemCard(self):
        pass

    @abc.abstractmethod
    def useSupportCard(self):
        pass

    @abc.abstractmethod
    def useToolCard(self):
        pass

    @abc.abstractmethod
    def useTrapCard(self):
        pass

    @abc.abstractmethod
    def useUnitCard(self):
        pass