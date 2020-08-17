from random import randint
from ai import AI


class Easy(AI):
    level = 'easy'

    def get_coords(self):
        return self.get_random_coords(self.board)

    @staticmethod
    def get_random_coords(board):
        return [randint(0, board.get_size() - 1), randint(0, board.get_size() - 1)]
