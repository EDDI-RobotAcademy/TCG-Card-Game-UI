from common.protocol import CustomProtocol


class RequestAttackMainCharacter:
    def __init__(self, _sessionInfo, _attacker_unit_index, _target_game_main_character_index):
        self.__protocolNumber = CustomProtocol.ATTACK_MAIN_CHARACTER.value
        self.__attacker_unit_index = str(_attacker_unit_index)
        self.__target_game_main_character_index = _target_game_main_character_index
        self.__sessionInfo = _sessionInfo

    def toDictionary(self):
        return {
            "protocolNumber": self.__protocolNumber,
            "attacker_unit_index": self.__attacker_unit_index,
            "target_game_main_character_index": self.__target_game_main_character_index,
            "sessionInfo": self.__sessionInfo
        }

    def __str__(self):
        return (f"RequestAttackMainCharacter(protocolNumber={self.__protocolNumber}, "
                f"attacker_unit_index={self.__attacker_unit_index}, "
                f"target_game_main_character_index={self.__target_game_main_character_index}, "
                f"sessionInfo={self.__sessionInfo})")
