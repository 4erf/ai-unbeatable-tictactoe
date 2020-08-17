class Board:
    def __init__(self, bs, board=None):
        if board is None:
            self.board = [[' ' for _ in range(bs)] for _ in range(bs)]
        else:
            self.board = board
        # self.board = [['O', 'X', 'X'], [' ', 'X', 'O'], ['O', ' ', ' ']]  # testing only
        self.result = None

    def __str__(self):
        string = '---------\n'
        for x in self.board:
            string += '| ' + ' '.join(x) + ' |\n'
        string += '---------'
        return string

    def __copy__(self):
        board = Board(self.get_size(), [[cell for cell in row] for row in self.board])
        return board

    def has_empty_cells(self):
        return any([cell == ' ' for row in self.board for cell in row])

    def has_full_row(self):
        lines = self.get_lines(self.board)
        return next(
            (line[0] for line in lines if line[1:] == line[:-1] and line[0] != ' '),
            None
        )

    def make_move(self, symbol, x, y, verbose=False):
        if self.result is None:
            if not self.validate_coords(x, y, verbose):
                return False
            self.board[x][y] = symbol
            return True
        print('Full table')
        return True

    def validate_coords(self, x, y, verbose):
        if not (0 <= x <= self.get_size() - 1) or not (0 <= y <= self.get_size() - 1):
            if verbose:
                print(f'Coordinates should be from 1 to {self.get_size() - 1}!')
            return False
        elif self.board[x][y] != ' ':
            if verbose:
                print('This cell is occupied! Choose another one!')
            return False
        return True

    def get_status(self):
        player = self.has_full_row()
        if player is not None:
            self.result = player + ' wins'
        elif self.has_empty_cells():
            return False
        else:
            self.result = 'Draw'
        return True

    def get_result(self):
        return self.result

    def get_size(self):
        return len(self.board)

    def convert_user_coords(self, x, y):
        return [self.get_size() - y, x - 1]

    def get_full_board(self):
        return [
            [
                [cell, [i, j]] for j, cell in enumerate(row)
            ]
            for i, row in enumerate(self.board)
        ]

    def get_possible_moves(self):
        board = self.get_full_board()
        return [cell[1] for row in board for cell in row if cell[0] == ' ']

    @staticmethod
    def get_lines(board):
        lines = [[cell for cell in row] for row in board]
        lines += zip(*board)  # columns
        lines += Board.get_diagonals(board)
        return lines

    @staticmethod
    def get_diagonals(board):
        return [
            [row[i] for i, row in enumerate(board)],
            [row[-i - 1] for i, row in enumerate(board)]
        ]
