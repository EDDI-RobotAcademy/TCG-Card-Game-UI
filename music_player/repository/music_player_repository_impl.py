import os
import time

import pygame.mixer
from colorama import Fore, Style
from pygame import mixer
from music_player.repository.music_player_repository import MusicPlayerRepository


class MusicPlayerRepositoryImpl(MusicPlayerRepository):
    __instance = None
    __uiIpcChannel = None
    __backgroundMusicFileDict = {}

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def loadBackgroundMusic(self, frame_name: str):
        print(f"MusicPlayerRepositoryImpl : load_background_music - {frame_name}")
        pygame.mixer.init()

        current_location = os.getcwd()
        background_music_path = os.path.join(current_location, 'local_storage', 'background_music', f'{frame_name}.mp3')
        background_music = pygame.mixer.Sound(background_music_path)
        self.__backgroundMusicFileDict[frame_name] = background_music
        print(self.__backgroundMusicFileDict)

    def playBackgroundMusic(self):
        while True:
            try:
                print("MusicPlayerRepositoryImpl : playBackgroundMusic")
                frame_name = self.__uiIpcChannel.get()
                if frame_name is not None:
                    for frame in self.__backgroundMusicFileDict.keys():
                        if frame == frame_name:
                            loaded_sound = self.get_background_music(frame_name)
                            loaded_sound.play(-1)
            finally:
                time.sleep(0.1)

    def get_background_music(self, frame_name: str):
        print("MusicPlayerRepositoryImpl : get_background_music - " + frame_name)
        return self.__backgroundMusicFileDict[frame_name]

    # def changeBackgroundMusic(self):
    #     self.__currentFrameName.pop(0)
    #     mixer.music.stop()
    #     mixer.quit()
    #
    # def getBackgroundMusicFilePath(self, frameName: str):
    #     if self.__backgroundMusicFilePathDict[frameName]:
    #         return self.__backgroundMusicFilePathDict[frameName]
    #     else:
    #         print(f"{Fore.RED}There is no background music for this frame{Style.RESET_ALL}")
    #
    # def detectFrameChange(self):
    #     while True:
    #         try:
    #             frameName = self.__uiIpcChannel.get()
    #             print(f"frame change detected: {frameName}")
    #             print(f"current frame name is: {self.__currentFrameName}")
    #             if not self.__currentFrameName:
    #                 self.__currentFrameName.append(frameName)
    #                 self.playBackgroundMusic()
    #             elif frameName != self.__currentFrameName[0]:
    #                 self.__currentFrameName.append(frameName)
    #                 self.changeBackgroundMusic()
    #                 self.playBackgroundMusic()
    #             else:
    #                 pass
    #         finally:
    #             time.sleep(0.5)

    def saveUiIpcChannel(self, uiIpcChannel):
        print('music channel saved')
        self.__uiIpcChannel = uiIpcChannel
