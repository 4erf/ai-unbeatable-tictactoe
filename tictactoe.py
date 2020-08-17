from game import Game

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
