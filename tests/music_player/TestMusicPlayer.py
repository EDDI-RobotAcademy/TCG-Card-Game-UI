import multiprocessing
import unittest
import os

from music_player.controller.music_player_controller_impl import MusicPlayerControllerImpl


class TestMusicPlayer(unittest.TestCase):

    def testGetAllFileNameList(self):
        currentLocation = os.getcwd()
        directoryPath = os.path.join(currentLocation, '../../', 'local_storage', 'background_music')
        # directoryPath = os.path.join(currentLocation, '../../', 'local_storage')
        fileNameList = [
            f for f in os.listdir(directoryPath)
            if os.path.isfile(os.path.join(directoryPath, f))
        ]
        print(fileNameList)

    def testMusicPlayer(self):
        queue = multiprocessing.Queue()
        queue.put("main-menu")
        musicPlayer = MusicPlayerControllerImpl.getInstance()
        musicPlayer.loadAllMusicFiles()
        musicPlayer.requestToInjectUiIpcChannel(queue)
        musicPlayer.playBackgroundMusic()


if __name__ == '__main__':
    unittest.main()
