from ai import AI


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
