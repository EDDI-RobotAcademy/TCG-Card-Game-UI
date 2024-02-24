from battle_field.infra.opponent_field_unit_repository import OpponentFieldUnitRepository
from battle_field.infra.your_hand_repository import YourHandRepository
from card_info_from_csv.repository.card_info_from_csv_repository_impl import CardInfoFromCsvRepositoryImpl
from common.card_grade import CardGrade
from common.card_race import CardRace
from common.card_type import CardType
from image_shape.circle_kinds import CircleKinds
from image_shape.circle_number_image import CircleNumberImage
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage


class FixedUnitCardInsideHandler:
    __instance = None
    __pre_drawed_image_instance = PreDrawedImage.getInstance()
    __opponent_field_unit_repository = OpponentFieldUnitRepository.getInstance()


    def __new__(cls,
                your_hand_repository,
                your_field_unit_repository,
                card_info):

        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

            cls.__instance.your_hand_repository = your_hand_repository
            cls.__instance.your_field_unit_repository = your_field_unit_repository
            cls.__instance.card_info = card_info

        return cls.__instance

    @classmethod
    def getInstance(cls,
                    your_hand_repository,
                    your_field_unit_repository,
                    card_info):

        if cls.__instance is None:
            cls.__instance = cls(your_hand_repository,
                                 your_field_unit_repository,
                                 card_info)
        return cls.__instance

    def handle_pickable_card_inside_unit(self, selected_object, x, y):
        print(f"handle_pickable_card_inside_unit: {selected_object}, {x}, {y}")
        card_type = self.card_info.getCardTypeForCardNumber(selected_object.get_card_number())
        print(f"card_type: {card_type}")
        print(f"TOOL value: {CardType.TOOL.value}, ENERGY value: {CardType.ENERGY.value}")

        if card_type not in [CardType.TOOL.value, CardType.ENERGY.value]:
            return

        print("can I pass uppon condition ?")

        field_unit_list = self.your_field_unit_repository.get_current_field_unit_list()

        for unit_index, field_unit in enumerate(field_unit_list):
            if field_unit.get_fixed_card_base().is_point_inside((x, y)):
                self.handle_inside_field_unit(selected_object, unit_index)
                return True

        return False

    def handle_inside_field_unit(self, selected_object, your_unit_index):
        placed_card_id = selected_object.get_card_number()
        card_type = self.card_info.getCardTypeForCardNumber(placed_card_id)

        placed_card_index = self.your_hand_repository.find_index_by_selected_object(selected_object)

        if card_type == CardType.TOOL.value:
            self.handle_tool_card(placed_card_index)
        elif card_type == CardType.ENERGY.value:
            self.handle_energy_card(placed_card_index, your_unit_index, selected_object)


    def handle_tool_card(self, placed_card_index):
        print("도구를 붙입니다!")
        # self.your_hand_repository.remove_card_by_id(placed_card_id)
        self.your_hand_repository.remove_card_by_index(placed_card_index)
        self.your_hand_repository.replace_hand_card_position()

    def handle_energy_card(self, placed_card_index, your_unit_index, selected_object):
        print("에너지를 붙입니다!")
        # self.your_hand_repository.remove_card_by_id(placed_card_id)
        self.your_hand_repository.remove_card_by_index(placed_card_index)
        self.your_field_unit_repository.get_attached_energy_info().add_energy_at_index(your_unit_index, 1)
        self.your_hand_repository.replace_hand_card_position()

        your_fixed_field_unit = self.your_field_unit_repository.find_field_unit_by_index(your_unit_index)
        fixed_card_base = your_fixed_field_unit.get_fixed_card_base()
        fixed_card_attached_shape_list = fixed_card_base.get_attached_shapes()
        placed_card_id = selected_object.get_card_number()
        print(f"placed_card_id : {placed_card_id}")
        print(f"card grade : {self.card_info.getCardGradeForCardNumber(placed_card_id)}")

        attached_energy_count = self.your_field_unit_repository.get_attached_energy_info().get_energy_at_index(your_unit_index)

        # todo : 특수에너지의 갯수가 많아지면 카드 넘버로 특정 지어야 함
        # todo : 이미지가 추가되면 pre_drawed를 설정 후 불러와야함
        if self.card_info.getCardGradeForCardNumber(placed_card_id) == CardGrade.HERO.value:
             # card_freezing_image_circle = your_fixed_field_unit.creat_fixed_card_freezing_image_circle(image_data=self.__pre_drawed_image_instance.,
             #                                                                                           vertices=(45, 150),
             #                                                                                           local_translation=fixed_card_base.get_local_translation()
             #                                                                                           )
             # card_dark_flame_image_circle = your_fixed_field_unit.creat_fixed_card_dark_flame_image_circle(image_data=self.__pre_drawed_image_instance.,
             #                                                                                               vertices=(60, 150),
             #                                                                                               local_translation=fixed_card_base.get_local_translation()
             #                                                                                               )
             # fixed_card_base.set_attached_shapes(card_freezing_image_circle)
             # fixed_card_base.set_attached_shapes(card_dark_flame_image_circle)
             pass

        # 에너지 circle부분 확인 후 교체작업
        for fixed_card_attached_shape in fixed_card_attached_shape_list:
            if isinstance(fixed_card_attached_shape, CircleNumberImage):
                if fixed_card_attached_shape.get_circle_kinds() is CircleKinds.ENERGY:
                    fixed_card_attached_shape.set_image_data(self.__pre_drawed_image_instance.get_pre_draw_number_image(attached_energy_count))
                    print(f"changed energy: {fixed_card_attached_shape.get_circle_kinds()}")


        # 에너지 카드의 종족의 따라 circle 색이 달라짐
        # todo : race에 따른 circle color 추가 요망
        card_race = self.card_info.getCardRaceForCardNumber(placed_card_id)
        if card_race == CardRace.UNDEAD.value:
            card_race_circle = your_fixed_field_unit.creat_fixed_card_energy_race_circle(color=(0, 0, 0, 1),
                                                                                         vertices=(0, (attached_energy_count * 10) + 20),
                                                                                         local_translation=fixed_card_base.get_local_translation())
            fixed_card_base.set_attached_shapes(card_race_circle)

        fixed_card_base.draw()


        print(f"에너지 상태: {self.your_field_unit_repository.get_attached_energy_info().get_energy_at_index(your_unit_index)}")
        # TODO: attached_energy 값 UI에 표현 (이미지 작업 미완료)
        # TODO: 특수 에너지 붙인 것을 어떻게 표현 할 것인가 ? (아직 미정)

    def field_fixed_unit_card_choice_opponent_unit(self, selected_object, x, y):
        print(f"field_fixed_card_inside_unit: {selected_object}, {x}, {y}")
        card_type = self.card_info.getCardTypeForCardNumber(selected_object.get_card_number())
        print(f"card_type: {card_type}")

        if card_type not in [CardType.UNIT.value]:
            return

        opponent_field_unit_list = self.__opponent_field_unit_repository.get_current_field_unit_card_object_list()

        for opponent_unit_index, opponent_field_unit in enumerate(opponent_field_unit_list):
            if opponent_field_unit.get_fixed_card_base().is_point_inside((x, y)):
                self.field_inside_field_unit(selected_object, opponent_unit_index)
                self.__opponent_unit_id = opponent_field_unit.get_card_number()
                return True

        return False

    def field_inside_field_unit(self, selected_object, opponent_unit_index):
        placed_card_id = selected_object.get_card_number()
        card_type = self.card_info.getCardTypeForCardNumber(placed_card_id)

        placed_card_index = self.your_hand_repository.find_index_by_selected_object(selected_object)

        # if card_type == CardType.UNIT.value:
        #     self.field_fixed_unit_card(placed_card_id, opponent_unit_index, placed_card_index)



