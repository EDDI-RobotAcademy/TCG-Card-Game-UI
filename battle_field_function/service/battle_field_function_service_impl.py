from battle_field.infra.battle_field_repository import BattleFieldRepository
from battle_field.infra.opponent_field_unit_repository import OpponentFieldUnitRepository
from battle_field.infra.legacy.circle_image_legacy_your_hand_repository import CircleImageLegacyYourHandRepository
from battle_field_function.repository.battle_field_function_repository_impl import BattleFieldFunctionRepositoryImpl
from battle_field_function.service.battle_field_function_service import BattleFieldFunctionService
from battle_field_function.service.request.game_end_reward_request import GameEndRewardRequest
from battle_field_function.service.request.surrender_request import SurrenderRequest
from battle_field_function.service.request.turn_end_request import TurnEndRequest
from common.card_race import CardRace

from session.repository.session_repository_impl import SessionRepositoryImpl
from session.service.session_service_impl import SessionServiceImpl



class BattleFieldFunctionServiceImpl(BattleFieldFunctionService):
    __instance = None
    preDrawedBattleFieldFrame = None
    uiFrameController = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__battleFieldFunctionRepository = BattleFieldFunctionRepositoryImpl.getInstance()
            cls.__instance.__sessionRepository = SessionRepositoryImpl.getInstance()
            cls.__instance.__sessionService = SessionServiceImpl.getInstance()
            cls.__instance.__yourHandRepository = CircleImageLegacyYourHandRepository.getInstance()
            cls.__instance.__battle_field_repository = BattleFieldRepository.getInstance()
            #cls.__instance.__opponentHandRepository = OpponentHandRepository.getInstance()
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def injectTransmitIpcChannel(self, transmitIpcChannel):
        self.__battleFieldFunctionRepository.saveTransmitIpcChannel(transmitIpcChannel)

    def injectReceiveIpcChannel(self, receiveIpcChannel):
        self.__battleFieldFunctionRepository.saveReceiveIpcChannel(receiveIpcChannel)


    def saveFrame(self, ui_frame_controller,frame):
        self.preDrawedBattleFieldFrame = frame
        self.uiFrameController = ui_frame_controller

    def surrender(self, switchFrameWithMenuName = None):
        print(f"battleFieldFunctionServiceImpl: Surrender")
        surrender_response = self.__battleFieldFunctionRepository.requestSurrender(
            SurrenderRequest(
                self.__sessionService.getSessionInfo()
            )
        )
        # Todo : switchFrameWithMenuName('lobby-menu') 를 호출 할 수 있어야합니다.
        if switchFrameWithMenuName is not None:
            switchFrameWithMenuName("lobby-menu")
        else:
            print(f"항복 요청함!!! 응답: {surrender_response}")
            #self.gameEndReward()
            self.__battle_field_repository.lose()
            self.preDrawedBattleFieldFrame.battle_finish()


    def turnEnd(self):
        try:
            turnEndResponse = self.__battleFieldFunctionRepository.requestTurnEnd(
                TurnEndRequest(
                    #_sessionInfo=self.__sessionService.getSessionInfo())
                    _sessionInfo=self.__sessionRepository.get_session_info())
            )

        except Exception as e:
            print(f"turnEnd Error: {e}")


    def gameEndReward(self):
        try:
            gameEndRewardResponse = self.__battleFieldFunctionRepository.requestGameEnd(
                GameEndRewardRequest(
                    # _sessionInfo=self.__sessionService.getSessionInfo())
                    # _sessionInfo=self.__sessionRepository.get_session_info())
                    _sessionInfo=self.__sessionRepository.get_first_fake_session_info())
            )
            print(f"게임 끝! 응답: {gameEndRewardResponse}")
            if gameEndRewardResponse:
                # self.__battle_field_repository.game_end()
                self.__battle_field_repository.reset_game_state()
                self.uiFrameController.switchFrameWithMenuName("lobby-menu")
        except Exception as e:
            print(f"turnEnd Error: {e}")

    def drawYourCard(self, notify_dict_data):
        print(f"notify_dict_data : {notify_dict_data}")
        for data in notify_dict_data.values():
            card_list = data["You"]
            print(f"card_list : {card_list}")
            self.__yourHandRepository.create_additional_hand_card_list(card_list)
        print(f"hand list: {self.__yourHandRepository.get_current_hand_card_list()}")
        print(f"hand state: {self.__yourHandRepository.get_current_hand_state()}")
        #self.__yourHandRepository.replace_hand_card_position()

    def drawOpponentCard(self, notify_dict_data):
        #todo : 아직 opponentHandRepository가 없음.
        # 상대가 뽑은 카드 갯수 만큼 rendering해야함
        for data in notify_dict_data.values():
            card_count = data["Opponent"]
            #self.__opponentHandRepository.add_card_state(card_count)


    def useHandCard(self, notify_dict_data):
        for data in notify_dict_data.values():
            card_data = data["Opponent"]
            #todo : 상대방이 낸 카드를 사용하는 기능을 연결

    def useDeckCardList(self, notify_dict_data):
        for data in notify_dict_data.values():
            card_list = data["Opponent"]
            #Todo : 상대방의 덱에서 직접 카드를 사용하는 기능을 연결


    def attachFieldUnitEnergy(self, notify_dict_data):
        for data in notify_dict_data.values():
            for target_character in data.keys():
                for target_unit_index in data[target_character].keys():
                    for energy_race in data[target_character][target_unit_index]["attached_energy_map"].keys():
                        for race in CardRace:
                            if race.value == int(energy_race):
                                energy_race_data = race.name

                        race_energy_count = data[target_character][target_unit_index]["attached_energy_map"][energy_race]
                        total_energy_count = data[target_character][target_unit_index]["total_energy_count"]

                        result_data = {'energy_race' : int(energy_race), 'race_energy_count': int(race_energy_count),
                                'total_energy_count': int(total_energy_count), 'target_unit_index': int(target_unit_index)}

                        self.preDrawedBattleFieldFrame.attach_energy(result_data)
                        #todo :
                        # target_character => You || Opponent
                        # target_unit_index => 필드에 존재하는 유닛의 index값
                        # energy_race => 에너지의 종족값
                        # race_energy_count => 해당 종족 에너지의 총 갯수
                        # total_energy_count => 모든 종족 에너지의 총 합

    def spawnOpponentUnit(self, notify_dict_data):
        print(f"Spawn Opponent: {notify_dict_data}")
        for data in notify_dict_data.values():
            print(f"data: {data}")
            unit_card_id = data["Opponent"]
            print(f"unit_card_id: {unit_card_id}")
            OpponentFieldUnitRepository.getInstance().create_field_unit_card(int(unit_card_id))


    def searchOpponentCount(self, notify_dict_data):
        for data in notify_dict_data.values():
            search_count = data["Opponent"]


    def searchYourCardList(self, notify_dict_data):
        for data in notify_dict_data.values():
            search_card_list = data["You"]


