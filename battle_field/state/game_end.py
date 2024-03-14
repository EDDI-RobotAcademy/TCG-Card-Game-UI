from common.battle_finish_position import BattleFinishPosition


class GameEndState:

    def __init__(self):
        self.is_game_end = False
        self.is_win = BattleFinishPosition.Dummy

    def game_lose(self):
        self.is_game_end = True
        self.is_win = BattleFinishPosition.Loser

    def game_win(self):
        self.is_game_end = True
        self.is_win = BattleFinishPosition.Winner

    def game_draw(self):
        self.is_game_end = True
        self.is_win = BattleFinishPosition.Draw

    def get_is_game_end_state(self):
        return self.is_game_end

    def get_is_win_state(self):
        return self.is_win

    def reset_state(self):
        self.is_game_end = False
        self.is_win = False
