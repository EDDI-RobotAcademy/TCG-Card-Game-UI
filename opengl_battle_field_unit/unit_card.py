from card_info_from_csv.repository.card_info_from_csv_repository_impl import CardInfoFromCsvRepositoryImpl
from common.attack_type import AttackType

from image_shape.circle_image import CircleImage
from image_shape.circle_kinds import CircleKinds
from image_shape.circle_number_image import CircleNumberImage
from image_shape.non_background_image import NonBackgroundImage
from image_shape.non_background_number_image import NonBackgroundNumberImage

from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage


class UnitCard:
    __imagePath = None
    __pre_drawed_image_instance = PreDrawedImage.getInstance()
    __card_info_from_csv_repository = CardInfoFromCsvRepositoryImpl.getInstance()

    def __init__(self, local_translation=(0, 0)):
        self.shapes = []
        self.local_translation = local_translation

    def change_local_translation(self, _translation):
        self.local_translation = _translation

    def get_shapes(self):
        return self.shapes

    def add_shape(self, shape):
        shape.local_translate(self.local_translation)
        self.shapes.append(shape)


    def create_non_background_unit_energy(self, image_data, energy_number, center, radius):
        start_x = center[0] - radius * 1.5
        end_x = center[0] + radius * 1.5
        start_y = center[1] - radius * 1.3438 * 1.5
        end_y = center[1] + radius * 1.3438 * 1.5

        vertices = [
            (start_x, start_y),
            (end_x, start_y),
            (end_x, end_y),
            (start_x, end_y),
        ]
        unit_energy_image = NonBackgroundNumberImage(image_data=image_data,
                                                     vertices=vertices,
                                                     number=energy_number)

        unit_energy_image.set_circle_kinds(CircleKinds.ENERGY)
        unit_energy_image.set_visible(False)
        unit_energy_image.set_initial_vertices(vertices)
        self.add_shape(unit_energy_image)

    def create_non_background_unit_race(self, image_data, center, radius):
        start_x = center[0] - radius * 1.2
        end_x = center[0] + radius * 1.2
        start_y = center[1] - radius * 1.2
        end_y = center[1] + radius * 1.2

        # vertices = [
        #     (center[0] - radius, center[1] - radius),
        #     (center[0] + radius, center[1] - radius),
        #     (center[0] + radius, center[1] + radius),
        #     (center[0] - radius, center[1] + radius),
        # ]

        vertices = [
            (start_x, start_y),
            (end_x, start_y),
            (end_x, end_y),
            (start_x, end_y),
        ]

        unit_race_image = NonBackgroundImage(image_data=image_data,
                                             vertices=vertices)
        unit_race_image.set_initial_vertices(vertices)
        self.add_shape(unit_race_image)

    def create_non_background_unit_attack(self, image_data, attack_number, center, radius):
        start_x = center[0] - 5 - radius * 2.0
        end_x = center[0] - 5 + radius * 2.0
        start_y = center[1] - 7 - radius * 1.651 * 2.0
        end_y = center[1] - 7 + radius * 1.651 * 2.0

        # x: 376, y: 447
        # x: 371, y: 440

        vertices = [
            (start_x, start_y),
            (end_x, start_y),
            (end_x, end_y),
            (start_x, end_y),
        ]

        unit_attack_image = NonBackgroundNumberImage(image_data=image_data,
                                                     vertices=vertices,
                                                     number=attack_number)
        unit_attack_image.set_initial_vertices(vertices)
        unit_attack_image.set_circle_kinds(CircleKinds.ATTACK)
        self.add_shape(unit_attack_image)

    def create_non_background_unit_attack_wizard(self, image_data, attack_number, center, radius):
        start_x = center[0] - 5 - radius * 2.0 + 9
        end_x = center[0] - 5 + radius * 2.0 + 9
        start_y = center[1] - 7 - radius * 1.9353 * 2.0 - 32
        end_y = center[1] - 7 + radius * 1.9353 * 2.0 - 32

        # x: 376, y: 447
        # x: 371, y: 440

        vertices = [
            (start_x, start_y),
            (end_x, start_y),
            (end_x, end_y),
            (start_x, end_y),
        ]

        unit_attack_image = NonBackgroundNumberImage(image_data=image_data,
                                                     vertices=vertices,
                                                     number=attack_number)
        unit_attack_image.set_initial_vertices(vertices)
        unit_attack_image.set_circle_kinds(CircleKinds.ATTACK)
        self.add_shape(unit_attack_image)

    def create_non_background_unit_hp(self, image_data, hp_number, center, radius):
        # start_x = center[0] - 5 - radius * 1.8
        # end_x = center[0] - 5 + radius * 1.8
        # start_y = center[1] - 12 - radius * 1.2913 * 1.8
        # end_y = center[1] - 12 + radius * 1.2913 * 1.8

        start_x = center[0] - 5 - radius * 1.0
        end_x = center[0] - 5 + radius * 1.0
        start_y = center[1] - 12 - radius * 1.618 * 1.0
        end_y = center[1] - 12 + radius * 1.618 * 1.0

        # x: 267, y: 662
        # x: 272, y: 674

        vertices = [
            (start_x, start_y),
            (end_x, start_y),
            (end_x, end_y),
            (start_x, end_y),
        ]

        unit_hp_image = NonBackgroundNumberImage(image_data=image_data,
                                                 vertices=vertices,
                                                 number=hp_number)
        unit_hp_image.set_initial_vertices(vertices)
        unit_hp_image.set_circle_kinds(CircleKinds.HP)
        self.add_shape(unit_hp_image)

    def init_shapes(self, circle_radius, card_number, rectangle_height, rectangle_width):

        self.create_non_background_unit_energy(
            image_data=self.__pre_drawed_image_instance.get_pre_draw_unit_energy(0),
            energy_number=0,
            center=(0, 0),
            radius=circle_radius
        )

        race_number = self.__card_info_from_csv_repository.getCardRaceForCardNumber(card_number)

        self.create_non_background_unit_race(
            image_data=self.__pre_drawed_image_instance.get_pre_draw_unit_race(race_number),
            center=(rectangle_width, 0),
            radius=circle_radius)
        print(f"card_job : {type(self.__card_info_from_csv_repository.getCardJobForCardNumber(card_number))}")

        if int(self.__card_info_from_csv_repository.getCardJobForCardNumber(card_number)) is AttackType.sword_attack.value:
            self.create_non_background_unit_attack(
                image_data=self.__pre_drawed_image_instance.get_pre_draw_unit_attack(card_number),
                attack_number=self.__card_info_from_csv_repository.getCardAttackForCardNumber(card_number),
                center=(rectangle_width, rectangle_height),
                radius=circle_radius)
        else:
            self.create_non_background_unit_attack_wizard(
                image_data=self.__pre_drawed_image_instance.get_pre_draw_wizard_card_attack_power(card_number),
                attack_number=self.__card_info_from_csv_repository.getCardAttackForCardNumber(card_number),
                center=(rectangle_width, rectangle_height),
                radius=circle_radius)

        unit_hp_number = self.__card_info_from_csv_repository.getCardHpForCardNumber(card_number)

        self.create_non_background_unit_hp(
            image_data=self.__pre_drawed_image_instance.get_pre_draw_unit_hp(unit_hp_number),
            hp_number=unit_hp_number,
            center=(0, rectangle_height),
            radius=circle_radius)

