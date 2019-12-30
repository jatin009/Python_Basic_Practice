from StrategyImpl import *


def game_init():
    choice = input("""Welcome to the game of Hangman!
    - Play with hints (a)
    - Play without any hints (any key)
    """)

    st_obj = None
    if choice == 'a':
        st_obj = NoStrategy()
    else:
        st_obj = HintStrategy()
    return st_obj


game_context = Context(game_init())
game_context.run_game()
