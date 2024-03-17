from common.protocol import CustomProtocol
from common.skill_type import SkillType


class RequestAttackToYourFieldUnitWithActiveSkill:
    def __init__(self, _sessionInfo, _unitCardIndex, _opponentTargetCardIndex):
        self.__protocolNumber = CustomProtocol.ATTACK_UNIT_WITH_ACTIVE_SKILL.value
        self.__unitCardIndex = str(_unitCardIndex)
        self.__opponentTargetCardIndex = str(_opponentTargetCardIndex)
        self.__usageSkillIndex = str(SkillType.TARGET_ONE.value)
        self.__sessionInfo = _sessionInfo

    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber,
            "unitCardIndex": self.__unitCardIndex,
            "usageSkillIndex": self.__usageSkillIndex,
            "opponentTargetCardIndex": self.__opponentTargetCardIndex,
            "sessionInfo": self.__sessionInfo
        }

    def __str__(self):
        return (f"RequestAttackMainCharacter(protocolNumber={self.__protocolNumber}, "
                f"unitCardIndex={self.__unitCardIndex}, "
                f"usageSkillIndex={self.__usageSkillIndex}, "
                f"opponentTargetCardIndex={self.__opponentTargetCardIndex}, "
                f"sessionInfo={self.__sessionInfo})")