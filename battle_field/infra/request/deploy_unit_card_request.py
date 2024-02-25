from common.protocol import CustomProtocol


class DeployUnitCardRequest:
    def __init__(self, sessionInfo, unitId):
        self.__protocolNumber = CustomProtocol.DEPLOY_UNIT_CARD.value
        self.__unitId = str(unitId)
        self.__sessionInfo = sessionInfo

    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber,
            "unitId": self.__unitId,
            "sessionInfo": self.__sessionInfo
        }

    def __str__(self):
        return f"DrawCardByUseSupportCardRequest(protocolNumber={self.__protocolNumber}, unitId={self.__unitId}, sessionInfo={self.__sessionInfo})"
