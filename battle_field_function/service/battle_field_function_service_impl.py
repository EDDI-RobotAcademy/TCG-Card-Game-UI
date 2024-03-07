from battle_field.infra.battle_field_repository import BattleFieldRepository
from battle_field.infra.legacy.circle_image_legacy_opponent_field_unit_repository import \
    CircleImageLegacyOpponentFieldUnitRepository
from battle_field.infra.legacy.circle_image_legacy_your_hand_repository import CircleImageLegacyYourHandRepository
from battle_field_function.repository.battle_field_function_repository_impl import BattleFieldFunctionRepositoryImpl
from battle_field_function.service.battle_field_function_service import BattleFieldFunctionService
from battle_field_function.service.request.game_end_reward_request import GameEndRewardRequest
from battle_field_function.service.request.surrender_request import SurrenderRequest
from battle_field_function.service.request.turn_end_request import TurnEndRequest
from common.card_race import CardRace
from notify_reader.repository.notify_reader_repository_impl import NotifyReaderRepositoryImpl

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
            cls.__instance.__notify_reader_repository = NotifyReaderRepositoryImpl.getInstance()
            # cls.__instance.__opponentHandRepository = OpponentHandRepository.getInstance()
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

    def saveFrame(self, ui_frame_controller, frame):
        self.preDrawedBattleFieldFrame = frame
        self.uiFrameController = ui_frame_controller

    def surrender(self, switchFrameWithMenuName=None):
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
            # self.gameEndReward()
            self.__battle_field_repository.lose()
            self.preDrawedBattleFieldFrame.battle_finish()
            # from ui_frame.controller.ui_frame_controller_impl import UiFrameControllerImpl
            # UiFrameControllerImpl.getInstance().switchFrameWithMenuName("battle-result")

    def turnEnd(self):
        try:
            turnEndResponse = self.__battleFieldFunctionRepository.requestTurnEnd(
                TurnEndRequest(
                    # _sessionInfo=self.__sessionService.getSessionInfo())
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
        # self.__yourHandRepository.replace_hand_card_position()

    def drawOpponentCard(self, notify_dict_data):
        # todo : 아직 opponentHandRepository가 없음.
        # 상대가 뽑은 카드 갯수 만큼 rendering해야함
        for data in notify_dict_data.values():
            card_count = data["Opponent"]
            # self.__opponentHandRepository.add_card_state(card_count)

    def useHandCard(self, notify_dict_data):
        for data in notify_dict_data.values():
            card_data = data["Opponent"]
            # todo : 상대방이 낸 카드를 사용하는 기능을 연결

    def useDeckCardList(self, notify_dict_data):
        for data in notify_dict_data.values():
            card_list = data["Opponent"]
            # Todo : 상대방의 덱에서 직접 카드를 사용하는 기능을 연결

    def attachFieldUnitEnergy(self, notify_dict_data):
        for data in notify_dict_data.values():
            for target_character in data.keys():
                for target_unit_index in data[target_character].keys():
                    for energy_race in data[target_character][target_unit_index]["attached_energy_map"].keys():
                        for race in CardRace:
                            if race.value == int(energy_race):
                                energy_race_data = race.name

                        race_energy_count = data[target_character][target_unit_index]["attached_energy_map"][
                            energy_race]
                        total_energy_count = data[target_character][target_unit_index]["total_energy_count"]

                        result_data = {'energy_race': int(energy_race), 'race_energy_count': int(race_energy_count),
                                       'total_energy_count': int(total_energy_count),
                                       'target_unit_index': int(target_unit_index)}

                        self.preDrawedBattleFieldFrame.attach_energy(result_data)
                        # todo :
                        # target_character => You || Opponent
                        # target_unit_index => 필드에 존재하는 유닛의 index값
                        # energy_race => 에너지의 종족값
                        # race_energy_count => 해당 종족 에너지의 총 갯수
                        # total_energy_count => 모든 종족 에너지의 총 합

    # protocolNumber: 1000번(기본 공격)
    def basicAttackToUnit(self, notify_dict_data):
    
        is_my_turn = self.__notify_reader_repository.get_is_your_turn_for_check_fake_process()
        if is_my_turn is True:
            return

        your_field_unit_hp_index = None
        your_field_unit_hp = None
        opponent_field_unit_hp_index = None
        opponent_field_unit_hp = None

        your_harmful_status_list = None
        opponent_harmful_status_list = None

        field_unit_health_data = notify_dict_data["player_field_unit_health_point_map"]
        your_field_unit_hp_data = field_unit_health_data["You"]
        your_unit_data = your_field_unit_hp_data["field_unit_health_point_map"]
        for your_unit_index in your_unit_data.keys():
            your_field_unit_hp_index = int(your_unit_index)
            your_field_unit_hp = your_unit_data[your_unit_index]

        opponent_field_unit_hp_data = field_unit_health_data["Opponent"]
        opponent_unit_data = opponent_field_unit_hp_data["field_unit_health_point_map"]
        for opponent_unit_index in opponent_unit_data.keys():
            opponent_field_unit_hp_index = int(opponent_unit_index)
            opponent_field_unit_hp = opponent_unit_data[opponent_unit_index]

        field_unit_harmful_effect_data = notify_dict_data["player_field_unit_harmful_effect_map"]
        your_field_unit_harmful_effect_data = field_unit_harmful_effect_data["You"]
        your_unit_harmful_effect_data = your_field_unit_harmful_effect_data["field_unit_harmful_status_map"]
        for your_unit_index in your_unit_harmful_effect_data.keys():
            your_harmful_status_list = your_unit_harmful_effect_data[your_unit_index]['harmful_status_list']

        opponent_field_unit_harmful_effect_data = field_unit_harmful_effect_data["Opponent"]
        opponent_unit_harmful_effect_data = opponent_field_unit_harmful_effect_data["field_unit_harmful_status_map"]
        for opponent_unit_index in opponent_unit_harmful_effect_data.keys():
            opponent_harmful_status_list = opponent_unit_harmful_effect_data[opponent_unit_index]['harmful_status_list']

        field_unit_death_data = notify_dict_data["player_field_unit_death_map"]
        your_field_unit_death_data = field_unit_death_data["You"]
        your_unit_death_data = your_field_unit_death_data["dead_field_unit_index_list"]

        opponent_field_unit_death_data = field_unit_death_data["Opponent"]
        opponent_unit_death_data = opponent_field_unit_death_data["dead_field_unit_index_list"]

        result = {
            "You": {"index": your_field_unit_hp_index, "hp": your_field_unit_hp,
                    "harmful_status": your_harmful_status_list, "death": your_unit_death_data},
            "Opponent": {"index": opponent_field_unit_hp_index, "hp": opponent_field_unit_hp,
                         "harmful_status": opponent_harmful_status_list, "death": opponent_unit_death_data}}

    #     TOdo
    #      You     : index:피격 유닛 hp:피격 유닛의 체력 harmful_status: 피격 유닛의 해로윤 효과 death:유닛의 인덱스가 있거나 빈 리스트
    #      Opponent: index:공격 유닛 hp:공격 유닛의 체력 harmful_status: 공격 유닛의 해로윤 효과 death:유닛의 인덱스가 있거나 빈 리스트



    # protocolNumber: 1006번(즉사 아이템 사용 - 죽음의 낫)
    def use_instant_unit_death_item_card(self, notify_dict_data):
        # 1006 = {"NOTIFY_USE_INSTANT_UNIT_DEATH_ITEM_CARD":
        #     {"player_hand_use_map":
        #          {"Opponent": {"card_id": 8, "card_kind": 2}},
        #     "player_field_unit_health_point_map":
        #         {"You": {"field_unit_health_point_map": {"0": 0}}},
        #     "player_field_unit_death_map":
        #          {"You": {"dead_field_unit_index_list": [0]}}}}
        print(f"useInstantUnitDeathItemCard() -> notify_dict_data: {notify_dict_data}")

        # if self.__notify
        card_id = (notify_dict_data.get("USE_INSTANT_UNIT_DEATH_ITEM_CARD", {})
                   .get("player_hand_use_map", {})
                   .get("Opponent", {})
                   .get("card_id", None))

        # if self.__
        card_kind = (notify_dict_data.get("USE_INSTANT_UNIT_DEATH_ITEM_CARD", {})
                     .get("player_hand_use_map", {})
                     .get("Opponent", {})
                     .get("card_kind", None))

        # if self.__notify
        field_unit_health_point_map = (notify_dict_data.get("USE_INSTANT_UNIT_DEATH_ITEM_CARD", {})
                                       .get("player_field_unit_health_point_map", {})
                                       .get("You", {})
                                       .get("0", None))

        # if self.__notify
        dead_field_unit_index_list = (notify_dict_data.get("USE_INSTANT_UNIT_DEATH_ITEM_CARD", {})
                                      .get("player_field_unit_death_map", {})
                                      .get("You", {})
                                      .get(None))

    # protocolNumber: 1008번(상대 필드 에너지 제거 서포트 사용 - 죽음의 대지)
    def use_field_energy_support_card(self, notify_dict_data):
        #     1008 = {"NOTIFY_USE_FIELD_ENERGY_REMOVE_SUPPORT_CARD":
        #         {"player_hand_use_map":
        #         {"Opponent": {"card_id": 36, "card_kind": 4}},
        #
        #         "player_field_energy_map":
        #         {"You": 2}}}
        print(f"useFieldEnergySupportCard() -> notify_dict_data: {notify_dict_data}")

        # if self.__notify

        card_id = (notify_dict_data.get("NOTIFY_USE_FIELD_ENERGY_REMOVE_SUPPORT_CARD", {})
                   .get("player_hand_use_map", {})
                   .get("Opponent", {})
                   .get("card_id", None))

        card_kind = (notify_dict_data.get("NOTIFY_USE_FIELD_ENERGY_REMOVE_SUPPORT_CARD", {})
                     .get("player_hand_use_map", {})
                     .get("Opponent", {})
                     .get("card_kind", None))

        # if self.__notify
        you = (notify_dict_data.get("NOTIFY_USE_FIELD_ENERGY_REMOVE_SUPPORT_CARD", {})
               .get("player_field_energy_map", {})
               .get("You", None))

    # protocolNumber: 1009번(필드 에너지 충전 아이템 사용 - 사기 전환)
    def use_general_energy_card_to_unit(self, notify_dict_data):
        # 1009 = {"NOTIFY_USE_FIELD_ENERGY_INCREASE_ITEM_CARD":
        #        {"player_hand_use_map":
        #        {"Opponent": {"card_id": 35, "card_kind": 2}},
        #
        #        "player_field_energy_map":
        #        {"Opponent": 12}}}
        print(f"use_general_energy_card_to_unit() -> notify_dict_data: {notify_dict_data}")

        # if self.__notify_

        card_id = (notify_dict_data.get("NOTIFY_USE_FIELD_ENERGY_INCREASE_ITEM_CARD", {})
                   .get("player_hand_use_map", {})
                   .get("Opponent", {})
                   .get("card_id", None))

        # if self.__notify_

        card_kind = (notify_dict_data.get("NOTIFY_USE_FIELD_ENERGY_INCREASE_ITEM_CARD", {})
                     .get("player_hand_use_map", {})
                     .get("You", {})
                     .get("card_kind", None))

        # if self.__notify_
        opponent = (notify_dict_data.get("NOTIFY_USE_FIELD_ENERGY_INCREASE_ITEM_CARD", {})
                    .get("player_hand_use_map", {})
                    .get("Opponent", None))

    # protocolNumber: 1011번(검색 서포트 카드 사용 - 30 (레오닉의 부름))
    def use_search_deck_support_card(self, notify_dict_data):
        # 1011 = {"NOTIFY_USE_SEARCH_DECK_SUPPORT_CARD":
        #        {"player_hand_use_map":
        #        {"Opponent": {"card_id": 30, "card_kind": 4}},
        #
        #        "player_search_count_map": {"Opponent": 1}}}
        print(f"use_search_deck_support_card() -> notify_dict_data: {notify_dict_data}")

        # if self.__notify_

        card_id = (notify_dict_data.get("NOTIFY_USE_SEARCH_DECK_SUPPORT_CARD", {})
                   .get("player_hand_use_map", {})
                   .get("Opponent", {})
                   .get("card_id", None))

        # if self.__notify_
        card_kind = (notify_dict_data.get("NOTIFY_USE_SEARCH_DECK_SUPPORT_CARD", {})
                     .get("player_hand_use_map", {})
                     .get("Opponent", {})
                     .get("card_kind", None))

        # if self.__notify_
        opponent = (notify_dict_data.get("NOTIFY_USE_SEARCH_DECK_SUPPORT_CARD", {})
                    .get("player_hand_use_map", {})
                    .get("Opponent", None))

    # protocolNumber: 1013번(드로우 서포트 카드 사용 - 망자의 늪)
    def use_draw_support_card(self, notify_dict_data):
        # 1013 = {"NOTIFY_USE_DRAW_SUPPORT_CARD":
        #            {"player_hand_use_map":
        #            {"Opponent": {"card_id": 20, "card_kind": 4}},
        #
        #            "player_draw_count_map":
        #            {"Opponent": 3}}}
        print(f"use_draw_support_card() -> notify_dict_data: {notify_dict_data}")
        # if self.__notify_

        card_id = (notify_dict_data.get("NOTIFY_USE_DRAW_SUPPORT_CARD", {})
                   .get("player_hand_use_map", {})
                   .get("Opponent", {})
                   .get("card_id", None))

        # if self.__notify_

        card_kind = (notify_dict_data.get("NOTIFY_USE_DRAW_SUPPORT_CARD", {})
                     .get("player_hand_use_map", {})
                     .get("Opponent", {})
                     .get("card_kind", None))

        # if self.__notify_

        opponent = (notify_dict_data.get("NOTIFY_USE_DRAW_SUPPORT_CARD", {})
                    .get("player_hand_use_map", {})
                    .get("Opponent", None))

    def spawnOpponentUnit(self, notify_dict_data):
        print(f"Spawn Opponent: {notify_dict_data}")
        for data in notify_dict_data.values():
            print(f"data: {data}")
            unit_card_id = data["Opponent"]
            print(f"unit_card_id: {unit_card_id}")
            CircleImageLegacyOpponentFieldUnitRepository.getInstance().create_field_unit_card(int(unit_card_id))

    def basicAttackToMainCharacter(self, _notify_dict_data):
        notify_dict_data = _notify_dict_data['NOTIFY_BASIC_ATTACK_TO_MAIN_CHARACTER']

        is_my_turn = self.__notify_reader_repository.get_is_your_turn_for_check_fake_process()
        print(f"is my turn: {is_my_turn}")
        if is_my_turn is True:
            return

        target_character = list(notify_dict_data.get("player_main_character_health_point_map", {}).keys())[0]

        character_hp = int(notify_dict_data.get("player_main_character_health_point_map", {})[target_character])

        if notify_dict_data.get("player_main_character_survival_map", {})[target_character] == "Survival":
            character_survival = True
        else:
            character_survival = False

        result = {"target_character": target_character, "character_hp": character_hp,
                  "character_survival": character_survival}
        print(result)
        self.preDrawedBattleFieldFrame.damage_to_main_character(result)

    def useUnitEnergyRemoveItemCard(self, _notify_dict_data):

        is_my_turn = self.__notify_reader_repository.get_is_your_turn_for_check_fake_process()
        print(f"is my turn: {is_my_turn}")
        if is_my_turn is True:
            return

        notify_dict_data = _notify_dict_data['NOTIFY_USE_UNIT_ENERGY_REMOVE_ITEM_CARD']
        print(notify_dict_data)

        hand_use_card_id = int(notify_dict_data.get("player_hand_use_map", {})
                               .get("Opponent", {})
                               .get("card_id", None))
        print(hand_use_card_id)
        if notify_dict_data.get("player_field_unit_energy_map") != {}:
            field_unit_index = list(notify_dict_data.get("player_field_unit_energy_map", {})
                                    .get("You", {})
                                    .get("field_unit_energy_map", {}).keys())[0]
            print(field_unit_index)

            attach_total_energy_count = int(notify_dict_data.get("player_field_unit_energy_map", {})
                                            .get("You", {})
                                            .get("field_unit_energy_map", {})[field_unit_index]
                                            .get("total_energy_count", None))
            print(attach_total_energy_count)

            if attach_total_energy_count != 0:
                attach_energy_race_type = list(notify_dict_data.get("player_field_unit_energy_map", {})
                                               .get("You", {})
                                               .get("field_unit_energy_map", {})[field_unit_index]
                                               .get("attached_energy_map", {}).keys())[0]
                print(attach_energy_race_type)
                attach_race_energy_count = (notify_dict_data.get("player_field_unit_energy_map", {})
                .get("You", {})
                .get("field_unit_energy_map", {})[field_unit_index]
                .get("attached_energy_map", {})[attach_energy_race_type])

                print(attach_race_energy_count)
                attach_energy_race_type = int(attach_energy_race_type)
                attach_race_energy_count = int(attach_race_energy_count)
            else:
                attach_energy_race_type = None
                attach_race_energy_count = 0

            field_unit_index = int(field_unit_index)


            result = {
                "hand_use_card_id": hand_use_card_id,
                "field_unit_index": field_unit_index, "attach_energy_race_type": attach_energy_race_type,
                "attach_race_energy_count": attach_race_energy_count,
                "attach_total_energy_count": attach_total_energy_count
            }

            print(f"result : {result}")
            self.preDrawedBattleFieldFrame.detach_energy_to_your_unit(result)


        else:
            field_unit_index = int(list(notify_dict_data.get("player_field_unit_health_point_map", {})
                                        .get("You", {})
                                        .get("field_unit_health_point_map", {}).keys())[0])

            field_unit_hp = int(list(notify_dict_data.get("player_field_unit_health_point_map", {})
                                     .get("You", {})
                                     .get("field_unit_health_point_map", {}).values())[0])

            dead_field_unit_index_list = list(notify_dict_data.get("player_field_unit_death_map", {})
                                              .get("You", {})
                                              .get("dead_field_unit_index_list", []))

            result = {
                "hand_use_card_id": hand_use_card_id,
                "field_unit_index": field_unit_index, "field_unit_hp": field_unit_hp,
                "dead_field_unit_index_list": dead_field_unit_index_list
            }

            self.preDrawedBattleFieldFrame.damage_to_your_field_unit(result)

        print(result)

    def useMultipleUnitDamageItemCard(self, notify_dict_data):

        is_my_turn = self.__notify_reader_repository.get_is_your_turn_for_check_fake_process()
        if is_my_turn is True:
            return

        hand_use_card_id = int(notify_dict_data.get("player_hand_use_map", {})
                               .get("Opponent", {})
                               .get("card_id", None))

        string_target_unit_index_list = list(notify_dict_data.get("player_field_unit_health_point_map", {})
                                             .get("You", {})
                                             .get("field_unit_health_point_map", {}).keys())
        target_unit_index_list = []
        for unit_index in string_target_unit_index_list:
            target_unit_index_list.append(int(unit_index))

        target_unit_hp_list = list(notify_dict_data.get("player_field_unit_health_point_map", {})
                                   .get("You", {})
                                   .get("field_unit_health_point_map", {}).values())

        opponent_dead_field_unit_index_list = (notify_dict_data.get("player_field_unit_death_map", {})
                                               .get("Opponent", {})
                                               .get("dead_field_unit_index_list", []))

        your_dead_field_unit_index_list = (notify_dict_data.get("player_field_unit_death_map", {})
                                           .get("You", {})
                                           .get("dead_field_unit_index_list", []))

        result = {
            "hand_use_card_id": hand_use_card_id, "target_unit_index_list": target_unit_index_list,
            "target_unit_hp_list": target_unit_hp_list,
            "opponent_dead_field_unit_index_list": opponent_dead_field_unit_index_list,
            "your_dead_field_unit_index_list": your_dead_field_unit_index_list
        }

    def useSpecialEnergyCardToUnit(self, _notify_dict_data):

        is_my_turn = self.__notify_reader_repository.get_is_your_turn_for_check_fake_process()
        if is_my_turn is True:
            return

        notify_dict_data = _notify_dict_data['NOTIFY_USE_SPECIAL_ENERGY_CARD_TO_UNIT']

        hand_use_card_id = int(notify_dict_data.get("player_hand_use_map", {})
                               .get("Opponent", {})
                               .get("card_id", None))

        field_unit_index =  list(notify_dict_data.get("player_field_unit_energy_map", {})
                            .get("Opponent", {}).get("field_unit_energy_map", {}).keys())[0]

        attach_energy_race_type = list(notify_dict_data.get("player_field_unit_energy_map", {})
                                      .get("Opponent", {}).get("field_unit_energy_map", {})[field_unit_index]
                                      .get("attached_energy_map", {}).keys())[0]

        attach_race_energy_count = (notify_dict_data.get("player_field_unit_energy_map", {})
                                       .get("Opponent", {}).get("field_unit_energy_map", {})[field_unit_index]
                                       .get("attached_energy_map", {})[attach_energy_race_type])

        attach_total_energy_count = int(notify_dict_data.get("player_field_unit_energy_map", {})
                                        .get("Opponent", {})
                                        .get("field_unit_energy_map", {})[field_unit_index]
                                        .get("total_energy_count", None))

        extra_effect_list = (notify_dict_data.get("player_field_unit_extra_effect_map", {})
                             .get("Opponent",{})
                             .get("field_unit_extra_effect_map", {})[field_unit_index]
                             .get("extra_effect_list",[])
                             )

        field_unit_index = int(field_unit_index)
        attach_energy_race_type = int(attach_energy_race_type)
        attach_race_energy_count = int(attach_race_energy_count)

        result = {
            "hand_use_card_id" : hand_use_card_id, "field_unit_index" : field_unit_index,
            "attach_energy_race_type" : attach_energy_race_type, "attach_race_energy_count" : attach_race_energy_count,
            "attach_total_energy_count": attach_total_energy_count, "extra_effect_list" : extra_effect_list
        }

        print(f"special energy notify result : {result}")

    def useGeneralEnergyCardToUnit(self, _notify_dict_data):

        is_my_turn = self.__notify_reader_repository.get_is_your_turn_for_check_fake_process()
        if is_my_turn is True:
            return

        print("use General Energy Card To Unit!! ", _notify_dict_data)
        notify_dict_data = _notify_dict_data["NOTIFY_USE_GENERAL_ENERGY_CARD_TO_UNIT"]
        print(f"notify dict data: {notify_dict_data}")
        try:
            hand_use_card_id = int(notify_dict_data.get("player_hand_use_map", {})
                                   .get("Opponent", {})
                                   .get("card_id", None))
            print(hand_use_card_id)

            field_unit_index = list(notify_dict_data.get("player_field_unit_energy_map", {})
                                    .get("Opponent", {})
                                    .get("field_unit_energy_map", {}).keys())[0]

            print(field_unit_index)

            attach_energy_race_type = list(notify_dict_data.get("player_field_unit_energy_map", {})
                                           .get("Opponent", {})
                                           .get("field_unit_energy_map", {})[field_unit_index]
                                           .get("attached_energy_map", {}).keys())[0]
            print(attach_energy_race_type)
            attach_race_energy_count = (notify_dict_data.get("player_field_unit_energy_map", {})
                                            .get("Opponent", {})
                                            .get("field_unit_energy_map", {})[field_unit_index]
                                            .get("attached_energy_map", {})[attach_energy_race_type])
            print(attach_race_energy_count)
            attach_total_energy_count = int(notify_dict_data.get("player_field_unit_energy_map", {})
                                            .get("Opponent", {})
                                            .get("field_unit_energy_map", {})[field_unit_index]
                                            .get("total_energy_count", None))
            print(attach_total_energy_count)
            field_unit_index = int(field_unit_index)
            attach_energy_race_type = int(attach_energy_race_type)
            attach_race_energy_count = int(attach_race_energy_count)

            result = {
                "hand_use_card_id": hand_use_card_id, "field_unit_index": field_unit_index,
                "attach_energy_race_type": attach_energy_race_type, "attach_race_energy_count": attach_race_energy_count,
                "attach_total_energy_count": attach_total_energy_count
            }

            print(f"result : {result}")

            self.preDrawedBattleFieldFrame.attach_energy_to_opponent_unit(result)
        except Exception as e:
            print(f"Notify Error : {e}")


    def searchOpponentCount(self, notify_dict_data):
        for data in notify_dict_data.values():
            search_count = data["Opponent"]

    def searchYourCardList(self, notify_dict_data):
        for data in notify_dict_data.values():
            search_card_list = data["You"]
