import math
import random

from OpenGL.GL import *


class LightningGenerator:
    class LightningSegment:
        def __init__(self, start, end, brightness=1.0):
            self.start = start
            self.end = end
            self.brightness = brightness

    def __init__(self):
        pass

    @staticmethod
    def average(point1, point2):
        return ((point1[0] + point2[0]) / 2, (point1[1] + point2[1]) / 2)

    @staticmethod
    def normalize(vector):
        length = (vector[0]**2 + vector[1]**2)**0.5
        return (vector[0] / length, vector[1] / length)

    @staticmethod
    def perpendicular(vector):
        return (-vector[1], vector[0])

    @staticmethod
    def rotate(vector, angle):
        x = vector[0] * math.cos(angle) - vector[1] * math.sin(angle)
        y = vector[0] * math.sin(angle) + vector[1] * math.cos(angle)
        return (x, y)

    @staticmethod
    def random_float(min_val, max_val):
        return random.uniform(min_val, max_val)

    def generate_lightning(self, start_point, end_point, maximum_offset, num_generations, branch_probability, length_scale):
        segment_list = [self.LightningSegment(start_point, end_point)]
        offset_amount = maximum_offset

        for generation in range(num_generations):
            for segment in segment_list[:]:
                segment_list.remove(segment)

                mid_point = self.average(segment.start, segment.end)
                direction = self.normalize((segment.end[0] - segment.start[0], segment.end[1] - segment.start[1]))
                normal = self.perpendicular(direction)

                mid_point = (mid_point[0] + normal[0] * self.random_float(-offset_amount, offset_amount),
                             mid_point[1] + normal[1] * self.random_float(-offset_amount, offset_amount))

                segment_list.append(self.LightningSegment(segment.start, mid_point, segment.brightness))
                segment_list.append(self.LightningSegment(mid_point, segment.end, segment.brightness))

                if generation % 2 == 0 and random.random() < branch_probability:
                    branch_direction = self.rotate(direction, self.random_float(-math.pi / 2, math.pi / 2))
                    split_end = (mid_point[0] + branch_direction[0] * length_scale,
                                 mid_point[1] + branch_direction[1] * length_scale)

                    segment_list.append(self.LightningSegment(mid_point, split_end, segment.brightness * 0.5))

            offset_amount /= 2.0

        return segment_list

    def draw_lightning_segment(self, segment):
        glLineWidth(3.0)
        neon_color = (0.5, 0.5, 0.5, 1.0)

        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glColor4fv(neon_color)

        glBegin(GL_LINE_STRIP)
        glVertex2f(segment.start[0], segment.start[1])
        glVertex2f(segment.end[0], segment.end[1])
        glEnd()

        glDisable(GL_BLEND)
