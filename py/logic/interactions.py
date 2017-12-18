# -*- coding: utf8 -*-
from tools.multiple_dispatcher.combined_method import CombinedMethod
from logic.entities.creature.npc import NPC
from logic.entities.creature.playable import Playable
from logic.entities.creature.creature import Creature
from tools.multiple_dispatcher.shorthands import OC


@CombinedMethod(Playable, NPC)
def interact(player, npc):

    if hasattr(npc, 'words'):
        lines = npc.words.splitlines()
        print u'\'' + unicode(lines[npc.cnt % len(lines)]) + u'\''
        npc.cnt += 1

    if npc.is_hostile:
        player.hp -= 10
        npc.hp -= player.spell_power
        print unicode(npc.alt_title) + u' rani Cię, odbierając 10HP'
        print u'Ranisz nieprzyjaciela, odbierając %dHP' % player.spell_power


@CombinedMethod(NPC, Playable)
def interact(npc, player):
    # zaliasowanie powyzszej funkcji
    OC(player, npc).interact()


@CombinedMethod(Creature, Creature)
def interact(cr1, cr2):
    print u'Spotykają się %s i %s' % (cr1.title, cr2.title)


# Podobnie mozna dodac przeszkody Obstacle, niebezpieczenstwa Harmful, a zwlaszcza - itemy: Collectable, itd...:
#
# @CombinedMethod(NPC, Collectable)
# def interact(npc, collectable):
#     if npc.should_i_take_it(collectable):
#       npc.add_to_equipment(collectable)
#
# @CombinedMethod(Harmful, Creature)
# def interact(harmful, creature):
#     # np gracza badz npc
#     harmful.damage(creature)
#
# # aczkolwiek ponizsza funkcja dzialalaby poprawnie dla nieco innego sposobu sprawdzania kolizji:
# @CombinedMethod(Obstacle, Creature)
# def interact(harmful, creature):
#     # np gracza badz npc
#     settatr(creature, 'offset', (0, 0))
#
