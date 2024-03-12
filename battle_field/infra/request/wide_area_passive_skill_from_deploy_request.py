from common.protocol import CustomProtocol


class WideAreaPassiveSkillFromDeployRequest:
    def __init__(self, _sessionInfo, _unitCardIndex, _usageSkillIndex):
        self.__protocolNumber = CustomProtocol.FIRST_PASSIVE_WIDE_AREA_SKILL_FROM_DEPLOY.value
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
