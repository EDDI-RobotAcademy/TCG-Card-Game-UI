from common.protocol import CustomProtocol


# {"protocolNumber":2012, "unitCardIndex": "0", "usageSkillIndex": "1", "sessionInfo":""}
class TurnStartFirstPassiveSkillRequest:
    def __init__(self, _sessionInfo, _unitCardIndex, _usageSkillIndex):
        self.__protocolNumber = CustomProtocol.TURN_START_FIRST_PASSIVE_WIDE_AREA_SKILL.value
        self.__unitCardIndex = _unitCardIndex
        self.__usageSkillIndex = _usageSkillIndex
        self.__sessionInfo = _sessionInfo

    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber,
            "unitCardIndex": self.__unitCardIndex,
            "usageSkillIndex": self.__usageSkillIndex,
            "sessionInfo": self.__sessionInfo
        }

    def __str__(self):
        return (f"WideAreaPassiveSkillFromDeployRequest("
                f"protocolNumber={self.__protocolNumber}, "
                f"unitCardIndex={self.__unitCardIndex}, "
                f"usageSkillIndex={self.__usageSkillIndex}, "
                f"sessionInfo={self.__sessionInfo})")
