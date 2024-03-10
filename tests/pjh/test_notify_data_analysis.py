import unittest

from battle_field.infra.opponent_field_unit_repository import OpponentFieldUnitRepository
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

    def test_notify_use_draw_support_card(self):
        # notice_type : NOTIFY_USE_CATASTROPHIC_DAMAGE_ITEM_CARD
        notify_reader_service = NotifyReaderServiceImpl.getInstance()
        notice_dictionary = {"NOTIFY_USE_DRAW_SUPPORT_CARD":{
            "player_hand_use_map":{
                "Opponent":{
                    "card_id":20,"card_kind":4}},
            "player_draw_count_map":{
                "Opponent":3}}}


if __name__ == "__main__":
    unittest.main()
