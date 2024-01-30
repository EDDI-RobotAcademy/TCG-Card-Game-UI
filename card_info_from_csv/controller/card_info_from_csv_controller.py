import abc

class CardInfoFromCsvController(abc.ABC):

    @abc.abstractmethod
    def requestToCardInfoSettingInMemory(self):
        pass
