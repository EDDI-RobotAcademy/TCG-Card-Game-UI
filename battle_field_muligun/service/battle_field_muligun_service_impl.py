from battle_field_muligun.frame.battle_field_muligun_frame import BattleFieldMuligunFrame
from battle_field_muligun.infra.your_hand_repository import YourHandRepository
from battle_field_muligun.service.battle_field_muligun_service import BattleFieldMuligunFrameService
from battle_field_muligun.service.request.muligun_request import MuligunRequest
from session.repository.session_repository_impl import SessionRepositoryImpl


class BattleFieldMuligunFrameServiceImpl(BattleFieldMuligunFrameService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__battleFieldMuligunFrameRepository = YourHandRepository()
            cls.__instance.__battleFieldMuligunFrame = BattleFieldMuligunFrame
            cls.__instance.__sessionRepository = SessionRepositoryImpl.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def createBattleFieldMuligunFrame(self, rootWindow, switchFrameWithMenuName):

        battleFieldMuligunFrame = self.__battleFieldMuligunFrame(rootWindow)

        try:
            session_info = self.__sessionRepository.get_session_info()
            if session_info is not None:
                responseData = self.__battleFieldMuligunFrameRepository.requestMuligun(
                    MuligunRequest(self.__sessionRepository.get_session_info(),
                                   self.__battleFieldMuligunFrameRepository.get_change_card_id_list()))

                print(f"responseData: {responseData}")

                if responseData is not None:
                    server_data = responseData.get("redrawn_card_id_list")

                    self.__battleFieldMuligunFrameRepository.save_current_hand_state(server_data)
                    # battleFieldMuligunFrame.on_canvas_ok_button_click()

                else:
                    print("Invalid or missing response data.")

        except Exception as e:
            print(f"An error occurred: {e}")


        return battleFieldMuligunFrame

    def injectTransmitIpcChannel(self, transmitIpcChannel):
        print("MyDeckRegisterFrameService: injectTransmitIpcChannel()")
        self.__battleFieldMuligunFrameRepository.saveTransmitIpcChannel(transmitIpcChannel)

    def injectReceiveIpcChannel(self, receiveIpcChannel):
        print("MyDeckRegisterFrameService: injectTransmitIpcChannel()")
        self.__battleFieldMuligunFrameRepository.saveReceiveIpcChannel(receiveIpcChannel)