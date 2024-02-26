import unittest

from battle_field_function.repository.battle_field_function_repository_impl import BattleFieldFunctionRepositoryImpl
from battle_field_function.service.request.surrender_request import SurrenderRequest


class TestBattleFieldFunction(unittest.TestCase):

    def test_battle_field_function(self):
        surrenderReqeust = SurrenderRequest("abcbabcb")
        BattleFieldFunctionRepositoryImpl.getInstance().requestSurrender(surrenderReqeust)