class ImageItem:
    def __init__(self, path, position, size, translation=(0, 0)):
        self.path = path
        self.position = position
        self.size = size
        self.translation = translation
        self.is_visible = True

    def set_visible(self, visible):
        self.is_visible = visible

    def get_visible(self):
        return self.is_visible

    def translate(self, translation):
        self.translation = translation
