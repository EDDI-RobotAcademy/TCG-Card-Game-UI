import os

from common.utility import get_project_root
from utility.image_data_loader import ImageDataLoader


class PreDrawedImage:
    __instance = None

    __project_root = get_project_root()
    __pre_drawed_tomb = None

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

    def pre_draw_every_image(self):
        self.pre_draw_tomb()

    def get_pre_draw_tomb(self):
        print(f"pre drawed tomb: {self.__pre_drawed_tomb}")
        return self.__pre_drawed_tomb

