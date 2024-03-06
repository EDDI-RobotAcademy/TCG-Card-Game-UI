from common.protocol import CustomProtocol


class TurnEndRequest:
    def __init__(self, sessionInfo):
        self.__protocolNumber = CustomProtocol.TURN_END.value
      #  self.__roomNumber = BattleFieldFunctionRepositoryImpl.getInstance().getRoomNumber()
        self.__sessionInfo = sessionInfo

    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber,
          #  "roomNumber": self.__roomNumber,
            "sessionInfo": self.__sessionInfo
        }

    def __str__(self):
        #return f"TurnEndRequest(protocolNumber={self.__protocolNumber}, roomNumber={self.__roomNumber}, sessionInfo={self.__sessionInfo})"
        return f"TurnEndRequest(protocolNumber={self.__protocolNumber}, sessionInfo={self.__sessionInfo})"
