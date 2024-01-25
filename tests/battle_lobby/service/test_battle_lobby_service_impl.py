import unittest

from future.moves import tkinter
from battle_lobby_frame.repository.battle_lobby_frame_repository_impl import BattleLobbyFrameRepositoryImpl
from battle_lobby_frame.service.battle_lobby_frame_service_impl import BattleLobbyFrameServiceImpl


class TestBattleLobbyServiceImpl(unittest.TestCase):
    __battleLobbyFrameRepository = BattleLobbyFrameRepositoryImpl.getInstance()
    __battleLobbyFrameService = BattleLobbyFrameServiceImpl.getInstance()

    def test_battle_lobby_service_impl(self):
        requestData = {'abc':[{'1': "ㅁㄴㅇㄻㄴㅇㄹ"}, {'2': "123123"}, {'3': "568567858"}, {'4': "ㅋㅋㅋㅋㅋㅋㅋ"},
                   {'5': "ㅋ시발 "}, {'6': "되냐??"}]}
        battleLobbyFrame = tkinter.Tk()


       # self.__battleLobbyFrameService.createBattleLobbyMyDeckButton(requestData)




        battleLobbyFrame.mainloop()
        self.__battleLobbyFrameService.checkTimeForDeckSelection(battleLobbyFrame)


if __name__ == '__main__':
    unittest.main()
