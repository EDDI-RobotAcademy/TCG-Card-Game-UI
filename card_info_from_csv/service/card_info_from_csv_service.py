import abc


class CardInfoFromCsvService(abc.ABC):

    @abc.abstractmethod
    def cardInfoSettingInMemory(self):
        pass