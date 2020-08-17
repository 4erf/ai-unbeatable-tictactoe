from board import Board
from easy import Easy
from medium import Medium
from hard import Hard
from user import User


class Game:
    def __init__(self, bs, player_a, player_b):
        self.board = Board(bs)
        self.active_player = self.create_player(player_a, 'X')
        self.waiting_player = self.create_player(player_b, 'O')
        self.game_finished = False

    def start(self):
        print(self.board)

        while not self.game_finished:
            self.run_game_round()
            self.swap_player()
            print(self.board)

        print(self.board.get_result())

    def run_game_round(self):
        self.active_player.make_move()
        self.game_finished = self.board.get_status()

    def swap_player(self):
        self.active_player, self.waiting_player = self.waiting_player, self.active_player

    def create_player(self, player_type, symbol):
        if player_type == 'user':
            return User(symbol, self.board)
        elif player_type == 'easy':
            return Easy(symbol, self.board)
        elif player_type == 'medium':
            return Medium(symbol, self.board)
        elif player_type == 'hard':
            return Hard(symbol, self.board)
