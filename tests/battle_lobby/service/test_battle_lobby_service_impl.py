import unittest

from future.moves import tkinter
from battle_lobby_frame.repository.battle_lobby_frame_repository_impl import BattleLobbyFrameRepositoryImpl
from battle_lobby_frame.service.battle_lobby_frame_service_impl import BattleLobbyFrameServiceImpl


class TestBattleLobbyServiceImpl(unittest.TestCase):
    __battleLobbyFrameRepository = BattleLobbyFrameRepositoryImpl.getInstance()
    __battleLobbyFrameService = BattleLobbyFrameServiceImpl.getInstance()

    def test_battle_lobby_service_impl(self):
        requestData = [{'deckName': "ㅁㄴㅇㄻㄴㅇㄹ"}, {'deckName': "123123"}, {'deckName': "568567858"}, {'deckName': "ㅋㅋㅋㅋㅋㅋㅋ"},
                   {'deckName': "ㅋ시발 "}, {'deckName': "되냐??"}]
        battleLobbyFrame = tkinter.Tk()


        self.__battleLobbyFrameService.createBattleLobbyMyDeckButton(requestData)



        battleLobbyFrame.mainloop()


if __name__ == '__main__':
    unittest.main()
