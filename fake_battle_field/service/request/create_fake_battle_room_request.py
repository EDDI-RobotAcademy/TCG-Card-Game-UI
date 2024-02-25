from common.protocol import CustomProtocol

from decouple import config


class CreateFakeBattleRoomRequest:
    def __init__(self):
        self.__protocolNumber = CustomProtocol.CREATE_FAKE_BATTLE_ROOM.value
        self.__firstFakeTestAccountId = config('FIRST_FAKE_ACCOUNT_ID')
        self.__firstFakeTestPassword = config('FIRST_FAKE_ACCOUNT_PW')
        self.__secondFakeTestAccountId = config('SECOND_FAKE_ACCOUNT_ID')
        self.__secondFakeTestPassword = config('SECOND_FAKE_ACCOUNT_PW')

    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber,
            "firstFakeTestAccountId": self.__firstFakeTestAccountId,
            "firstFakeTestPassword": self.__firstFakeTestPassword,
            "secondFakeTestAccountId": self.__secondFakeTestAccountId,
            "secondFakeTestPassword": self.__secondFakeTestPassword
        }

    def __str__(self):
        return (f"CreateFakeBattleRoomRequest(protocolNumber={self.__protocolNumber}, "
                f"firstFakeTestAccountId={self.__firstFakeTestAccountId}, "
                f"firstFakeTestPassword={self.__firstFakeTestPassword}, "
                f"secondFakeTestAccountId={self.__secondFakeTestAccountId}, "
                f"secondFakeTestPassword={self.__secondFakeTestPassword})")

