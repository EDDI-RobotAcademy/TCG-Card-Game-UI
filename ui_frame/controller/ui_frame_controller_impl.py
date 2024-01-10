from app_window.service.window_service_impl import WindowServiceImpl
from main_frame.service.main_menu_frame_service_impl import MainMenuFrameServiceImpl
from ui_frame.controller.ui_frame_controller import UiFrameController
from ui_frame.service.ui_frame_service_impl import UiFrameServiceImpl


class UiFrameControllerImpl(UiFrameController):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__uiFrameService = UiFrameServiceImpl.getInstance()
            cls.__instance.__windowService = WindowServiceImpl.getInstance()
            cls.__instance.__mainMenuFrameService = MainMenuFrameServiceImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def requestToCreateUiFrame(self):
        print("UiFrameControllerImpl: requestToCreateUiFrame()")

        self.__windowService.createRootWindow()
        rootWindow = self.__windowService.getRootWindow()

        mainMenuFrame = self.__mainMenuFrameService.createMainUiFrame(rootWindow)
        self.__uiFrameService.registerMainMenuUiFrame(mainMenuFrame)
        
        self.__uiFrameService.createLoginUiFrame(rootWindow)

    def requestToStartPrintGameUi(self):
        rootWindow = self.__windowService.getRootWindow()
        rootWindow.mainloop()

