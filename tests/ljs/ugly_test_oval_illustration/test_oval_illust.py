import os
import tkinter
import unittest
from math import cos, sin, pi
from PIL import Image, ImageDraw
import tkinter as tk
from OpenGL.GL import *
from OpenGL.GLU import *
from pyopengltk import OpenGLFrame

class OvalIllustrationApp(OpenGLFrame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        self.width = screen_width
        self.height = screen_height


    def initgl(self):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_TEXTURE_2D)
        glClearColor(0.8, 0.8, 0.8, 1.0)
        gluOrtho2D(0, self.width, 0, self.height)

        current_directory = os.getcwd()
        parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir, os.pardir, os.pardir))
        image_path = os.path.join(parent_directory, 'local_storage', 'card_images', '6.png')

        image = Image.open(image_path)
        print(f"imageWidth: {image.width}, imageHeight: {image.height}")
        oval_image = self.crop_center(image, 320, 128)

        self.texture_id = self.load_texture(oval_image)

    def crop_center(self, original_image, width, height):
        # 이미지의 중앙 부분 좌표 계산
        # todo : 타원안에 표시하고 싶은 곳의 좌표를 입력하면 됩니다.
        #  현재는 이미지의 크기와 위치가 제각각이라 임의로 값을 더했지만,
        #  실제로는 이미지의 크기와 위치를 통일시켜 하나의 코드로 동작하게 만들어야합니다.
        left = (original_image.width - width) // 2
        top = (original_image.height - height) // 2 + 45
        right = left + width
        bottom = top + height

        # 중앙 부분 추출
        cropped_image = original_image.crop((left, top, right, bottom))
        # cropped_image = cropped_image.resize((width, height))

        return cropped_image

    def crop_ellipse(self, original_image):
        # 타원 모양으로 자르기 위한 영역 계산
        ellipse_bbox = (0, 0, original_image.width, original_image.height)
        mask = Image.new("L", original_image.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse(ellipse_bbox, fill=255)

        # 타원 모양으로 자르기
        oval_image = original_image.copy()
        oval_image.putalpha(mask)
        oval_image = oval_image.crop(ellipse_bbox)

        return oval_image

    def redraw(self):
        self.tkMakeCurrent()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glBegin(GL_TRIANGLE_FAN)
        glColor3f(1.0, 1.0, 1.0)

        radius_x = 320
        radius_y = 128.0

        for i in range(361):
            angle = i * pi / 180.0
            x = self.width / 2 + radius_x * cos(angle)
            y = self.height / 2 + radius_y * sin(angle)
            glTexCoord2f(0.5 + 0.5 * cos(angle), 0.5 + 0.5 * sin(angle))
            glVertex2f(x, y)

        glEnd()

        self.tkSwapBuffers()

    def load_texture(self, image):
        image_data = image.tobytes("raw", "RGB", 0, -1)

        texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, image_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        return texture_id

class TestPickingCard(unittest.TestCase):
    def test_animation_frame(self):
        root = tkinter.Tk()
        root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}-0-0")
        root.deiconify()

        oval_app = OvalIllustrationApp(root)
        oval_app.pack(fill=tk.BOTH, expand=1)

        root.update_idletasks()

        root.mainloop()

if __name__ == '__main__':
    unittest.main()