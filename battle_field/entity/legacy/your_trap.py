from image_shape.rectangle_image import RectangleImage
from pre_drawed_image_manager.pre_drawed_image import PreDrawedImage


class YourTrap:
    __pre_drawed_image_instance = PreDrawedImage.getInstance()

    def __init__(self, local_translation=(0, 0), scale=1):
        self.pre_drawed_trap = None
        self.shapes = []
        self.local_translation = local_translation
        self.scale = scale

    def get_trap_shapes(self):
        return self.shapes

    def change_local_translation(self, _translation):
        self.local_translation = _translation

    def add_shape(self, shape):
        shape.local_translate(self.local_translation)
        self.shapes.append(shape)

    def create_trap(self, image_data, vertices):
        trap_illustration = RectangleImage(image_data=image_data,
                                           vertices=vertices)
        self.add_shape(trap_illustration)

    def init_shapes(self):
        self.__pre_drawed_image_instance.pre_draw_your_trap()
        # -1040, 480
        self.create_trap(image_data=self.__pre_drawed_image_instance.get_pre_draw_your_trap(),
                         vertices=[(300, 680), (500, 680), (500, 880), (300, 880)])