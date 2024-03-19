import os
import time

import pygame.mixer

from music_player.repository.music_player_repository import MusicPlayerRepository


class MusicPlayerRepositoryImpl(MusicPlayerRepository):
    __instance = None
    __uiIpcChannel = None
    __backgroundMusicFilePathDict = {}
    __soundPathDict = {}

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

            # pygame.mixer.init()

        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def saveUiIpcChannel(self, uiIpcChannel):
        print('music channel saved')
        self.__uiIpcChannel = uiIpcChannel

    def load_background_music_path_with_frame_name(self, frame_name: str):
        print(f"MusicPlayerRepositoryImpl : load_background_music_path_with_frame_name - {frame_name}")
        current_location = os.getcwd()
        background_music_path = os.path.join(current_location, 'local_storage', 'background_music', f'{frame_name}.mp3')
        self.__backgroundMusicFilePathDict[frame_name] = background_music_path
        print(self.__backgroundMusicFilePathDict)

    def load_sound_effect_path_with_event_name(self, event_name: str):
        print(f"MusicPlayerRepositoryImpl : load_sound_effect_path_with_event_name - {event_name}")
        current_location = os.getcwd()
        sound_effect_file_path = os.path.join(current_location, 'local_storage', 'sound_effect', f'{event_name}.mp3')
        self.__soundPathDict[event_name] = sound_effect_file_path
        print(self.__soundPathDict)

    def play_background_music(self):
        while True:
            try:
                frame_name = self.__uiIpcChannel.get()
                if frame_name:
                    for frame in self.__backgroundMusicFilePathDict.keys():
                        if frame == frame_name:
                            path = self.__get_background_music_path(frame_name)
                            pygame.mixer.init()
                            self.play_music(path)
                            if pygame.mixer.music.get_busy():
                                print("Background music - " + frame_name)
            finally:
                time.sleep(0.1)

    def play_music(self, path):
        pygame.mixer.music.load(path)
        pygame.mixer.music.play(-1)

    def __get_background_music_path(self, frame_name: str):
        return self.__backgroundMusicFilePathDict[frame_name]

    def play_sound_effect_with_event_name(self, event_name: str):
        print("MusicPlayerRepositoryImpl : play_sound_effect_with_event_name - " + event_name)
        pygame.mixer.init()
        sound = pygame.mixer.Sound(self.__soundPathDict[event_name])
        sound.play()

        time.sleep(0.1)

    def play_sound_effect_with_event_name_for_wav(self, event_name: str):
        print("MusicPlayerRepositoryImpl : play_sound_effect_with_event_name_for_wav - " + event_name)
        pygame.mixer.init()
        current_location = os.getcwd()
        sound_effect_file_path = os.path.join(current_location, 'local_storage', 'sound_effect', f'{event_name}.wav')
        sound = pygame.mixer.Sound(sound_effect_file_path)
        sound.play()

        time.sleep(0.1)
