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
        print("registerCardInfo 찾기")
        card = pd.read_csv('../../../local_storage/card/data.csv')
        findCardInfo = card.loc[(card['백로그번호'] == cardNumber)].to_dict(orient='list')

        card_type = findCardInfo['종류'][0]
        card_name = findCardInfo['카드명'][0]
        card_race = findCardInfo['종족'][0]
        card_energy = findCardInfo['공격 준비 에너지'][0]
        if card_type == '유닛':
            card_health = findCardInfo['체력(유닛)'][0]
            card_attack = findCardInfo['공격력(유닛)'][0]
        else:
            card_health = findCardInfo['종류'][0]
            card_attack = None
        return CardInfo(card_type, card_name, card_race, card_health, card_attack, card_energy)



