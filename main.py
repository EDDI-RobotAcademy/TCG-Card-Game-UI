from initializer.init_domain import DomainInitializer
from ui_frame.service.ui_frame_service_impl import UiFrameServiceImpl
from window.service.window_service_impl import WindowServiceImpl

DomainInitializer.initEachDomain()


if __name__ == "__main__":
    windowService = WindowServiceImpl.getInstance()
    rootWindow = windowService.createStartWindow()
    rootWindow.mainloop()

