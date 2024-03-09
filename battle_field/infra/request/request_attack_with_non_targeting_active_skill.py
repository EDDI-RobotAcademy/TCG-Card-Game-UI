from common.protocol import CustomProtocol
from common.skill_type import SkillType


class RequestAttackWithNonTargetingActiveSkill:
    def __init__(self, _sessionInfo, _unitCardIndex):
        self.__protocolNumber = CustomProtocol.ATTACK_WITH_NON_TARGETING_ACTIVE_SKILL.value
        self.__unitCardIndex = str(_unitCardIndex)
        self.__usageSkillIndex = str(SkillType.ALL_ENEMY_UNITS.value)
        self.__sessionInfo = _sessionInfo

    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber,
            "sessionInfo": self.__sessionInfo,
            "unitCardIndex": self.__unitCardIndex,
            "usageSkillIndex": self.__usageSkillIndex,
        }

    def __str__(self):
        return f"RequestAttackWithNonTargetingActiveSkill(protocolNumber={self.__protocolNumber}, unitCardIndex={self.__unitCardIndex}, usageSkillIndex={self.__usageSkillIndex}, sessionInfo={self.__sessionInfo})"
