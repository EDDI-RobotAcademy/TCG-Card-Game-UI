from opengl_button.button_binding.button_bind import MyCardMainFrameButtonBind
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

        buttonBinding = MyCardMainFrameButtonBind(master=rootWindow, frame=myCardMainFrame)
        buttonBinding.button_bind()

        return myCardMainFrame