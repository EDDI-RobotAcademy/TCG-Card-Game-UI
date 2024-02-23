from account_register_frame.service.account_register_frame_service_impl import AccountRegisterFrameServiceImpl
from app_window.service.window_service_impl import WindowServiceImpl
from account_login_frame.service.login_menu_frame_service_impl import LoginMenuFrameServiceImpl
from battle_field.infra.battle_field_repository import BattleFieldRepository
from battle_field.infra.your_deck_repository import YourDeckRepository
from battle_field.infra.your_field_unit_repository import YourFieldUnitRepository
from battle_field_muligun.infra.your_hand_repository import YourHandRepository
from battle_field.infra.your_tomb_repository import YourTombRepository
from battle_field_function.service.battle_field_function_service_impl import BattleFieldFunctionServiceImpl
from battle_field_muligun.service.battle_field_muligun_service_impl import BattleFieldMuligunFrameServiceImpl
from battle_lobby_frame.service.battle_lobby_frame_service_impl import BattleLobbyFrameServiceImpl
from card_shop_frame.service.card_shop_service_impl import CardShopMenuFrameServiceImpl
from card_shop_frame.frame.buy_check_frame.service.buy_check_service_impl import BuyCheckServiceImpl
from lobby_frame.service.lobby_menu_frame_service_impl import LobbyMenuFrameServiceImpl
from main_frame.service.main_menu_frame_service_impl import MainMenuFrameServiceImpl
from matching_window.service.matching_window_service_impl import MatchingWindowServiceImpl
from opengl_battle_field.frame.battle_field_frame import BattleFieldFrame
from opengl_my_card_main_frame.service.my_card_main_frame_service_impl import MyCardMainFrameServiceImpl
from opengl_buy_random_card_frame.service.buy_random_card_frame_service_impl import BuyRandomCardFrameServiceImpl
from opengl_my_deck_register_frame.service.my_deck_register_frame_service_impl import MyDeckRegisterFrameServiceImpl


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
            cls.__instance.__buyCheckService = BuyCheckServiceImpl.getInstance()
            cls.__instance.__myCardMainFrameService = MyCardMainFrameServiceImpl.getInstance()
            cls.__instance.__buyRandomCardFrameService = BuyRandomCardFrameServiceImpl.getInstance()
            cls.__instance.__battleFieldFunctionService = BattleFieldFunctionServiceImpl.getInstance()
            cls.__instance.__myDeckRegisterFrameService = MyDeckRegisterFrameServiceImpl.getInstance()
            cls.__instance.__battleFieldFrame = BattleFieldFrame
            cls.__instance.__sessionService = SessionServiceImpl.getInstance()
            cls.__instance.__matchingWindowService = MatchingWindowServiceImpl.getInstance()
            cls.__instance.__battleFieldRepository = BattleFieldRepository.getInstance()
            cls.__instance.__yourDeckRepository = YourDeckRepository.getInstance()
            cls.__instance.__yourFieldUnitRepository = YourFieldUnitRepository.getInstance()
            cls.__instance.__yourHandRepository = YourHandRepository.getInstance()
            cls.__instance.__yourTombRepository = YourTombRepository.getInstance()
            cls.__instance.__battleFieldMuligunFrameServiece = BattleFieldMuligunFrameServiceImpl.getInstance()

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

        # myDeckRegisterFrame = self.__myDeckRegisterFrameService.createMyDeckRegisterUiFrame(rootWindow, self.switchFrameWithMenuName)
        # self.__uiFrameService.registerMyDeckRegisterUiFrame(myDeckRegisterFrame)

        battleFieldFrame = self.__battleFieldFrame()
        self.__uiFrameService.registerBattleFieldUiFrame(battleFieldFrame)

        battleFieldMuligunFrame = self.__battleFieldMuligunFrameServiece.createBattleFieldMuligunFrame(rootWindow, self.switchFrameWithMenuName)
        self.__uiFrameService.registerBattleFieldMuligunUiFrame(battleFieldMuligunFrame)

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
        self.__matchingWindowService.injectTransmitIpcChannel(transmitIpcChannel)

        self.__buyCheckService.injectTransmitIpcChannel(transmitIpcChannel)
        self.__battleFieldMuligunFrameServiece.injectReceiveIpcChannel(transmitIpcChannel)

        self.__battleFieldRepository.saveTransmitIpcChannel(transmitIpcChannel)
        self.__yourDeckRepository.saveTransmitIpcChannel(transmitIpcChannel)
        self.__yourFieldUnitRepository.saveTransmitIpcChannel(transmitIpcChannel)
        self.__yourHandRepository.saveTransmitIpcChannel(transmitIpcChannel)
        self.__yourTombRepository.saveTransmitIpcChannel(transmitIpcChannel)


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
        self.__matchingWindowService.injectReceiveIpcChannel(receiveIpcChannel)

        self.__buyCheckService.injectReceiveIpcChannel(receiveIpcChannel)
        self.__battleFieldMuligunFrameServiece.injectReceiveIpcChannel(receiveIpcChannel)

        self.__battleFieldRepository.saveReceiveIpcChannel(receiveIpcChannel)
        self.__yourDeckRepository.saveReceiveIpcChannel(receiveIpcChannel)
        self.__yourFieldUnitRepository.saveReceiveIpcChannel(receiveIpcChannel)
        self.__yourHandRepository.saveReceiveIpcChannel(receiveIpcChannel)
        self.__yourTombRepository.saveReceiveIpcChannel(receiveIpcChannel)


    def requestToInjectMusicPlayIpcChannel(self, musicPlayIpcChannel):
        print("UiFrameControllerImpl: requestToInjectMusicPlayIpcChannel()")

        self.__uiFrameService.injectMusicPlayIpcChannel(musicPlayIpcChannel)

    def requestToInjectNoWaitIpcChannel(self, uiNoWaitIpcChannel):
        print("UiFrameControllerImpl: requestToInjectMusicPlayIpcChannel()")

        self.__battleFieldRepository.injectNoWaitIpcChannel(uiNoWaitIpcChannel)
