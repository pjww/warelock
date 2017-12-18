from random import random

from logic.entities.entity_class_factory import EntityClassFactory
from path import root_path
from logic.misc import WORLD_WIDTH
from logic.misc import WORLD_HEIGHT
from drawing.scene import Scene
from drawing.scene import Layer
from logic.collision_processor import CollisionProcessor
from logic.interactions import *


class Gamestate(object):

    def __init__(self, difficulty=None):

        difficulty = difficulty or 1
        assert isinstance(difficulty, int) and 0 < difficulty

        self.difficulty = difficulty
        self.friendly_npcs_classes = None
        self.hostile_npcs_classes = None
        self.friendly_npcs = []
        self.hostile_npcs = []
        self.playable = None

    def load_gamestate(self, filename):

        # atrapa (implementacja jest nieistotna dla projektu)
        # udajemy, ze .load_gamestate wywoluje jakies funkcje parsujace
        # jak w przypadku obiektow klas entity:

        path = 'data/gamestates/' + filename

        # np te listy moglyby pochodzic z tego pliku:

        # klasy NPC-ow

        self.load_friendly_npc_classes(['kind_executable.xml', 'moody_script.xml', 'schelduler_exe.xml'])
        self.load_hostile_npc_classes(['angry_binary.xml', 'moody_script.xml'])

        # obiekty (rozmieszczenie) NPC-ow

        self.friendly_npcs.append(self.friendly_npcs_classes[0]())
        self.friendly_npcs.append(self.friendly_npcs_classes[1]())
        self.friendly_npcs.append(self.friendly_npcs_classes[2]())

        self.hostile_npcs.append(self.hostile_npcs_classes[0]())
        self.hostile_npcs.append(self.hostile_npcs_classes[1]())
        self.hostile_npcs.append(self.hostile_npcs_classes[0]())

        for npc in self.friendly_npcs:
            npc._layer.x = int(random() * WORLD_WIDTH)
            npc._layer.y = int(random() * WORLD_HEIGHT)
            npc.is_hostile = False
            setattr(npc, 'list', self.friendly_npcs)

        for npc in self.hostile_npcs:
            npc._layer.x = int(random() * WORLD_WIDTH)
            npc._layer.y = int(random() * WORLD_HEIGHT)
            npc.is_hostile = True
            setattr(npc, 'list', self.hostile_npcs)


        # klasy przeszkod (scian)

        # obiekty (rozmieszczenie) przeszkod (scian)

    def load_friendly_npc_classes(self, filenames):

        dir = root_path + 'data/entities/creature/npcs/'
        self.friendly_npcs_classes = [EntityClassFactory.from_xml(dir + filename) for filename in filenames]

    def load_hostile_npc_classes(self, filenames):

        dir = root_path + 'data/entities/creature/npcs/'
        self.hostile_npcs_classes = [EntityClassFactory.from_xml(dir + filename) for filename in filenames]

    def apply_difficulty(self):

        # Todo: na NPC / wrogach
        for hostile_npc_class in self.hostile_npcs_classes:
            hostile_npc_class.max_hp = int(hostile_npc_class.max_hp * self.difficulty)

    def gen_all_npcs(self):

        return (npc for npc in self.friendly_npcs + self.hostile_npcs)

    def gen_all_characters(self):

        return (c for c in [self.playable] + self.friendly_npcs + self.hostile_npcs)

    def draw(self):

        scene = Scene(w=WORLD_WIDTH, h=WORLD_HEIGHT)

        for npc in self.gen_all_characters():
            scene.add_layer(npc._layer)

        grass = Layer(w=WORLD_WIDTH - 6, h=WORLD_HEIGHT - 6, x=3, y=3, fillchar=' ')
        fence1 = Layer(w=5, h=4, x=16, y=1, z=10, content='+---+|   ||   |+---+')
        fence2 = Layer(w=5, h=4, x=2, y=5, z=10, content='+---+|   ||   |+---+')

        new_layer = grass + fence1 + fence2
        scene.add_layer(new_layer)

        scene.draw()

    def update(self, offset):

        # troszke hak, przepraszam
        setattr(self.playable, 'offset', offset)

        for ch in self.gen_all_characters():
            if ch.hp <= 0 and hasattr(ch, 'list'):
                getattr(ch, 'list').remove(ch)
                continue

            ch.update()

        for pair in CollisionProcessor.process(self.gen_all_characters()):
            try:
                # print pair[0]
                # print pair[1]
                # print OC(pair[0], pair[1])
                # print 'dla porownania'
                # print OC(pair[0], NPC())
                OC(pair[0], pair[1]).interact()
                # print issubclass(pair[0].__class__, Playable)

            # ignoruj jesli brakuje dopasowan do multimetod
            except AttributeError:
                pass
