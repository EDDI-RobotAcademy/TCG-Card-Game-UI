from matching_window.controller.matching_window_controller import MatchingWindowController
from matching_window.service.matching_window_service_impl import MatchingWindowServiceImpl


class MatchingWindowControllerImpl(MatchingWindowController):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__matchingWindowService = MatchingWindowServiceImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def makeMatchingWindow(self, rootWindow):
        self.__matchingWindowService.createMatchingWindow(rootWindow)

    def matching(self, rootWindow):
        return self.__matchingWindowService.startMatching(rootWindow)