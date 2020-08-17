from random import randint


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


class Player:
    def __init__(self, symbol, board):
        self.symbol = symbol
        self.board = board


class User(Player):
    def make_move(self):
        valid_coords = False
        while not valid_coords:
            coords = self.get_coords()
            valid_coords = self.board.make_move(self.symbol, *coords, verbose=True)

    def get_coords(self):
        return self.board.convert_user_coords(*User.obtain_valid_params())

    @staticmethod
    def obtain_valid_params():
        while True:
            params = input('Enter the coordinates: ')
            try:
                return [int(x) for x in params.split()]
            except ValueError:
                print('You should enter numbers!')


class AI(Player):
    level = ''

    def make_move(self):
        print(f'Making move level "{self.level}"')
        valid_coords = False
        while not valid_coords:
            coords = self.get_coords()
            valid_coords = self.board.make_move(self.symbol, *coords)

    def get_coords(self):
        return [0, 0]


class Easy(AI):
    level = 'easy'

    def get_coords(self):
        return self.get_random_coords(self.board)

    @staticmethod
    def get_random_coords(board):
        return [randint(0, board.get_size() - 1), randint(0, board.get_size() - 1)]


class Medium(AI):
    level = 'medium'

    def get_coords(self):
        lines = self.board.get_lines(self.board.get_full_board())
        player = self.coords_to_full_line(lines, self.symbol, True)
        opponent = self.coords_to_full_line(lines, self.symbol, False)
        if player is not None:
            return player
        elif opponent is not None:
            return opponent
        else:
            return Easy.get_random_coords(self.board)

    @staticmethod
    def coords_to_full_line(lines, symbol, is_player):
        for line in lines:
            line = sorted(line, key=lambda cell: cell[0])
            simple = [cell[0] for cell in line]
            if (
                    (
                        (is_player and line[1][0] == symbol)
                        or (
                                not is_player and line[1][0] != symbol
                                and line[1][0] != ' '
                        )
                    )
                    and line[0][0] == ' ' and simple[2:] == simple[1:-1]
            ):
                return line[0][1]


class Hard(AI):
    level = 'hard'
    change_symbol = {'X': 'O', 'O': 'X'}

    def get_coords(self):
        return self.minimax(self.board.__copy__(), self.symbol, True)[1]

    @staticmethod
    def minimax(board, symbol, is_player):
        if board.has_full_row() is None:
            possible_moves = board.get_possible_moves()
            if not len(possible_moves):
                return [0, None]
            outcomes = []
            for move in possible_moves:
                new_board = board.__copy__()
                move_symbol = symbol if is_player else Hard.change_symbol[symbol]
                new_board.make_move(move_symbol, *move)
                outcomes.append([Hard.minimax(new_board, symbol, not is_player)[0], move])
            return max(outcomes) if is_player else min(outcomes)
        if board.has_full_row() == symbol:
            return [1, None]
        else:
            return [-1, None]


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


#########################################################################################


# Vars
board_size = 3
allowed_players = ['user', 'easy', 'medium', 'hard']
exit_game = False

# Menu loop
while not exit_game:
    action = input('Input command: ').split()
    action_name = action[0]
    action_params = action[1:]
    if (
        action_name == 'start' and len(action_params) == 2
        and all(x in allowed_players for x in action_params)
    ):
        game = Game(board_size, *action_params)
        game.start()
    elif action_name == 'exit':
        exit_game = True
    else:
        print('Bad parameters!')
