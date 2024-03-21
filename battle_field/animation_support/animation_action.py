from enum import Enum


# 애니메이션을 넣는다고 하면 카드 아이디로 맞추는 것이 좋을 것이라 봄
class AnimationAction(Enum):
    DUMMY = -1

    DEATH_SCYTHE = 8
    ENERGY_BURN = 9

    CONTRACT_OF_DOOM = 25
    
    CORPSE_EXPLOSION = 33