import numpy as np
from PIL import Image


class ImageDataLoader:
    @staticmethod
    def load_image_data(path):
        image = Image.open(path)
        resized_image = image.resize((300, 300))

        rgba_image = resized_image.convert("RGBA")
        img_data = np.array(rgba_image)

        return img_data
