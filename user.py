from player import Player


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
