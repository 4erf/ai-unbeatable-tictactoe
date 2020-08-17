from ai import AI
from easy import Easy


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
