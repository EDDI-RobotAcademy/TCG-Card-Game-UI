class MyCardMainFrameScene:
    def __init__(self):
        self.shapes = []
        self.translations = []

    def add_shape(self, shape, translation=(0, 0)):
        shape.local_translate(translation)
        self.shapes.append(shape)
        self.translations.append(translation)