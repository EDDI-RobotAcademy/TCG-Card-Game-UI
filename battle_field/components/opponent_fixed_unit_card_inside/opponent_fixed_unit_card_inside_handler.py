from battle_field.infra.opponent_field_unit_repository import OpponentFieldUnitRepository
from battle_field.infra.opponent_tomb_repository import OpponentTombRepository
from battle_field.infra.legacy.circle_image_legacy_your_hand_repository import CircleImageLegacyYourHandRepository
from battle_field.infra.your_tomb_repository import YourTombRepository
from card_info_from_csv.repository.card_info_from_csv_repository_impl import CardInfoFromCsvRepositoryImpl
from common.card_grade import CardGrade
from common.card_race import CardRace
from common.card_type import CardType
from image_shape.circle_kinds import CircleKinds
from image_shape.circle_number_image import CircleNumberImage
from opengl_shape.circle import Circle
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage


class OpponentFixedUnitCardInsideHandler:
    __instance = None

    __required_energy = -1
    __required_energy_race = CardRace.DUMMY
    __opponent_field_area_action = None
    __opponent_unit_index = -1
    __opponent_unit_id = -1
    __action_set_card_index = -1
    __your_hand_card_id = -1

    __your_hand_repository = CircleImageLegacyYourHandRepository.getInstance()
    __your_tomb_repository = YourTombRepository.getInstance()
    __opponent_field_unit_repository = OpponentFieldUnitRepository.getInstance()
    __opponent_tomb_repository = OpponentTombRepository.getInstance()
    __card_info_repository = CardInfoFromCsvRepositoryImpl.getInstance()
    __pre_drawed_image_instance = PreDrawedImage.getInstance()

    __lightning_border_list = []

    __opponent_fixed_unit_card_inside_handler_table = {}

    def __new__(cls):

        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

            # cls.__instance.your_hand_repository = your_hand_repository
            # cls.__instance.opponent_field_unit_repository = opponent_field_unit_repository
            # cls.__instance.card_info = card_info

            # cls.__instance.__opponent_fixed_unit_card_inside_handler_table[8] = cls.__instance.death_sice_need_two_undead_energy
            cls.__instance.__opponent_fixed_unit_card_inside_handler_table[8] = cls.__instance.death_sice
            # cls.__instance.__opponent_fixed_unit_card_inside_handler_table[20] = cls.__instance.contract_of_doom
            cls.__instance.__opponent_fixed_unit_card_inside_handler_table[9] = cls.__instance.energy_burn
            # cls.__instance.__opponent_fixed_unit_card_inside_handler_table[35] = cls.__instance.do_nothing

        return cls.__instance

    @classmethod
    def getInstance(cls):

        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def get_required_energy(self):
        return self.__required_energy

    def decrease_required_energy(self):
        self.__required_energy -= 1

    def clear_required_energy(self):
        self.__required_energy = -1

    def get_required_energy_race(self):
        return self.__required_energy_race

    def clear_required_energy_race(self):
        self.__required_energy_race = CardRace.DUMMY

    def set_opponent_field_area_action(self, opponent_field_area_action):
        self.__opponent_field_area_action = opponent_field_area_action

    def get_opponent_field_area_action(self):
        return self.__opponent_field_area_action

    def clear_opponent_field_area_action(self):
        self.__opponent_field_area_action = None

    def get_opponent_unit_index(self):
        return self.__opponent_unit_index

    def clear_opponent_unit_index(self):
        self.__opponent_unit_index = -1

    def get_action_set_card_index(self):
        return self.__action_set_card_index

    def clear_action_set_card_index(self):
        self.__action_set_card_index = -1

    def get_lightning_border_list(self):
        return self.__lightning_border_list

    def clear_lightning_border_list(self):
        self.__lightning_border_list = []

    def get_opponent_unit_id(self):
        return self.__opponent_unit_id

    def clear_opponent_unit_id(self):
        self.__opponent_unit_id = -1

    def get_your_hand_card_id(self):
        return self.__your_hand_card_id

    def clear_your_hand_card_id(self):
        self.__your_hand_card_id = -1

    def handle_pickable_card_inside_unit(self, selected_object, x, y):
        print(f"handle_pickable_card_inside_unit: {selected_object}, {x}, {y}")
        card_type = self.__card_info_repository.getCardTypeForCardNumber(selected_object.get_card_number())
        print(f"card_type: {card_type}")

        if selected_object.get_card_number() == 35:
            return False

        if card_type not in [CardType.ITEM.value]:
            return

        opponent_field_unit_list = self.__opponent_field_unit_repository.get_current_field_unit_card_object_list()

        for opponent_unit_index, opponent_field_unit in enumerate(opponent_field_unit_list):
            if opponent_field_unit is None:
                continue

            if opponent_field_unit.get_fixed_card_base().is_point_inside((x, y)):
                self.handle_inside_field_unit(selected_object, opponent_unit_index)
                self.__opponent_unit_id = opponent_field_unit.get_card_number()
                print("handle_pickable_card_inside_unit -> True")
                return True

        print("handle_pickable_card_inside_unit -> False")
        return False

    def handle_inside_field_unit(self, selected_object, opponent_unit_index):
        placed_card_id = selected_object.get_card_number()
        card_type = self.__card_info_repository.getCardTypeForCardNumber(placed_card_id)

        # placed_card_index = self.__your_hand_repository.find_index_by_selected_object(selected_object)
        placed_card_index = self.__your_hand_repository.find_index_by_selected_object_with_page(selected_object)

        if card_type == CardType.ITEM.value:
            self.handle_item_card(placed_card_id, opponent_unit_index, placed_card_index)

    def handle_item_card(self, placed_card_id, unit_index, placed_card_index):
        print("아이템 카드를 사용합니다!")

        proper_handler = self.__opponent_fixed_unit_card_inside_handler_table[placed_card_id]
        proper_handler(placed_card_index, unit_index, placed_card_id)

        # self.your_hand_repository.remove_card_by_id(placed_card_id)
        # self.opponent_field_unit_repository.remove_current_field_unit_card(unit_index)
        # self.your_hand_repository.replace_hand_card_position()

    def energy_burn(self, placed_card_index, unit_index, placed_card_id):
        print("energy_burn")

        opponent_field_unit = self.__opponent_field_unit_repository.find_opponent_field_unit_by_index(unit_index)

        detach_count = 2
        total_attached_energy_count = self.__opponent_field_unit_repository.get_total_energy_at_index(unit_index)
        print(f"opponent_field_unit_attached_undead_energy_count: {total_attached_energy_count}")

        # attached_energy = self.__opponent_field_unit_repository.attached_energy_info.get(unit_index, [])

        if total_attached_energy_count == 0:
            detach_count = 0
        elif total_attached_energy_count == 1:
            detach_count = 1

        attached_energy_after_energy_burn = total_attached_energy_count - detach_count
        if attached_energy_after_energy_burn < 0:
            attached_energy_after_energy_burn = 0

        opponent_fixed_card_base = opponent_field_unit.get_fixed_card_base()
        opponent_fixed_card_attached_shape_list = opponent_fixed_card_base.get_attached_shapes()

        energy_circle_list = []
        energy_circle_index_list = []
        count = 0

        for opponent_fixed_card_attached_shape in opponent_fixed_card_attached_shape_list:
            if isinstance(opponent_fixed_card_attached_shape, CircleNumberImage):
                if opponent_fixed_card_attached_shape.get_circle_kinds() is CircleKinds.ENERGY:
                    opponent_fixed_card_attached_shape.set_image_data(
                        self.__pre_drawed_image_instance.get_pre_draw_number_image(
                            attached_energy_after_energy_burn))

            if isinstance(opponent_fixed_card_attached_shape, Circle):
                energy_circle_index_list.append(count)
                print(f"Energy burn opponent unit vertices: {opponent_fixed_card_attached_shape.get_vertices()}")
                energy_circle_list.append(opponent_fixed_card_attached_shape)

                del opponent_fixed_card_attached_shape

            count += 1

        energy_circle_index_list.reverse()
        for index in energy_circle_index_list:
            if 0 <= index < len(opponent_fixed_card_attached_shape_list):
                if detach_count == 0:
                    break

                del opponent_fixed_card_attached_shape_list[index]
                detach_count -= 1

        # energy_circle_list.reverse()
        # extract_energy_circle = energy_circle_list[:2]
        # print(f"energy_circle_list: {extract_energy_circle}")
        #
        # opponent_fixed_card_attached_shape_list = [shape for shape in opponent_fixed_card_attached_shape_list if shape not in extract_energy_circle]
        # print(f"opponent_fixed_card_attached_shape_list: {opponent_fixed_card_attached_shape_list}")

        # self.__your_hand_repository.remove_card_by_index(placed_card_index)
        self.__your_hand_repository.remove_card_by_index_with_page(placed_card_index)
        self.__your_tomb_repository.create_tomb_card(placed_card_id)
        # self.__your_hand_repository.replace_hand_card_position()
        self.__your_hand_repository.update_your_hand()

    def death_sice(self, placed_card_index, unit_index, placed_card_id):
        DEATH_SICE_FIXED_DAMAGE = 30

        # self.__your_hand_repository.remove_card_by_index(placed_card_index)
        self.__your_hand_repository.remove_card_by_index_with_page(placed_card_index)
        self.__your_tomb_repository.create_tomb_card(placed_card_id)

        opponent_unit = self.__opponent_field_unit_repository.find_opponent_field_unit_by_index(unit_index)
        opponent_unit_card_id = opponent_unit.get_card_number()

        is_opponent_unit_death = True
        opponent_unit_hp = 0

        opponent_fixed_card_base = None
        opponent_attached_shape_list = None

        if self.__card_info_repository.getCardGradeForCardNumber(opponent_unit_card_id) > CardGrade.LEGEND.value:
            # opponent_unit_hp = self.__card_info_repository.getCardHpForCardNumber(opponent_unit_card_id)
            opponent_fixed_card_base = opponent_unit.get_fixed_card_base()
            opponent_attached_shape_list = opponent_fixed_card_base.get_attached_shapes()

            for opponent_attached_shape in opponent_attached_shape_list:
                if isinstance(opponent_attached_shape, CircleNumberImage):
                    if opponent_attached_shape.get_circle_kinds() is CircleKinds.HP:
                        opponent_unit_hp = opponent_attached_shape.get_number()
                        opponent_unit_hp -= DEATH_SICE_FIXED_DAMAGE
                        opponent_attached_shape.set_number(opponent_unit_hp)

                        if opponent_unit_hp <= 0:
                            break

                        opponent_attached_shape.set_image_data(
                            self.__pre_drawed_image_instance.get_pre_draw_number_image(
                                opponent_unit_hp))

            print(f"opponent_unit_hp: {opponent_unit_hp}")
            if opponent_unit_hp > 0:
                is_opponent_unit_death = False
        else:
            self.__opponent_tomb_repository.create_opponent_tomb_card(opponent_unit_card_id)

        # self.__your_hand_repository.replace_hand_card_position()

        if is_opponent_unit_death:
            print(f"is it death ? {opponent_unit_hp}")
            self.__opponent_field_unit_repository.remove_current_field_unit_card(unit_index)
            self.__opponent_field_unit_repository.replace_opponent_field_unit_card_position()

        # else:
        #     opponent_fixed_card_base = opponent_unit.get_fixed_card_base()
        #     opponent_attached_shape_list = opponent_fixed_card_base.get_attached_shapes()
        #
        #     for opponent_attached_shape in opponent_attached_shape_list:
        #         if isinstance(opponent_attached_shape, CircleNumberImage):
        #             if opponent_attached_shape.get_circle_kinds() is CircleKinds.HP:
        #                 opponent_attached_shape.set_image_data(
        #                     self.__pre_drawed_image_instance.get_pre_draw_number_image(
        #                         opponent_unit_hp))

        self.__your_hand_repository.update_your_hand()

    # def death_sice_need_two_undead_energy(self, placed_card_index, unit_index, placed_card_id):
    #     print("death_sice operates")

        # # TODO: 실제로 여기서 조정하면 됨 (필요한 에너지 값)
        # self.__required_energy = 2
        # self.__required_energy_race = CardRace.UNDEAD
        #
        # # 뭔가 작업을 위해 대기가 필요한 상황 (에너지가 필요하다던지)
        # self.__opponent_field_area_action = OpponentFieldAreaAction.REQUIRE_ENERGY_TO_USAGE
        # self.__opponent_unit_index = unit_index
        # self.__action_set_card_index = placed_card_index
        # self.__your_hand_card_id = placed_card_id
        #
        # your_current_hand_card_list = self.__your_hand_repository.get_current_hand_card_list()
        #
        # for your_current_hand_card in your_current_hand_card_list:
        #     your_hand_card_id = your_current_hand_card.get_card_number()
        #     if your_hand_card_id == 93 or your_hand_card_id == 151:
        #         card_base = your_current_hand_card.get_pickable_card_base()
        #         self.__lightning_border_list.append(card_base)

    # def contract_of_doom(self, placed_card_index, placed_card_id):
    #     print(f"contract_of_doom() -> placed_card_index: {placed_card_index}, placed_card_id: {placed_card_id}")
    #
    #     self.__required_energy = 0
    #
    #     damage = 15
    #
    #     # TODO: 즉발이므로 대기 액션이 필요없음 (서버와의 통신을 위해 대기가 발생 할 수 있긴함) 그 때 가서 추가
    #     for index, opponent_field_unit_list in enumerate(self.__opponent_field_unit_repository.get_current_field_unit_card_object_list()):
    #         remove_from_field = False
    #
    #         fixed_card_base = opponent_field_unit_list.get_fixed_card_base()
    #         attached_shape_list = fixed_card_base.get_attached_shapes()
    #
    #         # TODO: 가만 보면 이 부분이 은근히 많이 사용되고 있음 (중복 많이 발생함)
    #         for attached_shape in attached_shape_list:
    #             if isinstance(attached_shape, CircleNumberImage):
    #                 if attached_shape.get_circle_kinds() is CircleKinds.HP:
    #
    #                     hp_number = attached_shape.get_number()
    #                     hp_number -= damage
    #
    #                     # TODO: n 턴간 불사 특성을 검사해야하므로 사실 이것도 summary 방식으로 빼는 것이 맞으나 우선은 진행한다.
    #                     # (지금 당장 불사가 존재하지 않음)
    #                     if hp_number <= 0:
    #                         remove_from_field = True
    #                         break
    #
    #                     attached_shape.set_image_data(
    #                         # TODO: 실제로 여기서 서버로부터 계산 받은 값을 적용해야함
    #                         self.__pre_drawed_image_instance.get_pre_draw_number_image(hp_number))
    #
    #         if remove_from_field:
    #             self.__opponent_field_unit_repository.remove_current_field_unit_card(index)




