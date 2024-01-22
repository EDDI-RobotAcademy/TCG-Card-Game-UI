class BattleFieldUnitCardScene:
    def __init__(self):
        self.shapes = []
        self.images = []
        self.translations = []

    def add_shape(self, shape, translation=(0, 0)):
        self.shapes.append(shape)
        self.translations.append(translation)

    def add_image(self, image):
        self.images.append(image)
