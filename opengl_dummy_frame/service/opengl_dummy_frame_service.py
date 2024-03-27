from opengl_dummy_frame.dummy_frame import DummyFrame
from opengl_dummy_frame.repository.opengl_dummy_frame_repository import OpenGLDummyFrameRepository


class OpenGLDummyFrameService:
    __instance = None

    __switchFrameWithMenuName = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__openGLDummyFrameRepository = OpenGLDummyFrameRepository.getInstance()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()

            cls.__instance.__openGLDummyFrame = DummyFrame
        return cls.__instance

    def get_switch_frame_with_menu_name(self):
        return self.__switchFrameWithMenuName

    def createOpenGLDummyFrame(self, rootWindow, switchFrameWithMenuName):
        # openGLDummyFrame = self.__openGLDummyFrameRepository.createOpenGLDummyFrame(rootWindow, switchFrameWithMenuName)
        openGLDummyFrame = self.__openGLDummyFrame(rootWindow, switchFrameWithMenuName)

        return openGLDummyFrame