from alpha_background.entity.alpha_background import AlphaBackground
from alpha_background.repository.alpha_background_repository import AlphaBackgroundRepository


class AlphaBackgroundRepositoryImpl(AlphaBackgroundRepository):
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

    def createAlphaBackground(self, rootWindow):
        print("AlphaBackgroundRepositoryImpl: createAlphaBackground()")
        alphBackgroundFrame = AlphaBackground(rootWindow)

        return alphBackgroundFrame