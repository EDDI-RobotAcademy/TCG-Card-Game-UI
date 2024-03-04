import numpy as np
from PIL import Image


class ImageDataLoader:
    @staticmethod
    def load_background_image_data(path, width, height):
        try:
            image = Image.open(path)
            resized_image = image.resize((width, height))

            rgba_image = resized_image.convert("RGBA")
            img_data = np.array(rgba_image)

            resized_image.close()
            image.close()

            return img_data

        except Exception as e:
            print(f"Error loading image data: {e}")
            return None

    @staticmethod
    def load_card_frame_image_data(path):
        try:
            image = Image.open(path)
            resized_image = image.resize((570, 916))

            rgba_image = resized_image.convert("RGBA")
            img_data = np.array(rgba_image)

            resized_image.close()
            image.close()

            return img_data

        except Exception as e:
            print(f"Error loading image data: {e}")
            return None

    @staticmethod
    def load_rectangle_image_data(path):
        try:
            image = Image.open(path)
            resized_image = image.resize((300, 300))

            rgba_image = resized_image.convert("RGBA")
            img_data = np.array(rgba_image)

            resized_image.close()
            image.close()

            return img_data

        except Exception as e:
            print(f"Error loading image data: {e}")
            return None

    @staticmethod
    def load_surrender_screen_image_data(path):
        try:
            image = Image.open(path)
            resized_image = image.resize((1200, 600))

            rgba_image = resized_image.convert("RGBA")
            img_data = np.array(rgba_image)

            resized_image.close()
            image.close()

            return img_data

        except Exception as e:
            print(f"Error loading image data: {e}")
            return None

    @staticmethod
    def load_oval_image_data(image_path):
        try:
            image = Image.open(image_path)
            width, height = image.size
            image_data = image.tobytes("raw", "RGB", 0, 0)

            image.close()

            return width, height, image_data

        except Exception as e:
            print(f"Error loading image data: {e}")
            return None

    @staticmethod
    def load_circle_image_data(image_path):
        try:
            image = Image.open(image_path)
            width, height = image.size
            image_data = image.tobytes("raw", "RGB", 0, 0)

            image.close()

            return width, height, image_data

        except Exception as e:
            print(f"Error loading image data: {e}")
            return None
