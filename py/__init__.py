import os

# tylko, jesli skrypt zostal uruchomiony
if __name__ == '__main__':

    import os
    import sys
    from path import root_path

    from logic.game import Game

    game = Game()
    game.run()

