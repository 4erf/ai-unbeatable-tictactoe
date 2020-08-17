from player import Player


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
