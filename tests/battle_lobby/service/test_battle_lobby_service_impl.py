import unittest

from future.moves import tkinter
from battle_lobby_frame.repository.battle_lobby_frame_repository_impl import BattleLobbyFrameRepositoryImpl
from battle_lobby_frame.service.battle_lobby_frame_service_impl import BattleLobbyFrameServiceImpl
from battle_lobby_frame.service.request.request_deck_card_list import RequestDeckCardList
from session.repository.session_repository_impl import SessionRepositoryImpl


class TestBattleLobbyServiceImpl(unittest.TestCase):
    __battleLobbyFrameRepository = BattleLobbyFrameRepositoryImpl.getInstance()
    __battleLobbyFrameService = BattleLobbyFrameServiceImpl.getInstance()
    __sessionRepository = SessionRepositoryImpl.getInstance()

    def test_battle_lobby_service_impl(self):
        __battleLobbyFrameRepository = BattleLobbyFrameRepositoryImpl.getInstance()
        __battleLobbyFrameService = BattleLobbyFrameServiceImpl.getInstance()
        __sessionRepository = SessionRepositoryImpl.getInstance()

        battleLobbyFrame = tkinter.Tk()


       # self.__battleLobbyFrameService.createBattleLobbyMyDeckButton(requestData)





        #self.__battleLobbyFrameService.checkTimeForDeckSelection(battleLobbyFrame)
        response = self.__battleLobbyFrameRepository.requestCardList(
            RequestDeckCardList(1,
                                "eab86cd4-8d5d-492c-81b4-cc53118cd401")
        )
#        self.assertIsNotNone(response)
        battleLobbyFrame.mainloop()


if __name__ == '__main__':
    unittest.main()
