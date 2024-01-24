from enum import Enum


class CustomProtocol(Enum):
    ACCOUNT_REGISTER = 1
    ACCOUNT_LOGIN = 2

    SESSION_LOGIN = 3

    DECK_NAME_LIST = 11
    ENTER_MATCH = 12
    READY_FOR_BATTLE = 13
    DECK_CARD_LIST = 14

    PROGRAM_EXIT = 4444



