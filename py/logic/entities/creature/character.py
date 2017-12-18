from creature import *


class Character(Creature):

    def __init__(self):
        super(Character, self).__init__()
        self.cnt = 0  # licznik dla dialogow
