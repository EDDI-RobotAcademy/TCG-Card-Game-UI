import unittest

from music_player.service.music_player_service_impl import MusicPlayerServiceImpl


class TestMusicPlayer(unittest.TestCase):
    def testMusicPlayer(self):
        music_player_service = MusicPlayerServiceImpl.getInstance()
        sample_frame_name = "main-menu"

        music_player = music_player_service.playMusicWithFrameName(sample_frame_name)


if __name__ == '__main__':
    unittest.main()
