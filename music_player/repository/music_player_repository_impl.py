import os
import time

from pygame import mixer
from music_player.repository.music_player_repository import MusicPlayerRepository


class MusicPlayerRepositoryImpl(MusicPlayerRepository):
    __instance = None
    __uiIpcChannel = None
    __backgroundMusicFilePathDict = {}

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def getInstance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def loadBackgroundMp3(self, frameName: str):
        # 방식의 개선이 필요함
        currentLocation = os.getcwd()
        backgroundMusicPath = os.path.join(currentLocation, 'local_storage', 'background_music', f'{frameName}.mp3')
        self.__backgroundMusicFilePathDict[frameName] = backgroundMusicPath
        print(f'MusicPlayerRepositoryImpl : {frameName} background music loaded')
        print(self.__backgroundMusicFilePathDict)

    def playBackgroundMusic(self):
        backgroundMusicPath = self.getBackgroundMusicFilePath()
        mixer.init()
        mixer.music.load(backgroundMusicPath)
        mixer.music.play()

        while mixer.music.get_busy():
            print("Background Music is playing")
            time.sleep(5)
    def stopBackgroundMusic(self):

        mixer.music.stop()
        mixer.quit()


    def getBackgroundMusicFilePath(self):
        frameName = self.__uiIpcChannel.get()
        if self.__backgroundMusicFilePathDict[frameName]:
            return self.__backgroundMusicFilePathDict[frameName]
        else:
            print("Background Music is not playing")

    def saveUiIpcChannel(self, uiIpcChannel):
        print('music channel saved')
        self.__uiIpcChannel = uiIpcChannel
        print(self.__uiIpcChannel)
