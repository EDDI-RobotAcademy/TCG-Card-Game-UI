from enum import Enum


class OpponentFieldAreaAction(Enum):
    Dummy = 0
    REQUIRE_ENERGY_TO_USAGE = 1
    ENERGY_BURN = 2
    GENERAL_ATTACK_TO_TARGETING_ENEMY = 3
    SKILL_TARGETING_ENEMY = 4


