import numpy as np
from PIL import Image


class ImageDataLoader:
    @staticmethod
    def load_rectangle_image_data(path):
        image = Image.open(path)
        resized_image = image.resize((300, 300))

        rgba_image = resized_image.convert("RGBA")
        img_data = np.array(rgba_image)

        return img_data

    @staticmethod
    def load_oval_image_data(image_path):
        try:
            print(f"load_oval_image_data: {image_path}")
            image = Image.open(image_path)
            width, height = image.size
            image_data = image.tobytes("raw", "RGB", 0, 0)
            return width, height, image_data
        except Exception as e:
            print(f"Error loading image data: {e}")
            return None
