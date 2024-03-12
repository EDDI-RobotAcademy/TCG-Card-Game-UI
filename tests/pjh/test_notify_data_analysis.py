import unittest

from battle_field.infra.opponent_field_unit_repository import OpponentFieldUnitRepository
from battle_field.infra.opponent_hand_repository import OpponentHandRepository
from battle_field.infra.your_deck_repository import YourDeckRepository
from battle_field.infra.your_field_unit_repository import YourFieldUnitRepository
from battle_field.infra.your_lost_zone_repository import YourLostZoneRepository
from card_info_from_csv.controller.card_info_from_csv_controller_impl import CardInfoFromCsvControllerImpl
from notify_reader.service.notify_reader_service_impl import NotifyReaderServiceImpl
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage


# OpponentFieldUnitRepository.getInstance()
# OpponentFieldEnergyRepository.getInstance()
# YourFieldEnergyRepository.getInstance()
# YourHandRepository.getInstance()
# FakeOpponentHandRepositoryImpl.getInstance()
# YourHpRepository.getInstance()
# YourTombRepository.getInstance()
# OpponentTombRepository.getInstance()
# YourFieldUnitRepository.getInstance()
# OpponentHandRepository.getInstance()


class TestNotifyDataAnalysis(unittest.TestCase):
    def test_notify_use_special_energy_card_to_unit(self):
        # notice_type : NOTIFY_USE_SPECIAL_ENERGY_CARD_TO_UNIT
        card_date_csv_controller = CardInfoFromCsvControllerImpl.getInstance()
        card_date_csv_controller.requestToCardInfoSettingInMemory()

        pre_draw = PreDrawedImage.getInstance()
        pre_draw.pre_draw_every_image()

        opponent_field_unit_repository = OpponentFieldUnitRepository.getInstance()
        opponent_field_unit_repository.create_field_unit_card(31)
        opponent_field_unit_repository.attach_race_energy(0, 2, 2)

        notify_reader_service = NotifyReaderServiceImpl.getInstance()
        notice_dictionary = {"NOTIFY_USE_SPECIAL_ENERGY_CARD_TO_UNIT":{
            "player_hand_use_map":{
                "Opponent":{
                    "card_id":151,"card_kind":6}},
            "player_field_unit_energy_map":{
                "Opponent":{
                    "field_unit_energy_map":{
                        "0":{"attached_energy_map":{"2":3},"total_energy_count":3}}}},
            "player_field_unit_extra_effect_map":{
                "Opponent":{
                    "field_unit_extra_effect_map":{
                        "0":{"extra_effect_list":["DarkFire","Freeze"]}}}}}}

        notify_reader_service.notify_use_special_energy_card_to_unit(notice_dictionary)

    def test_notify_use_catastrophic_damage_item_card(self):
        # notice_type : NOTIFY_USE_CATASTROPHIC_DAMAGE_ITEM_CARD
        card_date_csv_controller = CardInfoFromCsvControllerImpl.getInstance()
        card_date_csv_controller.requestToCardInfoSettingInMemory()

        pre_draw = PreDrawedImage.getInstance()
        pre_draw.pre_draw_every_image()

        your_deck_repository = YourDeckRepository.getInstance()
        your_deck_repository.save_deck_state([35, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

        your_field_unit_repository = YourFieldUnitRepository.getInstance()
        your_field_unit_repository.create_field_unit_card(27)
        your_field_unit_repository.create_field_unit_card(27)
        your_field_unit_repository.create_field_unit_card(31)
        your_field_unit_repository.create_field_unit_card(31)
        your_field_unit_repository.create_field_unit_card(31)
        your_field_unit_repository.create_field_unit_card(26)

        your_lost_zone_repository = YourLostZoneRepository.getInstance()
        your_lost_zone_repository.create_your_lost_zone_card_list()

        notify_reader_service = NotifyReaderServiceImpl.getInstance()
        notice_dictionary = {"NOTIFY_USE_CATASTROPHIC_DAMAGE_ITEM_CARD":{
            "player_hand_use_map":{
                "Opponent":{
                    "card_id":25,"card_kind":2}},
            "player_field_unit_health_point_map":{
                "You":{
                    "field_unit_health_point_map":{"1":5,"3":0,"2":0,"4":0,"0":5,"5":10}}},
            "player_field_unit_death_map":{
                "You":{
                    "dead_field_unit_index_list":[2,3,4]}},
            "player_main_character_health_point_map":{
                "You":90},
            "player_main_character_survival_map":{
                "You":"Survival"},
            "player_deck_card_lost_list_map":{
                "You":[35]}}}

        notify_reader_service.notify_use_catastrophic_damage_item_card(notice_dictionary)

    def test_notify_use_draw_support_card(self):
        # notice_type : NOTIFY_USE_DRAW_SUPPORT_CARD
        card_date_csv_controller = CardInfoFromCsvControllerImpl.getInstance()
        card_date_csv_controller.requestToCardInfoSettingInMemory()

        pre_draw = PreDrawedImage.getInstance()
        pre_draw.pre_draw_every_image()

        notify_reader_service = NotifyReaderServiceImpl.getInstance()
        notice_dictionary = {"NOTIFY_USE_DRAW_SUPPORT_CARD":{
            "player_hand_use_map":{
                "Opponent":{
                    "card_id":20,"card_kind":4}},
            "player_draw_count_map":{
                "Opponent":3}}}

        opponent_hand_repository = OpponentHandRepository.getInstance()
        opponent_hand_repository.create_opponent_hand_card_list()

        notify_reader_service.notify_use_draw_support_card(notice_dictionary)

    def test_notify_use_multiple_unit_damage_item_card(self):
        # notice_type : NOTIFY_USE_MULTIPLE_UNIT_DAMAGE_ITEM_CARD
        card_date_csv_controller = CardInfoFromCsvControllerImpl.getInstance()
        card_date_csv_controller.requestToCardInfoSettingInMemory()

        pre_draw = PreDrawedImage.getInstance()
        pre_draw.pre_draw_every_image()

        your_field_unit_repository = YourFieldUnitRepository.getInstance()
        your_field_unit_repository.create_field_unit_card(27)
        your_field_unit_repository.create_field_unit_card(27)

        opponent_field_unit_repository = OpponentFieldUnitRepository.getInstance()
        opponent_field_unit_repository.create_field_unit_card(31)

        notify_reader_service = NotifyReaderServiceImpl.getInstance()
        notice_dictionary = {"NOTIFY_USE_MULTIPLE_UNIT_DAMAGE_ITEM_CARD": {
            "player_hand_use_map": {
                "Opponent": {
                    "card_id": 33, "card_kind": 2}},
            "player_field_unit_health_point_map": {
                "You": {
                    "field_unit_health_point_map": {"1": 10, "0": 10}}},
            "player_field_unit_death_map": {
                "Opponent": {
                    "dead_field_unit_index_list": [0]},
                "You": {
                    "dead_field_unit_index_list": []}}}}

        notify_reader_service.notify_use_multiple_unit_damage_item_card(notice_dictionary)

    def test_notify_turn_start_targeting_attack_skill_to_unit(self):
        card_date_csv_controller = CardInfoFromCsvControllerImpl.getInstance()
        card_date_csv_controller.requestToCardInfoSettingInMemory()

        pre_draw = PreDrawedImage.getInstance()
        pre_draw.pre_draw_every_image()

        your_field_unit_repository = YourFieldUnitRepository.getInstance()
        your_field_unit_repository.create_field_unit_card(27)
        your_field_unit_repository.create_field_unit_card(27)

        notify_reader_service = NotifyReaderServiceImpl.getInstance()
        notice_dictionary = {"NOTIFY_TURN_START_TARGETING_ATTACK_PASSIVE_SKILL_TO_UNIT": {
            "player_field_unit_health_point_map": {
                "You": {
                    "field_unit_health_point_map": {
                        "0": 5}}},
            "player_field_unit_harmful_effect_map": {
                "You": {
                    "field_unit_harmful_status_map": {
                        "0": {"harmful_status_list": ['DarkFire', 'Freeze']}}}},
            "player_field_unit_death_map": {
                "You": {
                    "dead_field_unit_index_list": [1]}}}}

        notify_reader_service.notify_turn_start_targeting_attack_passive_skill_to_unit(notice_dictionary)

    def test_notify_deploy_targeting_attack_skill_to_unit(self):
        card_date_csv_controller = CardInfoFromCsvControllerImpl.getInstance()
        card_date_csv_controller.requestToCardInfoSettingInMemory()

        pre_draw = PreDrawedImage.getInstance()
        pre_draw.pre_draw_every_image()

        your_field_unit_repository = YourFieldUnitRepository.getInstance()
        your_field_unit_repository.create_field_unit_card(27)
        your_field_unit_repository.create_field_unit_card(27)

        notify_reader_service = NotifyReaderServiceImpl.getInstance()
        notice_dictionary = {"NOTIFY_DEPLOY_TARGETING_ATTACK_PASSIVE_SKILL_TO_UNIT":{
            "player_field_unit_health_point_map": {
                "You": {
                    "field_unit_health_point_map": {
                        "0": 5}}},
            "player_field_unit_harmful_effect_map": {
                "You": {
                    "field_unit_harmful_status_map": {
                        "0": {"harmful_status_list": ['DarkFire', 'Freeze']}}}},
            "player_field_unit_death_map": {
                "You": {
                    "dead_field_unit_index_list": [1]}}}}

        notify_reader_service.notify_deploy_targeting_attack_passive_skill_to_unit(notice_dictionary)

    def test_notify_turn_start_non_targeting_attack_passive_skill(self):
        card_date_csv_controller = CardInfoFromCsvControllerImpl.getInstance()
        card_date_csv_controller.requestToCardInfoSettingInMemory()

        pre_draw = PreDrawedImage.getInstance()
        pre_draw.pre_draw_every_image()

        your_field_unit_repository = YourFieldUnitRepository.getInstance()
        your_field_unit_repository.create_field_unit_card(27)
        your_field_unit_repository.create_field_unit_card(27)

        notify_reader_service = NotifyReaderServiceImpl.getInstance()
        notice_dictionary = {"NOTIFY_TURN_START_NON_TARGETING_ATTACK_PASSIVE_SKILL": {
            "player_field_unit_health_point_map": {
                "You": {
                    "field_unit_health_point_map": {
                        "0": 5}}},
            "player_field_unit_harmful_effect_map": {
                "You": {
                    "field_unit_harmful_status_map": {
                        "0": {"harmful_status_list": ['DarkFire', 'Freeze']}}}},
            "player_field_unit_death_map": {
                "You": {
                    "dead_field_unit_index_list": [1]}}}}

        notify_reader_service.notify_turn_start_non_targeting_attack_passive_skill(notice_dictionary)

    def test_notify_deploy_non_targeting_attack_passive_skill(self):
        card_date_csv_controller = CardInfoFromCsvControllerImpl.getInstance()
        card_date_csv_controller.requestToCardInfoSettingInMemory()

        pre_draw = PreDrawedImage.getInstance()
        pre_draw.pre_draw_every_image()

        your_field_unit_repository = YourFieldUnitRepository.getInstance()
        your_field_unit_repository.create_field_unit_card(27)
        your_field_unit_repository.create_field_unit_card(27)
        your_field_unit_repository.create_field_unit_card(27)
        your_field_unit_repository.create_field_unit_card(27)

        notify_reader_service = NotifyReaderServiceImpl.getInstance()
        notice_dictionary = {"NOTIFY_DEPLOY_NON_TARGETING_ATTACK_PASSIVE_SKILL": {
            "player_field_unit_health_point_map": {
                "You": {
                    "field_unit_health_point_map": {"3": 0, "1": 0, "2": 0, "0": 10}}},
            "player_field_unit_harmful_effect_map": {
                "You": {
                    "field_unit_harmful_status_map": {
                      "3": {"harmful_status_list": ['DarkFire', 'Freeze']},
                      "1": {"harmful_status_list": ['DarkFire', 'Freeze']},
                      "2": {"harmful_status_list": ['DarkFire', 'Freeze']},
                      "0": {"harmful_status_list": ['DarkFire', 'Freeze']}}}},
            "player_field_unit_death_map": {
                "You": {
                    "dead_field_unit_index_list": [1, 2, 3]}}}}

        notify_reader_service.notify_deploy_non_targeting_attack_passive_skill(notice_dictionary)

    def test_notify_turn_start_targeting_attack_to_game_main_character(self):
        card_date_csv_controller = CardInfoFromCsvControllerImpl.getInstance()
        card_date_csv_controller.requestToCardInfoSettingInMemory()

        pre_draw = PreDrawedImage.getInstance()
        pre_draw.pre_draw_every_image()

        notify_reader_service = NotifyReaderServiceImpl.getInstance()
        notice_dictionary = {"NOTIFY_TURN_START_TARGETING_ATTACK_TO_GAME_MAIN_CHARACTER":{
            "player_main_character_health_point_map":{
                "You":60},
            "player_main_character_survival_map":{
                "You":"Survival"}}}

        notify_reader_service.notify_turn_start_targeting_attack_to_game_main_character(notice_dictionary)

    def test_notify_deploy_targeting_attack_to_game_main_character(self):
        card_date_csv_controller = CardInfoFromCsvControllerImpl.getInstance()
        card_date_csv_controller.requestToCardInfoSettingInMemory()

        pre_draw = PreDrawedImage.getInstance()
        pre_draw.pre_draw_every_image()

        notify_reader_service = NotifyReaderServiceImpl.getInstance()
        notice_dictionary = {"NOTIFY_DEPLOY_TARGETING_ATTACK_TO_GAME_MAIN_CHARACTER":{
            "player_main_character_health_point_map":{
                "You":80},
            "player_main_character_survival_map":{
                "You":"Survival"}}}

        notify_reader_service.notify_deploy_targeting_attack_to_game_main_character(notice_dictionary)


if __name__ == "__main__":
    unittest.main()
