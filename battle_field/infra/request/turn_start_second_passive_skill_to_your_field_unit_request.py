from common.protocol import CustomProtocol


# {"protocolNumber":2010, "unitCardIndex": "0", "opponentTargetCardIndex": "0", "usageSkillIndex": "2", "sessionInfo":""}
class TurnStartSecondPassiveSkillToYourFieldUnitRequest:
    def __init__(self, _sessionInfo, _unitCardIndex, _opponentTargetCardIndex, _usageSkillIndex):
        self.__protocolNumber = CustomProtocol.TURN_START_SECOND_PASSIVE_SKILL_TO_YOUR_FIELD_UNIT.value
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
        return (f"WideAreaPassiveSkillFromDeployRequest("
                f"protocolNumber={self.__protocolNumber}, "
                f"unitCardIndex={self.__unitCardIndex}, "
                f"targetGameMainCharacterIndex={self.__targetGameMainCharacterIndex}, "
                f"usageSkillIndex={self.__usageSkillIndex}, "
                f"sessionInfo={self.__sessionInfo})")
