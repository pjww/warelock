from ..entity import *


class Creature(Entity):

    # domyslnie:
    max_hp = 100
    repr = 'C'

    def __init__(self):
        super(Creature, self).__init__()
        self.hp = self.__class__.max_hp
        self.repr = self.__class__.repr
        self._layer.content = self.repr
        self._layer.z = 10
        self.is_hostile = False

    # okreslenie zachowania w grze:
    # interfejs: update() - klasy pochodne maja okreslic
    # swoje zachowanie, np:
    # - NPC - losowy ruch w danym kierunku badz pozostanie w miejscu
    # - Playable - ruch na podstawie wczytanego klawisza
    # domyslnie - jak tutaj: stoi w miejscu

    # (a wiec metoda bedzie zachowywala sie jak funkcja wirtualna
    # w jezyku c++, ale w wyniku duck typing'u)

    def update(self):
        pass
