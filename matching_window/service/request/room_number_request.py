from common.protocol import CustomProtocol


class RoomNumberRequest:
    def __init__(self, sessionInfo):
        self.__protocolNumber = CustomProtocol.WHAT_IS_THE_ROOM_NUMBER.value
        self.__sessionInfo = sessionInfo

    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber,
            "sessionInfo": self.__sessionInfo
        }

    def __str__(self):
        return f"RoomNumberRequest(protocolNumber={self.__protocolNumber}, sessionInfo={self.__sessionInfo})"
