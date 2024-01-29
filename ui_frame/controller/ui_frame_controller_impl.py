from account_register_frame.service.account_register_frame_service_impl import AccountRegisterFrameServiceImpl
from app_window.service.window_service_impl import WindowServiceImpl
from account_login_frame.service.login_menu_frame_service_impl import LoginMenuFrameServiceImpl
from battle_field_function.service.battle_field_function_service_impl import BattleFieldFunctionServiceImpl
from battle_lobby_frame.service.battle_lobby_frame_service_impl import BattleLobbyFrameServiceImpl
from card_shop_frame.service.card_shop_service_impl import CardShopMenuFrameServiceImpl
from lobby_frame.service.lobby_menu_frame_service_impl import LobbyMenuFrameServiceImpl
from main_frame.service.main_menu_frame_service_impl import MainMenuFrameServiceImpl
from tests.my_card_main_frame_legacy.service.my_card_main_frame_service_impl import MyCardMainFrameServiceImpl

from buy_random_card_frame.service.buy_random_card_frame_service_impl import BuyRandomCardFrameServiceImpl

# from card_random_frame.service.card_random_frame_service_impl import CardRandomFrameServiceImpl
from my_deck_register_frame.service.my_deck_register_frame_service_impl import MyDeckRegisterFrameServiceImpl


from session.service.session_service_impl import SessionServiceImpl

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
            cls.__instance.__loginMenuFrameService = LoginMenuFrameServiceImpl.getInstance()
            cls.__instance.__accountRegisterFrameService = AccountRegisterFrameServiceImpl.getInstance()
            cls.__instance.__lobbyMenuFrameService = LobbyMenuFrameServiceImpl.getInstance()
            cls.__instance.__battleLobbyFrameService = BattleLobbyFrameServiceImpl.getInstance()
            cls.__instance.__cardShopMenuFrameService = CardShopMenuFrameServiceImpl.getInstance()
            cls.__instance.__myCardMainFrameService = MyCardMainFrameServiceImpl.getInstance()

            cls.__instance.__buyRandomCardFrameService = BuyRandomCardFrameServiceImpl.getInstance()

            # cls.__instance.__cardRandomFrameService = CardRandomFrameServiceImpl.getInstance()

            cls.__instance.__battleFieldFunctionService = BattleFieldFunctionServiceImpl.getInstance()

            cls.__instance.__myDeckRegisterFrameService = MyDeckRegisterFrameServiceImpl.getInstance()


            cls.__instance.__sessionService = SessionServiceImpl.getInstance()
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

        mainMenuFrame = self.__mainMenuFrameService.createMainUiFrame(rootWindow, self.switchFrameWithMenuName)
        self.__uiFrameService.registerMainMenuUiFrame(mainMenuFrame)

        loginMenuFrame = self.__loginMenuFrameService.createLoginUiFrame(rootWindow, self.switchFrameWithMenuName)
        self.__uiFrameService.registerLoginMenuUiFrame(loginMenuFrame)

        accountRegisterFrame = self.__accountRegisterFrameService.createAccountRegisterUiFrame(rootWindow, self.switchFrameWithMenuName)
        self.__uiFrameService.registerAccountRegisterUiFrame(accountRegisterFrame)

        battleLobbyMenuFrame = self.__battleLobbyFrameService.createBattleLobbyUiFrame(rootWindow, self.switchFrameWithMenuName)
        self.__uiFrameService.registerBattleLobbyMenuUiFrame(battleLobbyMenuFrame)

        lobbyMenuFrame = self.__lobbyMenuFrameService.createLobbyUiFrame(rootWindow, self.switchFrameWithMenuName)
        self.__uiFrameService.registerLobbyMenuUiFrame(lobbyMenuFrame)

        myCardMainFrame = self.__myCardMainFrameService.createMyCardMainUiFrame(rootWindow, self.switchFrameWithMenuName)
        self.__uiFrameService.registerMyCardMainUiFrame(myCardMainFrame)

        cardShopMenuFrame = (
            self.__cardShopMenuFrameService.createCardShopUiFrame(rootWindow, self.switchFrameWithMenuName))
        self.__uiFrameService.registerCardShopMenuUiFrame(cardShopMenuFrame)

        buyRandomCardFrame = self.__buyRandomCardFrameService.createBuyRandomCardUiFrame(rootWindow, self.switchFrameWithMenuName)
        self.__uiFrameService.registerBuyRandomCardUiFrame(buyRandomCardFrame)

        myDeckRegisterFrame = self.__myDeckRegisterFrameService.createMyDeckRegisterUiFrame(rootWindow, self.switchFrameWithMenuName)
        self.__uiFrameService.registerMyDeckRegisterUiFrame(myDeckRegisterFrame)

        self.switchFrameWithMenuName("main-menu")

    def switchFrameWithMenuName(self, name):
        print("UiFrameControllerImpl: switchFrameWithMenuName()")
        self.__uiFrameService.switchFrameWithMenuName(name)

    def requestToStartPrintGameUi(self):
        print("UiFrameControllerImpl: requestToStartPrintGameUi()")
        rootWindow = self.__windowService.getRootWindow()
        rootWindow.mainloop()

    def requestToInjectTransmitIpcChannel(self, transmitIpcChannel):
        print("UiFrameControllerImpl: requestToInjectTransmitIpcChannel()")

        self.__uiFrameService.injectTransmitIpcChannel(transmitIpcChannel)
        self.__accountRegisterFrameService.injectTransmitIpcChannel(transmitIpcChannel)
        self.__loginMenuFrameService.injectTransmitIpcChannel(transmitIpcChannel)
        self.__mainMenuFrameService.injectTransmitIpcChannel(transmitIpcChannel)
        self.__battleLobbyFrameService.injectTransmitIpcChannel(transmitIpcChannel)
        self.__lobbyMenuFrameService.injectTransmitIpcChannel(transmitIpcChannel)
        self.__sessionService.injectTransmitIpcChannel(transmitIpcChannel)

        self.__battleFieldFunctionService.injectTransmitIpcChannel(transmitIpcChannel)

        self.__myDeckRegisterFrameService.injectTransmitIpcChannel(transmitIpcChannel)


    def requestToInjectReceiveIpcChannel(self, receiveIpcChannel):
        print("UiFrameControllerImpl: requestToInjectReceiveIpcChannel()")

        self.__uiFrameService.injectReceiveIpcChannel(receiveIpcChannel)
        self.__accountRegisterFrameService.injectReceiveIpcChannel(receiveIpcChannel)
        self.__loginMenuFrameService.injectReceiveIpcChannel(receiveIpcChannel)
        self.__mainMenuFrameService.injectReceiveIpcChannel(receiveIpcChannel)
        self.__battleLobbyFrameService.injectReceiveIpcChannel(receiveIpcChannel)
        self.__lobbyMenuFrameService.injectReceiveIpcChannel(receiveIpcChannel)
        self.__sessionService.injectReceiveIpcChannel(receiveIpcChannel)

        self.__battleFieldFunctionService.injectReceiveIpcChannel(receiveIpcChannel)

        self.__myDeckRegisterFrameService.injectReceiveIpcChannel(receiveIpcChannel)


    def requestToInjectMusicPlayIpcChannel(self, musicPlayIpcChannel):
        print("UiFrameControllerImpl: requestToInjectMusicPlayIpcChannel()")

        self.__uiFrameService.injectMusicPlayIpcChannel(musicPlayIpcChannel)
