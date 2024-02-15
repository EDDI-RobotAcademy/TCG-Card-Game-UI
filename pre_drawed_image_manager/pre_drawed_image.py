import os

from common.utility import get_project_root
from utility.image_data_loader import ImageDataLoader


class PreDrawedImage:
    __instance = None

    __project_root = get_project_root()
    __pre_drawed_tomb = None
    __pre_drawed_lost_zone = None
    __pre_drawed_trap = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def pre_draw_tomb(self):
        tomb_image_path = os.path.join(self.__project_root, "local_storage", "image", "battle_field", "tomb.jpeg")
        self.__pre_drawed_tomb = ImageDataLoader.load_image_data(tomb_image_path)

    def pre_draw_lost_zone(self):
        lost_zone_image_path = os.path.join(self.__project_root, "local_storage", "image", "battle_field", "lost_zone.png")
        self.__pre_drawed_lost_zone = ImageDataLoader.load_image_data(lost_zone_image_path)

    def pre_draw_trap(self):
        trap_image_path = os.path.join(self.__project_root, "local_storage", "image", "battle_field", "trap.jpeg")
        self.__pre_drawed_trap = ImageDataLoader.load_image_data(trap_image_path)

    def pre_draw_every_image(self):
        self.pre_draw_tomb()
        self.pre_draw_lost_zone()
        self.pre_draw_trap()

    def get_pre_draw_tomb(self):
        return self.__pre_drawed_tomb

    def get_pre_draw_lost_zone(self):
        return self.__pre_drawed_lost_zone

    def get_pre_draw_trap(self):
        return self.__pre_drawed_trap
