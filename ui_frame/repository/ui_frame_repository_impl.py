from pyopengltk import OpenGLFrame

from opengl_my_card_main_frame.frame.my_card_main_frame import MyCardMainFrame
from ui_frame.repository.ui_frame_repository import UiFrameRepository


class UiFrameRepositoryImpl(UiFrameRepository):
    __instance = None
    __currentFrame = None
    __transmitIpcChannel = None
    __receiveIpcChannel = None
    __musicPlayIpcChannel = None
    __windowFrameList = {}
    __animation_running = False
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def setCurrentFrame(self, currentFrame):
        self.__currentFrame = currentFrame

    def getWindowFrameList(self):
        print("UiFrameRepositoryImpl: getWindowFrameList()")
        return self.__windowFrameList

    def registerUiFrame(self, name, newFrame):
        print("UiFrameRepositoryImpl: registerUiFrame()")
        self.__windowFrameList[name] = newFrame
        # self.__currentFrame = newFrame

    def switchFrameWithMenuName(self, name: str):
        print("UiFrameRepositoryImpl: switchFrameWithMenuName()")

        foundUiFrame = self.__windowFrameList[name]

        if foundUiFrame is None:
            print("UiFrame 등록 및 전환에 문제가 발생했습니다")

        if self.__currentFrame is not None:
            print("기존 Frame 해제")
            self.__currentFrame.pack_forget()
            self.__animation_running = False

        foundUiFrame.pack(expand=True, fill="both")
        self.__currentFrame = foundUiFrame

        self.__musicPlayIpcChannel.put(name)

        if isinstance(foundUiFrame, OpenGLFrame):
            if isinstance(foundUiFrame, MyCardMainFrame):
                return

            # foundUiFrame.start_redraw_loop()
            self.__animation_running = True
            def animate():
                if self.__animation_running:
                # print(f"OpenGL redrawing")
                    foundUiFrame.redraw()
                    foundUiFrame.after(17, animate)

            foundUiFrame.after(0, animate)

    def saveTransmitIpcChannel(self, transmitIpcChannel):
        print("UiFrameRepositoryImpl: saveTransmitIpcChannel()")
        self.__transmitIpcChannel = transmitIpcChannel

    def saveReceiveIpcChannel(self, receiveIpcChannel):
        print("UiFrameRepositoryImpl: saveReceiveIpcMessage()")
        self.__receiveIpcChannel = receiveIpcChannel

    def saveMusicPlayIpcChannel(self, musicPlayIpcChannel):
        print("UiFrameRepositoryImpl: saveMusicPlayIpcMessage()")
        self.__musicPlayIpcChannel = musicPlayIpcChannel
