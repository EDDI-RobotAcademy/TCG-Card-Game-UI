import unittest

from future.moves import tkinter
from battle_lobby_frame.repository.battle_lobby_frame_repository_impl import BattleLobbyFrameRepositoryImpl


class TestBattleLobbyServiceImpl(unittest.TestCase):
    __battleLobbyFrameRepository = BattleLobbyFrameRepositoryImpl.getInstance()

    def test_battle_lobby_service_impl(self):
        request = [{'deckName': "ㅁㄴㅇㄻㄴㅇㄹ"}, {'deckName': "123123"}, {'deckName': "568567858"}, {'deckName': "ㅋㅋㅋㅋㅋㅋㅋ"},
                   {'deckName': "ㅋ시발 "}, {'deckName': "되냐??"}]
        battleLobbyFrame = tkinter.Tk()

        def relX(j):
            return 0.3 if j % 2 == 0 else 0.7

        for i, deckData in enumerate(request):
            deck = tkinter.Label(battleLobbyFrame, text=f"{deckData['deckName']}", font=("Helvetica", 15))
            deck.place(relx=relX(i), rely=0.4 + (i // 2 * 0.15), anchor="center", relwidth=0.25, relheight=0.1)

            def onClick(event, _deck: tkinter.Button):
                self.__battleLobbyFrameRepository.selectDeck(_deck)

            deck.bind("<Button-1>", onClick)
            self.__battleLobbyFrameRepository.addDeckToDeckList(deck)




if __name__ == '__main__':
    unittest.main()
