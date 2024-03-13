import pygame.mixer


class SoundEffect:
    def __init__(self):
        self.sound_effect = None

    def set_sound_effect(self, sound_effect_path):
        self.sound_effect = pygame.mixer.Sound(sound_effect_path)

    def play(self, loops, max_time, fade_ms):
        self.sound_effect.play(loops, max_time, fade_ms)
