from common.button_type import ButtonType
from opengl_button.button_handler.button_handler_impl import ButtonHandlerImpl
from opengl_my_card_main_frame.entity.my_card_main_scene import MyCardMainScene
from opengl_my_card_main_frame.frame.my_card_main_frame import MyCardMainFrame
from opengl_my_card_main_frame.service.my_card_main_frame_service import MyCardMainFrameService


class MyCardMainFrameServiceImpl(MyCardMainFrameService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__myCardMainFrame = MyCardMainFrame
            cls.__instance.__myCardMainScene = MyCardMainScene()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def createMyCardMainUiFrame(self, rootWindow, switchFrameWithMenuName):
        myCardMainFrame = self.__myCardMainFrame(rootWindow)

        ButtonHandlerImpl()
        button_handler = ButtonHandlerImpl.getInstance()

        buttonFunction1 = button_handler.getButtonTypeTable(ButtonType.DECKREGISTER.value)
        buttonFunction1(master=rootWindow, frame=myCardMainFrame)
        #
        # buttonFunction2 = button_handler.getButtonTypeTable(ButtonType.MOVETOFRAME.value)
        # buttonFunction2(rootWindow, myCardMainFrame)

        # buttonFunction3 = button_handler.getButtonTypeTable(ButtonType.CREATEDECK.value)
        # buttonFunction3(rootWindow, myCardMainFrame)

        return myCardMainFrame