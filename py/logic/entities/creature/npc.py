from random import random

from logic.entities.creature.character import Character
from logic.misc import WORLD_HEIGHT
from logic.misc import WORLD_WIDTH


class NPC(Character):

    def __init__(self):
        super(NPC, self).__init__()

        self._target_pos = None

    def update(self):
        if not (random() * 100 < 50):
            return

        # sprawdzanie granic zostanie przeniesione do bardziej odpowiedniej klasy (na razie dla prostoty)
        self._target_pos = (self._layer.x + int(random()*3)-1, self._layer.y + int(random()*3)-1)

        if (0 <= self._target_pos[0] < WORLD_WIDTH) and (0 <= self._target_pos[1] < WORLD_HEIGHT):
            self._layer.x = self._target_pos[0]
            self._layer.y = self._target_pos[1]
