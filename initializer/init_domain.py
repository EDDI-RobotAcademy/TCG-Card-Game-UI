import multiprocessing

from account_register_frame.service.account_register_frame_service_impl import AccountRegisterFrameServiceImpl
from app_window.service.window_service_impl import WindowServiceImpl
from card_info_from_csv.controller.card_info_from_csv_controller_impl import CardInfoFromCsvControllerImpl
from client_socket.service.client_socket_service_impl import ClientSocketServiceImpl
from account_login_frame.service.login_menu_frame_service_impl import LoginMenuFrameServiceImpl
from main_frame.service.main_menu_frame_service_impl import MainMenuFrameServiceImpl
from music_player.controller.music_player_controller_impl import MusicPlayerControllerImpl
from notify_reader.controller.notify_reader_controller_impl import NotifyReaderControllerImpl
from opengl_battle_field_card_controller.legacy.card_controller_impl import LegacyCardControllerImpl
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage
from receiver.controller.receiver_controller_impl import ReceiverControllerImpl
from response_generator.repository.response_generator_repository_impl import ResponseGeneratorRepositoryImpl
from task_worker.service.task_worker_service_impl import TaskWorkerServiceImpl
from transmitter.controller.transmitter_controller_impl import TransmitterControllerImpl
from ui_frame.controller.ui_frame_controller_impl import UiFrameControllerImpl


class DomainInitializer:
    # UI Frame
    @staticmethod
    def initRootWindowDomain():
        WindowServiceImpl.getInstance()

    @staticmethod
    def initMainMenuFrameDomain():
        MainMenuFrameServiceImpl.getInstance()

    @staticmethod
    def initLoginMenuFrameDomain():
        LoginMenuFrameServiceImpl.getInstance()

    @staticmethod
    def initUiFrameDomain(uiTransmitIpcChannel, uiReceiveIpcChannel, uiMusicPlayIpcChannel, uiNoWaitIpcChannel):
        uiFrameController = UiFrameControllerImpl.getInstance()
        uiFrameController.requestToInjectTransmitIpcChannel(uiTransmitIpcChannel)
        uiFrameController.requestToInjectReceiveIpcChannel(uiReceiveIpcChannel)
        uiFrameController.requestToInjectMusicPlayIpcChannel(uiMusicPlayIpcChannel)
        uiFrameController.requestToInjectNoWaitIpcChannel(uiNoWaitIpcChannel)

    @staticmethod
    def initNotifyReaderDomain(noWaitIpcChannel):
        notifyReaderController = NotifyReaderControllerImpl.getInstance()
        notifyReaderController.requestToMappingNoticeWithFunction()
        notifyReaderController.requestToInjectNoWaitIpcChannel(noWaitIpcChannel)

    @staticmethod
    def initAccountRegisterFrameDomain():
        AccountRegisterFrameServiceImpl.getInstance()

    # Socket Domain
    @staticmethod
    def initClientSocketDomain():
        ClientSocketServiceImpl.getInstance()

    @staticmethod
    def initTransmitterDomain(uiTransmitIpcChannel):
        transmitterController = TransmitterControllerImpl.getInstance()
        transmitterController.requestToInjectUiIpcChannel(uiTransmitIpcChannel)

    @staticmethod
    def initReceiverDomain(uiReceiveIpcChannel, uiNoWaitIpcChannel):
        receiverController = ReceiverControllerImpl.getInstance()
        receiverController.requestToInjectUiIpcChannel(uiReceiveIpcChannel)
        receiverController.requestToInjectUiNoWaitIpcChannel(uiNoWaitIpcChannel)

    @staticmethod
    def initMusicPlayerDomain(uiMusicPlayIpcChannel):
        musicPlayerController = MusicPlayerControllerImpl.getInstance()
        musicPlayerController.requestToInjectUiIpcChannel(uiMusicPlayIpcChannel)

    # Task Worker Domain
    @staticmethod
    def initTaskWorkerDomain():
        TaskWorkerServiceImpl.getInstance()

    # Response Generator Domain
    @staticmethod
    def initResponseGeneratorDomain():
        ResponseGeneratorRepositoryImpl.getInstance()

    @staticmethod
    def initReadCsvFileDomain():
        cardInfoFromCsvController = CardInfoFromCsvControllerImpl.getInstance()
        cardInfoFromCsvController.requestToCardInfoSettingInMemory()

    @staticmethod
    def initPreDrawedImageDomain():
        pre_drawed_image_manager = PreDrawedImage.getInstance()
        pre_drawed_image_manager.pre_draw_every_image()

    @staticmethod
    def initBattleFieldCardControllerDomain():
        LegacyCardControllerImpl.getInstance()

    @staticmethod
    def initEachDomain():
        # IPC Channel
        uiTransmitIpcChannel = multiprocessing.Queue()
        uiReceiveIpcChannel = multiprocessing.Queue()
        uiMusicPlayIpcChannel = multiprocessing.Queue()
        uiNoWaitIpcChannel = multiprocessing.Queue()

        # UI Frame Domain
        DomainInitializer.initRootWindowDomain()
        DomainInitializer.initMainMenuFrameDomain()
        DomainInitializer.initLoginMenuFrameDomain()
        DomainInitializer.initAccountRegisterFrameDomain()
        DomainInitializer.initUiFrameDomain(uiTransmitIpcChannel, uiReceiveIpcChannel, uiMusicPlayIpcChannel, uiNoWaitIpcChannel)

        # Socket Domain
        DomainInitializer.initClientSocketDomain()
        DomainInitializer.initTransmitterDomain(uiTransmitIpcChannel)
        DomainInitializer.initReceiverDomain(uiReceiveIpcChannel, uiNoWaitIpcChannel)
        DomainInitializer.initMusicPlayerDomain(uiMusicPlayIpcChannel)
        DomainInitializer.initNotifyReaderDomain(uiNoWaitIpcChannel)


        # Task Worker Domain
        DomainInitializer.initTaskWorkerDomain()

        # Response Generator Domain
        DomainInitializer.initResponseGeneratorDomain()

        # Read Csv File Domain
        DomainInitializer.initReadCsvFileDomain()

        # Pre Drawed Image Domain
        DomainInitializer.initPreDrawedImageDomain()

        # Battle Field Card Controller Domain
        DomainInitializer.initBattleFieldCardControllerDomain()










