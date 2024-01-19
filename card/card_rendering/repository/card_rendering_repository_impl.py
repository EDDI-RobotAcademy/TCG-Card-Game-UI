from card.card_rendering.entity.card_rendering_entity import CardInfo
from card.card_rendering.repository.card_rendering_repository import CardRenderingRepository
import pandas as pd

class CardRenderingRepositoryImpl(CardRenderingRepository):
    __instance = None


    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def registerCardInfo(self, cardNumber):
        card = pd.read_csv('../../../local_storage/card/data.csv')
        print(card)
        findCardInfo = card.loc[(card['백로그번호'] == cardNumber)]
        print(findCardInfo)



