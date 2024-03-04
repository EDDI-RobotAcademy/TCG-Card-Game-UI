from card_info_from_csv.repository.card_info_from_csv_repository_impl import CardInfoFromCsvRepositoryImpl

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
        # 가로 대비 세로 => 1.343
        # 양측으로 벌리니까 => 1.1715
        vertices = [
            (center[0] - radius, center[1] + radius * 1.1715),
            (center[0] + radius, center[1] + radius * 1.1715),
            (center[0] + radius, center[1] - radius * 1.1715),
            (center[0] - radius, center[1] - radius * 1.1715),
        ]
        image_data = self.__pre_drawed_image_instance.get_pre_draw_unit_energy(energy_number)
        unit_energy_image = NonBackgroundNumberImage(image_data=image_data,
                                                     vertices=vertices,
                                                     number=energy_number)

        unit_energy_image.set_circle_kinds(CircleKinds.ENERGY)
        unit_energy_image.set_visible(False)
        self.add_shape(unit_energy_image)

    def create_unit_race_illustration_circle(self, image_data, center, radius):
        # print(f"create_unit_race_illustration_circle -> center: {center}")
        unit_race_circle = CircleImage(image_data=image_data,
                                       center=center,
                                       radius=radius)
        self.add_shape(unit_race_circle)

    def create_unit_attack_circle(self, image_data, attack_number, center, radius):
        unit_attack_circle = CircleNumberImage(image_data=image_data,
                                               center=center,
                                               radius=radius,
                                               number=attack_number)
        unit_attack_circle.set_circle_kinds(CircleKinds.ATTACK)
        self.add_shape(unit_attack_circle)

    def create_unit_hp_circle(self, image_data, hp_number, center, radius):
        unit_hp_circle = CircleNumberImage(image_data=image_data,
                                           center=center,
                                           radius=radius,
                                           number=hp_number)
        unit_hp_circle.set_circle_kinds(CircleKinds.HP)
        self.add_shape(unit_hp_circle)

    def init_shapes(self, circle_radius, card_number, rectangle_height, rectangle_width):

        self.create_non_background_unit_energy(
            image_data=self.__pre_drawed_image_instance.get_pre_draw_unit_energy(0),
            energy_number=0,
            center=(0, 0),
            radius=circle_radius
        )

        self.create_unit_race_illustration_circle(
            image_data=self.__pre_drawed_image_instance.get_pre_draw_card_race_with_card_number(card_number),
            center=(rectangle_width, 0),
            radius=circle_radius)

        self.create_unit_attack_circle(
            image_data=self.__pre_drawed_image_instance.get_pre_draw_card_attack_with_card_number(card_number),
            attack_number=self.__card_info_from_csv_repository.getCardAttackForCardNumber(card_number),
            center=(rectangle_width, rectangle_height),
            radius=circle_radius)

        self.create_unit_hp_circle(
            image_data=self.__pre_drawed_image_instance.get_pre_draw_card_hp_with_card_number(card_number),
            hp_number=self.__card_info_from_csv_repository.getCardHpForCardNumber(card_number),
            center=(0, rectangle_height),
            radius=circle_radius)

