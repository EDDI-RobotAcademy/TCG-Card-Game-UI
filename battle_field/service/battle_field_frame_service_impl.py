from battle_field.frame.battle_field_frame import BattleFieldFrame
from battle_field.infra.battle_field_frame_repository_impl import BattleFieldFrameRepositoryImpl
from battle_field.service.battle_field_frame_service import BattleFieldFrameService
from battle_field_muligun.infra.muligun_your_hand_repository import MuligunYourHandRepository

from session.repository.session_repository_impl import SessionRepositoryImpl


class BattleFieldFrameServiceImpl(BattleFieldFrameService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__BattleFieldFrameRepository = BattleFieldFrameRepositoryImpl.getInstance()
            cls.__instance.__muligunYourHandRepository = MuligunYourHandRepository()
            cls.__instance.__BattleFieldFrame = BattleFieldFrame
            cls.__instance.__sessionRepository = SessionRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def createBattleFieldFrame(self, rootWindow, switchFrameWithMenuName):

        BattleFieldFrame = self.__BattleFieldFrame(master=rootWindow, switchFrameWithMenuName=switchFrameWithMenuName)

        return BattleFieldFrame

    def injectTransmitIpcChannel(self, transmitIpcChannel):
        print("MyDeckRegisterFrameService: injectTransmitIpcChannel()")
        self.__BattleFieldFrameRepository.injectTransmitIpcChannel(transmitIpcChannel)

    def injectReceiveIpcChannel(self, receiveIpcChannel):
        print("MyDeckRegisterFrameService: injectTransmitIpcChannel()")
        self.__BattleFieldFrameRepository.injectReceiveIpcChannel(receiveIpcChannel)
