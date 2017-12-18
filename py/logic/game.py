# -*- coding: utf8 -*-
import os

from logic.entities.entity_class_factory import EntityClassFactory
from logic.gamestate import Gamestate
from path import root_path


class Game(object):

    def __init__(self):

        self.playable_classes = None
        self.gamestate = None

        self._running = False
        self.chosen_class_i = 0

    def main_menu(self):

        option = 's'

        i = 0
        while True:

            print u'Wybierz klasę postaci'
            print unicode(self.playable_classes[i % len(self.playable_classes)])
            print u'[P] Poprzednia   [N] Następna   [K] Akceptuj   [Q] Wyjście'
            option = raw_input()
            print

            if option.lower() == 'n':
                i += 1

            if option.lower() == 'p':
                i -= 1

            if option.lower() == 'k' or option.lower() == 'q':
                break

        if option.lower() == 'q':
            self.quit()

        self.chosen_class_i = i % len(self.playable_classes)

    def quit(self):

        self._running = False

    def load_playable_classes(self):

        dir = root_path + 'data/entities/creature/playable/'
        self.playable_classes = [EntityClassFactory.from_xml(dir + filename) for filename in os.listdir(dir)]

    def main_loop(self):

        option = ''

        while self._running:

            self.gamestate.draw()
            print u'[W][S][A][D] Poruszanie się  [Q] Wyjście'
            print u'HP: %d/%d    Moc: %d    Wiedza: %d' % \
                (self.gamestate.playable.hp, self.gamestate.playable.max_hp,
                 self.gamestate.playable.spell_power, self.gamestate.playable.spell_wisdom)

            option = raw_input()
            print

            offset = None

            if option.lower() == 'w':
                offset = (0, -1)
                pass

            elif option.lower() == 's':
                offset = (0, 1)
                pass

            elif option.lower() == 'a':
                offset = (-1, 0)
                pass

            elif option.lower() == 'd':
                offset = (1, 0)
                pass

            elif option.lower() == 'q':
                self.quit()

            if offset:
                self.gamestate.update(offset)

            if self.gamestate.playable.hp <= 0:
                print 'Niestety, umierasz...'
                raw_input()
                self.quit()

    def run(self):
        # laduje potrzebne do zaprezentowania w menu klasy postaci
        self.load_playable_classes()

        # opowiada historie i pozwala wybrac klase postaci
        self._running = True
        self.main_menu()

        # generuje mape
        self.gamestate = Gamestate()
        self.gamestate.load_gamestate('map01.xml')

        # tworzy obiekt postaci gracza
        self.gamestate.playable = self.playable_classes[self.chosen_class_i]()
        self.gamestate.playable._layer.x = 1
        self.gamestate.playable._layer.y = 1

        # rozpoczyna glowna petle

        self.main_loop()

