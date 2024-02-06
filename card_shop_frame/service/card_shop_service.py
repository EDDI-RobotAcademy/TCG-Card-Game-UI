import abc


class CardShopMenuFrameService(abc.ABC):
    @abc.abstractmethod
    def createCardShopUiFrame(self, rootWindow, switchFrameWithMenuName):
        pass

    @abc.abstractmethod
    def button_emp(self):
        pass

    @abc.abstractmethod
    def restore_frame(self, original_state):
        pass
