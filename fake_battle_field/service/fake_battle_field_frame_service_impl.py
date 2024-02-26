from battle_field_muligun.frame.battle_field_muligun_frame import BattleFieldMuligunFrame
from battle_field_muligun.infra.muligun_your_hand_repository import MuligunYourHandRepository

from battle_field_muligun.service.request.muligun_request import MuligunRequest
from fake_battle_field.frame.fake_battle_field_frame import FakeBattleFieldFrame
from fake_battle_field.infra.fake_battle_field_frame_repository_impl import FakeBattleFieldFrameRepositoryImpl
from fake_battle_field.service.fake_battle_field_frame_service import FakeBattleFieldFrameService
from fake_battle_field.service.request.create_fake_battle_room_request import CreateFakeBattleRoomRequest
from session.repository.session_repository_impl import SessionRepositoryImpl


class FakeBattleFieldFrameServiceImpl(FakeBattleFieldFrameService):
    __instance = None

    # __fakeBattleFieldFrame = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__fakeBattleFieldFrameRepository = FakeBattleFieldFrameRepositoryImpl.getInstance()
            cls.__instance.__muligunYourHandRepository = MuligunYourHandRepository()
            cls.__instance.__fakeBattleFieldFrame = FakeBattleFieldFrame
            cls.__instance.__sessionRepository = SessionRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def createFakeBattleFieldFrame(self, rootWindow, switchFrameWithMenuName):

        fakeBattleFieldFrame = self.__fakeBattleFieldFrame(master=rootWindow, switchFrameWithMenuName=switchFrameWithMenuName)

        # try:
        #     responseData = self.__fakeBattleFieldFrameRepository.requestCreateFakeBattleRoom(
        #         CreateFakeBattleRoomRequest())
        #
        #     print(f"responseData: {responseData}")
        #
        #     if responseData is not None:
        #         server_data = responseData.get("redrawn_hand_card_list")
        #         print(f"서버에서 데이터 잘 들어옴{server_data}")
        #
        #         # self.__fakeBattleFieldFrameRepository.save_current_hand_state(server_data)
        #         # battleFieldMuligunFrame.on_canvas_ok_button_click()
        #
        #     else:
        #         print("Invalid or missing response data.")
        #
        # except Exception as e:
        #     print(f"An error occurred: {e}")

        return fakeBattleFieldFrame

    def injectTransmitIpcChannel(self, transmitIpcChannel):
        print("MyDeckRegisterFrameService: injectTransmitIpcChannel()")
        self.__fakeBattleFieldFrameRepository.injectTransmitIpcChannel(transmitIpcChannel)

    def injectReceiveIpcChannel(self, receiveIpcChannel):
        print("MyDeckRegisterFrameService: injectTransmitIpcChannel()")
        self.__fakeBattleFieldFrameRepository.injectReceiveIpcChannel(receiveIpcChannel)
