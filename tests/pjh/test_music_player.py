import os
import unittest

import pygame


def get_user_keyboard_input():
    while True:
        try:
            userInput = os.read(0, 1024)
            if userInput.decode().strip() == "":
                print('아무것도 입력하지 않으셨습니다. 다시 입력하세요!')
            else:
                return str(userInput.decode().strip())

        except ValueError as e:
            print(f"입력한 문자열 오류: {e}")

        except EOFError:
            pass


def play_music_with_menu_name(path):
    pygame.mixer.music.load(path)
    pygame.mixer.music.play(-1)


def play_sample_sound_to_mix():
    current_location = os.getcwd()
    background_music_path = (
        os.path.join(current_location, '../../', 'local_storage', 'background_music', 'basic_attack4.mp3'))
    sound = pygame.mixer.Sound(background_music_path)
    sound.play(100)


class TestMusicPlayer(unittest.TestCase):
    def test_music_player_by_input(self):
        pygame.init()

        while True:
            user_input = get_user_keyboard_input()
            current_location = os.getcwd()
            background_music_path = os.path.join(current_location, '../../', 'local_storage', 'background_music',
                                                 f'{user_input}.mp3')
            play_music_with_menu_name(background_music_path)

    def test_mixing_music(self):
        pygame.init()

        while True:
            user_input = get_user_keyboard_input()
            current_location = os.getcwd()
            background_music_path = os.path.join(current_location, '../../', 'local_storage', 'background_music',
                                                 f'{user_input}.mp3')
            play_music_with_menu_name(background_music_path)
            play_sample_sound_to_mix()
