class GameEndState:

    def __init__(self):
        self.is_game_end = False
        self.is_win = False

    def game_lose(self):
        self.is_game_end = True
        self.is_win = False

    def game_win(self):
        self.is_game_end = True
        self.is_win = True

    def get_is_game_end_state(self):
        return self.is_game_end

    def get_is_win_state(self):
        return self.is_win

    def reset_state(self):
        self.is_game_end = False
        self.is_win = False
