import unittest

from colorama import Fore, Style

from battle_field.infra.opponent_field_unit_repository import OpponentFieldUnitRepository
from battle_field.infra.your_field_energy_repository import YourFieldEnergyRepository
from battle_field.infra.opponent_hand_repository import OpponentHandRepository
from battle_field.infra.your_deck_repository import YourDeckRepository
from battle_field.infra.your_field_unit_repository import YourFieldUnitRepository
from battle_field.infra.your_lost_zone_repository import YourLostZoneRepository
from card_info_from_csv.controller.card_info_from_csv_controller_impl import CardInfoFromCsvControllerImpl
from notify_reader.service.notify_reader_service_impl import NotifyReaderServiceImpl
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage
from battle_field.state.current_field_unit import CurrentFieldUnitState


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
    def test_notify_use_unit_energy_boost_support(self):
        # notice_type : NOTIFY_USE_UNIT_ENERGY_BOOST_SUPPORT_CARD
        card_date_csv_controller = CardInfoFromCsvControllerImpl.getInstance()
        card_date_csv_controller.requestToCardInfoSettingInMemory()

        pre_draw = PreDrawedImage.getInstance()
        pre_draw.pre_draw_every_image()

        opponent_field_unit_repository = OpponentFieldUnitRepository.getInstance()
        opponent_field_unit_repository.create_field_unit_card(31)

        notify_reader_service = NotifyReaderServiceImpl.getInstance()
        notice_dictionary = {"NOTIFY_USE_UNIT_ENERGY_BOOST_SUPPORT_CARD":{
            "player_hand_use_map":{
                "Opponent":{
                    "card_id":2,"card_kind":4}},
            "player_deck_card_use_list_map":{
                "Opponent":[93, 93]},
            "player_field_unit_energy_map":{
                "Opponent":{
                    "field_unit_energy_map":{
                        "0":{"attached_energy_map":{"2":2},"total_energy_count":2}}}}}}

        notify_reader_service.notify_use_unit_energy_boost_support(notice_dictionary)

    def test_notify_use_instant_unit_death_item_card(self):
        # notice_type : NOTIFY_USE_INSTANT_UNIT_DEATH_ITEM_CARD
        card_date_csv_controller = CardInfoFromCsvControllerImpl.getInstance()
        card_date_csv_controller.requestToCardInfoSettingInMemory()

        pre_draw = PreDrawedImage.getInstance()
        pre_draw.pre_draw_every_image()

        your_field_unit_repository = YourFieldUnitRepository.getInstance()
        your_field_unit_repository.create_field_unit_card(27)

        notify_reader_service = NotifyReaderServiceImpl.getInstance()
        notice_dictionary = {"NOTIFY_USE_INSTANT_UNIT_DEATH_ITEM_CARD":
            {"player_hand_use_map":
                 {"Opponent":
                      {"card_id": 8, "card_kind": 2}},
            "player_field_unit_health_point_map":
                {"You":
                     {"field_unit_health_point_map": {"0": 0}}},
            "player_field_unit_death_map":
                 {"You":
                      {"dead_field_unit_index_list": [0]}}}}

        your_field_unit_repository.create_field_unit_card_list()

        print(f"current_hand_list_before_test: {your_field_unit_repository.current_field_unit_list}")

        notify_reader_service.notify_use_instant_unit_death_item_card(notice_dictionary)

        print(f"current_hand_list_after_test: {your_field_unit_repository.current_field_unit_list}")

    def test_notify_use_field_energy_remove_support_card(self):
        # notice_type : NOTIFY_USE_FIELD_ENERGY_REMOVE_SUPPORT_CARD
        card_date_csv_controller = CardInfoFromCsvControllerImpl.getInstance()
        card_date_csv_controller.requestToCardInfoSettingInMemory()

        pre_draw = PreDrawedImage.getInstance()
        pre_draw.pre_draw_every_image()

        your_field_energy_repository = YourFieldEnergyRepository.getInstance()
        your_field_energy_repository.set_your_field_energy(10)

        notify_reader_service = NotifyReaderServiceImpl.getInstance()
        notice_dictionary = {"NOTIFY_USE_FIELD_ENERGY_REMOVE_SUPPORT_CARD":
                    {"player_hand_use_map":
                         {"Opponent":
                              {"card_id":36,"card_kind":4}},
                     "player_field_energy_map":
                         {"You":2}}}

        print(f"{Fore.RED}your_field_energy_list_before_test: {Fore.GREEN}{your_field_energy_repository.get_your_field_energy()}{Style.RESET_ALL}")

        notify_reader_service.notify_use_field_energy_remove_support_card(notice_dictionary)

        print(f"{Fore.RED}your_field_energy_list_after_test: {Fore.GREEN}{your_field_energy_repository.get_your_field_energy()}{Style.RESET_ALL}")


if __name__ == "__main__":
    unittest.main()
