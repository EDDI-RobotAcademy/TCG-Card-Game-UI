import multiprocessing
import unittest
import os

from music_player.controller.music_player_controller_impl import MusicPlayerControllerImpl


class TestMusicPlayer(unittest.TestCase):

    def testMusicPlayer(self):
        queue = multiprocessing.Queue()
        queue.put("main-menu")
        musicPlayer = MusicPlayerControllerImpl.getInstance()
        musicPlayer.loadAllMusicFiles()
        musicPlayer.requestToInjectUiIpcChannel(queue)
        musicPlayer.playBackgroundMusic()


if __name__ == '__main__':
    unittest.main()
