import itertools


class CollisionProcessor(object):

    # generator: zwraca pare kolidujacych ze soba obiektow:
    @staticmethod
    def process(entities):
        for ent1, ent2 in itertools.combinations(entities, 2):
            if ent1._layer.x == ent2._layer.x and ent1._layer.y == ent2._layer.y:
                yield (ent1, ent2)
