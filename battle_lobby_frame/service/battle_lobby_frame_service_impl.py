import tkinter

from battle_lobby_frame.repository.battle_lobby_frame_repository_impl import BattleLobbyFrameRepositoryImpl
from battle_lobby_frame.service.battle_lobby_frame_service import BattleLobbyFrameService
from utility.image_generator import ImageGenerator

from pyopengltk import OpenGLFrame
from OpenGL import GL, GLU, GLUT


# from discarded.battle_room_list_frame.repository import BattleRoomListFrameRepositoryImpl


class BattleLobbyFrameServiceImpl(BattleLobbyFrameService):
    __instance = None
    __battleLobbyFrame = None
    __onClickEventList = []
    __imageGenerator = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__battleLobbyFrameRepository = BattleLobbyFrameRepositoryImpl.getInstance()
            #cls.__instance.__imageGenerator = ImageGenerator.getInstance()
        #  cls.__instance.__battleRoomListFrameRepository = BattleRoomListFrameRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def createBattleLobbyUiFrame(self, rootWindow, switchFrameWithMenuName):
        self.__battleLobbyFrame = self.__battleLobbyFrameRepository.createBattleLobbyFrame(rootWindow)

        label = tkinter.Label(self.__battleLobbyFrame, text="WATING ROOM FOR BATTLE", font=("Helvetica", 50, "bold"),
                              fg="#FFFFFF", bg="#000000")
        label.place(relx=0.5, rely=0.15, anchor="center")

        # TODO: 테스트코드지워야함
        request = [{'deckName': "ㅁㄴㅇㄻㄴㅇㄹ"}, {'deckName': "123123"}, {'deckName': "568567858"}, {'deckName': "ㅋㅋㅋㅋㅋㅋㅋ"},
                   {'deckName': "ㅋ시발 "}, {'deckName': "되냐??"}]

        self.createBattleLobbyMyDeckButton(request)

        enterButton = tkinter.Button(self.__battleLobbyFrame, text="입장", font=("Arial", 20))
        enterButton.place(relx=0.5, rely=0.85, anchor="center", relwidth=0.15, relheight=0.075)

        return self.__battleLobbyFrame

    def createBattleLobbyMyDeckButton(self, request=None):
        imageGenerator = ImageGenerator.getInstance()
        if request:
            def relX(j):
                return 0.3 if j % 2 == 0 else 0.7

            for i, deckData in enumerate(request):
                generatedImage = imageGenerator.getUnselectedDeckImage()
                deck = tkinter.Canvas(self.__battleLobbyFrame, highlightthickness=0, highlightbackground="#93FFE8")
                deck.create_image(150,40, image=generatedImage)


                # deck = tkinter.Label(self.__battleLobbyFrame)
                # deck.configure(image=generatedImage)




                #text = tkinter.Canvas(deck)
                deck.create_text(150, 40, text=deckData["deckName"], font=("Arial",15))
                deck.pack()
                #text = tkinter.Label(deck, text=deckData["deckName"], font=("Arial", 15))

                #text.pack(fill="y", expand=True)
                # deck = tkinter.Label(self.__battleLobbyFrame, text=f"{deckData['deckName']}", font=("Helvetica", 15),
                #                      image=ImageGenerator.getInstance().getDeckImage(), anchor="center")
                                     #image=ImageGenerator.getInstance().generateImageByDirectoryAndName("battle_lobby",
                                     #                                                                  "deck"))

                # deck.place(relx=relX(i), rely=0.4 + (i // 2 * 0.15),
                #            anchor="center", relwidth=0.25, relheight=0.1)

                deck.place(relx=relX(i), rely=0.4 + (i // 2 * 0.15),
                           anchor="center", width=300, height=80)


                def onClick(event, _deck):
                    self.__battleLobbyFrameRepository.selectDeck(_deck)

                deck.bind("<Button-1>", lambda event, current_deck=deck: onClick(event, current_deck))
                self.__battleLobbyFrameRepository.addDeckToDeckList(deck)


    def initgl(self,width,height):
        GL.glClearColor(1.0, 1.0, 1.0, 0.0)
        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
        GL.glLoadIdentity()
        GLU.gluOrtho2D(0, width, height, 0)
        GLUT.glutInit()
