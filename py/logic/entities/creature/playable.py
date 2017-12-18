# -*- coding: utf8 -*-
from character import *
from logic.misc import WORLD_HEIGHT
from logic.misc import WORLD_WIDTH


class PlayableMetaclass(type):

    def __str__(self):

        output = ''
        output += '[' + self.repr + '] ' + self.title + '\n'
        output += 'Sila zaklec: ' + (self.spell_power / 10)*'#' + '\n'
        output += 'Ilosc zaklec: ' + (self.spell_wisdom / 10)*'#' + '\n'
        output += 'Maks. HP: ' + (self.max_hp / 10)*'#' + '\n'

        return output

    def __unicode__(self):

        output = u''
        shrunk_title = u''.join(list(self.title)[0: 0 + 20])

        output += u'┌───┐ ' + u'┌' + (len(shrunk_title)+2) * u'─' + u'┐' + u'\n'
        output += u'| ' + self.repr + u' | | ' + shrunk_title + u' |' + u'\n'
        output += u'└───┘ └' + (len(shrunk_title)+2) * u'─' + u'┘' + u'\n'

        output += u'┌' + 34*u'─' + u'┐ ' + u'\n'

        n1 = (self.spell_power / 10)
        n2 = (self.spell_wisdom / 10)
        n3 = (self.max_hp / 10)
        p1 = 20 - n1
        p2 = 20 - n2
        p3 = 20 - n3

        output += u'| ' + u'Siła zaklęć ' + n1 * u'▒' + p1 * u' ' + u' | ' + u'\n'
        output += u'| ' + u'Ilość zak.  ' + n2 * u'▒' + p2 * u' ' + u' | ' + u'\n'
        output += u'| ' + u'Maks. HP    ' + n3 * u'▒' + p3 * u' ' + u' | ' + u'\n'

        output += u'└' + 34*u'─' + u'┘ ' + u'\n'

        return output


class Playable(Character):

    __metaclass__ = PlayableMetaclass

    # domyslnie:
    spell_power = 0
    spell_wisdom = 0

    def __init__(self):
        super(Playable, self).__init__()
        self.spell_power = self.__class__.spell_power
        self.spell_wisdom = self.__class__.spell_wisdom

    def update(self):
        # sprawdzanie granic zostanie przeniesione do bardziej odpowiedniej klasy (na razie dla prostoty)

        # troszkie hakiem przekazany offset, ale interfejs jednostek powinien byc ujednolicony
        # natomiast to mocno zrefaktoryzowane (przepraszam za nieporzadek)
        if not hasattr(self, 'offset'):
            return

        self._target_pos = (self.offset[0] + self._layer.x, self.offset[1] + self._layer.y)

        if (0 <= self._target_pos[0] < WORLD_WIDTH) and (0 <= self._target_pos[1] < WORLD_HEIGHT):
            self._layer.x = self._target_pos[0]
            self._layer.y = self._target_pos[1]
