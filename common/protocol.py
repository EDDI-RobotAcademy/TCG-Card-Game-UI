from enum import Enum
from enum import Enum


class CustomProtocol(Enum):
    ACCOUNT_REGISTER = 1
    ACCOUNT_LOGIN = 2

    SESSION_LOGIN = 3

    BATTLE_WAIT_QUEUE_FOR_MATCH = 11
    BATTLE_READY = 12
    CANCEL_MATCH = 13 #13
    CHECK_BATTLE_PREPARE = 14 #14
    WHAT_IS_THE_ROOM_NUMBER = 15 #15
    BATTLE_DECK_LIST = 16 #16
    BATTLE_START_SHUFFLED_GAME_DECK_CARD_LIST = 17 #17
    CHANGE_FIRST_HAND = 18
    ROCKPAPERSCISSORS = 19
    CHECK_ROCKPAPERSCISSORS_WINNER = 20
    REAL_BATTLE_START = 21
    CHECK_OPPONENT_MULLIGAN = 22

    ACCOUNT_CARD_LIST = 31
    ACCOUNT_DECK_REGISTER = 41

    SHOP_DATA = 71
    SHOP_GACHA = 72
    FREE_GACHA = 73
    EVENT_DISTRIBUTE_CARDS = 90

    SEARCH_CARD_BY_SUPPORT_CARD = 501

    ATTACK_UNIT = 1000
    ATTACK_UNIT_WITH_ACTIVE_SKILL = 1001

   # MULLIGAN_CARD = 1012

    ATTACK_WITH_NON_TARGETING_ACTIVE_SKILL = 1002
    ATTACH_FIELD_ENERGY = 1003
    DEPLOY_UNIT_CARD = 1004
    USE_ENERGY_BOOST_SUPPORT_CARD = 1005
    # USE_TRAP_CARD = 1006
    USE_DEATH_SICE = 1006
    # USE_TOOL_CARD = 1007
    CONTRACT_OF_DOOM = 1007
    # USE_ENVIRONMENT_CARD = 1008
    USE_FIELD_ENERGY_REMOVE_ITEM_CARD = 1008
    USE_FIELD_ENERGY_INCREMENT_WITH_SACRIFICE_UNIT_ITME_CARD = 1009
    USE_ENERGY_CARD = 1010
    # USE_SPECIAL_ENERGY_CARD = 1011
    SEARCH_UNIT_CARD = 1011
    USE_SPECIAL_ENERGY_CARD = 1012
    DRAW_CARD_BY_SUPPORT_CARD = 1013
    USE_CORPSE_EXPLOSION = 1014
    USE_ENERGY_BURN = 1015
    ATTACK_MAIN_CHARACTER = 1016

    ATTACK_MAIN_CHARACTER_WITH_ACTIVE_SKILL = 1017

    UNIT_ATTACK = 1021
    UNIT_FIRST_SKILL = 1022
    UNIT_SECOND_SKILL = 1023

    SECOND_PASSIVE_TARGETING_SKILL_YOUR_FIELD_UNIT_FROM_DEPLOY = 2000
    SECOND_PASSIVE_TARGETING_SKILL_MAIN_CHARACTER_FROM_DEPLOY = 2001
    FIRST_PASSIVE_WIDE_AREA_SKILL_FROM_DEPLOY = 2002

    TURN_START_SECOND_PASSIVE_SKILL_TO_YOUR_FIELD_UNIT = 2010
    TURN_START_SECOND_PASSIVE_SKILL_TO_MAIN_CHARACTER = 2011
    TURN_START_FIRST_PASSIVE_WIDE_AREA_SKILL = 2012

    TURN_END = 3333
    BATTLE_FINISH = 4442
    SURRENDER = 4443
    PROGRAM_EXIT = 4444

    CREATE_FAKE_BATTLE_ROOM = 8001
    FAKE_MULTI_DRAW = 8003



