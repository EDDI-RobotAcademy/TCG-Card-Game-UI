from card_info_from_csv.entity.card_rendering_entity import Card
from card_info_from_csv.repository.card_rendering_repository import CardRenderingRepository
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

    def readCsvFile(self, filePath):
        print("readCsvFile 찾기")
        cards = []
        dataFile = pd.read_csv(filePath)
        for index, row in dataFile.iterrows():
            card = Card(row['카드명'], row['종족'], row['등급'], row['종류'], row['카드번호'], row['필요_에너지'], row['공격력'], row['체력'])
            cards.append(card.to_dict())

        return cards

    def findCardByNumber(self, cards, cardNumber):
        print("findCardByNumber 실행")
        print(f"{cards}")
        return cards.get(cardNumber)



