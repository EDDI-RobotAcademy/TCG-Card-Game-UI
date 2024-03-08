from common.protocol import CustomProtocol
from common.skill_type import SkillType


class RequestAttackMainCharacterWithActiveSkill:
    def __init__(self, _sessionInfo, _unitCardIndex, _targetGameMainCharacterIndex):
        self.__protocolNumber = CustomProtocol.ATTACK_MAIN_CHARACTER_WITH_ACTIVE_SKILL.value
        self.__unitCardIndex = str(_unitCardIndex)
        self.__targetGameMainCharacterIndex = _targetGameMainCharacterIndex
        self.__usageSkillIndex = str(SkillType.TARGET_ONE.value)
        self.__sessionInfo = _sessionInfo

    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber,
            "unitCardIndex": self.__unitCardIndex,
            "usageSkillIndex": self.__usageSkillIndex,
            "targetGameMainCharacterIndex": self.__targetGameMainCharacterIndex,
            "sessionInfo": self.__sessionInfo
        }

    def __str__(self):
        return (f"RequestAttackMainCharacter(protocolNumber={self.__protocolNumber}, "
                f"unitCardIndex={self.__unitCardIndex}, "
                f"usageSkillIndex={self.__usageSkillIndex}, "
                f"targetGameMainCharacterIndex={self.__targetGameMainCharacterIndex}, "
                f"sessionInfo={self.__sessionInfo})")
