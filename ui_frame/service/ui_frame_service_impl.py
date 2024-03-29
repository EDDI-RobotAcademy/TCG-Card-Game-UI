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

    def registerOpenGLDummyFrame(self, openGLDummyFrame):
        print(f"{Fore.GREEN}UiFrameServiceImpl: registerOpenGLDummyFrame(){Style.RESET_ALL}")
        self.__uiFrameRepository.registerUiFrame("dummy", openGLDummyFrame)

    def registerFakeBattleFieldUiFrame(self, fakeBattleFieldFrame):
        print(f"{Fore.GREEN}UiFrameServiceImpl: registerFakeBattleFieldUiFrame(){Style.RESET_ALL}")
        self.__uiFrameRepository.registerUiFrame("fake-battle-field", fakeBattleFieldFrame)


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
        print(f"{Fore.GREEN}UiFrameServiceImpl: registerMyCardMainUiFrame(){Style.RESET_ALL}")
        self.__uiFrameRepository.registerUiFrame("my-card-main", myCardMainFrame)

    def registerMyDeckUiFrame(self, myDeckFrame):
        print(f"{Fore.GREEN}UiFrameServiceImpl: registerMyDeckUiFrame(){Style.RESET_ALL}")
        self.__uiFrameRepository.registerUiFrame("my-deck", myDeckFrame)

    def registerCardShopMenuUiFrame(self, cardShopMenuFrame):
        print(f"{Fore.GREEN}UiFrameServiceImpl: registerCardShopMenuUiFrame(){Style.RESET_ALL}")
        self.__uiFrameRepository.registerUiFrame("card-shop-menu", cardShopMenuFrame)

    def registerBuyRandomCardUiFrame(self, buyRandomCardFrame):
        print(f"{Fore.GREEN}UiFrameServiceImpl: registerBuyRandomCardUiFrame(){Style.RESET_ALL}")
        self.__uiFrameRepository.registerUiFrame("buy-random-card", buyRandomCardFrame)

    def registerRockPaperScissorsUiFrame(self, rockPaperScissorsFrame):
        print(f"{Fore.GREEN}UiFrameServiceImpl: registerRockPaperScissorsUiFrame(){Style.RESET_ALL}")
        self.__uiFrameRepository.registerUiFrame("rock-paper-scissors", rockPaperScissorsFrame)

    def registerCheckRockPaperScissorsUiFrame(self, checkRockPaperScissorsFrame):
        print(f"{Fore.GREEN}UiFrameServiceImpl: registerCheckRockPaperScissorsUiFrame(){Style.RESET_ALL}")
        self.__uiFrameRepository.registerUiFrame("check-rock-paper-scissors", checkRockPaperScissorsFrame)

    # def registerMyDeckRegisterUiFrame(self, myDeckRegisterFrame):
    #     print(f"{Fore.GREEN}UiFrameServiceImpl: registerMyDeckRegisterUiFrame(){Style.RESET_ALL}")
    #     self.__uiFrameRepository.registerUiFrame("my-deck-register", myDeckRegisterFrame)

    def registerBattleFieldMuligunUiFrame(self, battleFieldMuligunFrame):
        print(f"{Fore.GREEN}UiFrameServiceImpl: registerBuyRandomCardUiFrame(){Style.RESET_ALL}")
        self.__uiFrameRepository.registerUiFrame("battle-field-muligun", battleFieldMuligunFrame)

    def legacyRegisterBattleFieldUiFrame(self, legacyBattleFieldFrame):
        print(f"{Fore.GREEN}UiFrameServiceImpl: legacyRegisterBattleFieldUiFrame(){Style.RESET_ALL}")
        self.__uiFrameRepository.registerUiFrame("legacy-battle-field", legacyBattleFieldFrame)

    def registerDecisionFirstStrikeFrame(self, decisionFirstStrikeFrame):
        self.__uiFrameRepository.registerUiFrame("decision-first", decisionFirstStrikeFrame)

    def injectTransmitIpcChannel(self, transmitIpcChannel):
        print(f"{Fore.GREEN}UiFrameServiceImpl: injectTransmitIpcChannel(){Style.RESET_ALL}")
        self.__uiFrameRepository.saveTransmitIpcChannel(transmitIpcChannel)

    def injectReceiveIpcChannel(self, receiveIpcChannel):
        print(f"{Fore.GREEN}UiFrameServiceImpl: injectReceiveIpcChannel(){Style.RESET_ALL}")
        self.__uiFrameRepository.saveReceiveIpcChannel(receiveIpcChannel)

    def injectMusicPlayIpcChannel(self, musicPlayIpcChannel):
        print(f"{Fore.GREEN}UiFrameServiceImpl: injectMusicPlayIpcChannel(){Style.RESET_ALL}")
        self.__uiFrameRepository.saveMusicPlayIpcChannel(musicPlayIpcChannel)

    def register_battle_result_frame(self, battleResultFrame):
        print(f"{Fore.GREEN}UiFrameServiceImpl: register_battle_result_frame(){Style.RESET_ALL}")
        self.__uiFrameRepository.registerUiFrame("battle-result", battleResultFrame)

    def registerBattleFieldUiFrame(self, battleFieldFrame):
        print(f"{Fore.GREEN}UiFrameServiceImpl: registerBattleFieldUiFrame(){Style.RESET_ALL}")
        self.__uiFrameRepository.registerUiFrame("battle-field", battleFieldFrame)