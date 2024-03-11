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

if __name__ == "__main__":
    unittest.main()
