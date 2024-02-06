from button.buntton_handler.button_handler import ButtonHandler
from button.button_service.create_deck_register_screen import CreateDeckRegisterScreen
from button.button_service.move_to_frame import MoveToFrame
from common.button_type import ButtonType


class ButtonHandlerImpl(ButtonHandler):
    __instance = None
    __buttonTable = {}

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

            cls.__buttonTable[
                ButtonType.DECKREGISTER.value] = cls.__instance.myDeckRegisterScreen

            cls.__buttonTable[
                ButtonType.MOVETOFRAME.value] = cls.__instance.goToLobbyFrame

    def __init__(self):
        print("ButtonHandlerImpl 생성")

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

        return cls.__instance

    def getButtonTypeTable(self, buttonType):
        print("buttonType을 찾아 옵니다")
        print(f"잘 나옴?{self.__buttonTable}")
        if self.__buttonTable[buttonType] is not None:
            return self.__buttonTable[buttonType]
        else:
            print(f"이 버튼 타입({buttonType}) 를 처리 할 수 있는 함수가 없습니다.")

    def myDeckRegisterScreen(self, master, canvas, scene):
        print("덱 생성 화면 만드는 버튼임")
        screen = CreateDeckRegisterScreen(master, canvas, scene)
        screen.createDeckRegisterScreenButton()

    def goToLobbyFrame(self):
        print("로비로 되돌아 가는 버튼임")
        lobby = MoveToFrame()
        lobby.moveToFrameButton("lobby-menu")