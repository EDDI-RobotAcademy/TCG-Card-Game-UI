from colorama import Style, Fore

from ui_frame.repository.ui_frame_repository_impl import UiFrameRepositoryImpl
from ui_frame.service.ui_frame_service import UiFrameService


class UiFrameServiceImpl(UiFrameService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__uiFrameRepository = UiFrameRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def switchFrameWithMenuName(self, menuName: str):
        print(f"{Fore.GREEN}UiFrameServiceImpl: switchFrameWithMenuName() -> {menuName}{Style.RESET_ALL}")
        self.__uiFrameRepository.switchFrameWithMenuName(menuName)

    def registerMainMenuUiFrame(self, mainMenuFrame):
        print(f"{Fore.GREEN}UiFrameServiceImpl: registerMainMenuUiFrame(){Style.RESET_ALL}")
        self.__uiFrameRepository.registerUiFrame("main-menu", mainMenuFrame)

    def registerLoginMenuUiFrame(self, loginMenuFrame):
        print(f"{Fore.GREEN}UiFrameServiceImpl: registerLoginMenuUiFrame(){Style.RESET_ALL}")
        self.__uiFrameRepository.registerUiFrame("login-menu", loginMenuFrame)

    def registerAccountRegisterUiFrame(self, accountRegisterFrame):
        print(f"{Fore.GREEN}UiFrameServiceImpl: registerAccountRegisterUiFrame(){Style.RESET_ALL}")
        self.__uiFrameRepository.registerUiFrame("account-register", accountRegisterFrame)

    def registerLobbyMenuUiFrame(self, lobbyMenuFrame):
        print(f"{Fore.GREEN}UiFrameServiceImpl: registerLobbyMenuUiFrame(){Style.RESET_ALL}")
        self.__uiFrameRepository.registerUiFrame("lobby-menu", lobbyMenuFrame)

    def registerBattleLobbyMenuUiFrame(self, battleLobbyFrame):
        print(f"{Fore.GREEN}UiFrameServiceImpl: registerBattleLobbyMenuUiFrame(){Style.RESET_ALL}")
        self.__uiFrameRepository.registerUiFrame("battle-lobby", battleLobbyFrame)

    def registerMyCardMainUiFrame(self, myCardMainFrame):
        print(f"{Fore.GREEN}UiFrameServiceImpl: registerMyCardUiFrame(){Style.RESET_ALL}")
        self.__uiFrameRepository.registerUiFrame("my-card-main", myCardMainFrame)

    def registerMyDeckUiFrame(self, myDeckFrame):
        print(f"{Fore.GREEN}UiFrameServiceImpl: registerMyDeckUiFrame(){Style.RESET_ALL}")
        self.__uiFrameRepository.registerUiFrame("my-deck", myDeckFrame)

    def registerCardUiFrame(self, cardFrame):
        print(f"{Fore.GREEN}UiFrameServiceImpl: registerCardUiFrame(){Style.RESET_ALL}")
        self.__uiFrameRepository.registerUiFrame("card", cardFrame)

    def registerCardShopMenuUiFrame(self, cardShopMenuFrame):
        print(f"{Fore.GREEN}UiFrameServiceImpl: registerCardShopMenuUiFrame(){Style.RESET_ALL}")
        self.__uiFrameRepository.registerUiFrame("card-shop-menu", cardShopMenuFrame)

    def injectTransmitIpcChannel(self, transmitIpcChannel):
        print(f"{Fore.GREEN}UiFrameServiceImpl: injectTransmitIpcChannel(){Style.RESET_ALL}")
        self.__uiFrameRepository.saveTransmitIpcChannel(transmitIpcChannel)

    def injectReceiveIpcChannel(self, receiveIpcChannel):
        print(f"{Fore.GREEN}UiFrameServiceImpl: injectReceiveIpcChannel(){Style.RESET_ALL}")
        self.__uiFrameRepository.saveReceiveIpcChannel(receiveIpcChannel)

    def injectMusicPlayIpcChannel(self, musicPlayIpcChannel):
        print(f"{Fore.GREEN}UiFrameServiceImpl: injectMusicPlayIpcChannel(){Style.RESET_ALL}")
        self.__uiFrameRepository.saveMusicPlayIpcChannel(musicPlayIpcChannel)
