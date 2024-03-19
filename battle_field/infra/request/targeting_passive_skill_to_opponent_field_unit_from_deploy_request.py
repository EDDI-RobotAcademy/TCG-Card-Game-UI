from common.protocol import CustomProtocol


# {"protocolNumber":2000, "unitCardIndex": "0", "opponentTargetCardIndex": "0", "usageSkillIndex": "2", "sessionInfo":""}
class TargetingPassiveSkillToOpponentFieldUnitFromDeployRequest:
    def __init__(self, _sessionInfo, _unitCardIndex, _opponentTargetCardIndex, _usageSkillIndex):
        self.__protocolNumber = CustomProtocol.SECOND_PASSIVE_TARGETING_SKILL_YOUR_FIELD_UNIT_FROM_DEPLOY.value
        self.__unitCardIndex = _unitCardIndex
        self.__opponentTargetCardIndex = _opponentTargetCardIndex
        self.__usageSkillIndex = _usageSkillIndex
        self.__sessionInfo = _sessionInfo

    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber,
            "unitCardIndex": self.__unitCardIndex,
            "opponentTargetCardIndex": self.__opponentTargetCardIndex,
            "usageSkillIndex": self.__usageSkillIndex,
            "sessionInfo": self.__sessionInfo
        }

    def __str__(self):
        return (f"TargetingPassiveSkillToOpponentFieldUnitFromDeployRequest("
                f"protocolNumber={self.__protocolNumber}, "
                f"unitCardIndex={self.__unitCardIndex}, "
                f"opponentTargetCardIndex={self.__opponentTargetCardIndex}, "
                f"usageSkillIndex={self.__usageSkillIndex}, "
                f"sessionInfo={self.__sessionInfo})")
