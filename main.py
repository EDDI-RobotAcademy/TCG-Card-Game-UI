import tkinter

from app_window.service.window_service_impl import WindowServiceImpl
from initializer.init_domain import DomainInitializer
from ui_frame.controller.ui_frame_controller_impl import UiFrameControllerImpl
from ui_frame.repository.main_menu_frame.main_menu_frame_repository_impl import MainMenuFrameRepositoryImpl
from ui_frame.service.ui_frame_service_impl import UiFrameServiceImpl

DomainInitializer.initEachDomain()


if __name__ == "__main__":
    windowService = WindowServiceImpl.getInstance()
    rootWindow = windowService.createStartWindow()

    uiFrameController = UiFrameControllerImpl.getInstance()
    uiFrameController.requestToCreateUiFrame(rootWindow)

    rootWindow.mainloop()

