from layer import *


class Scene(object):

    def __init__(self, w=None, h=None):
        self._w = 0
        self._h = 0

        self._layers = []
        self.w = w or 1
        self.h = h or 1

    def add_layer(self, layer):
        assert isinstance(layer, Layer)
        self._layers.append(layer)

    @property
    def w(self):
        return self._w

    @w.setter
    def w(self, w):
        self._w = abs(w)

    @property
    def h(self):
        return self._h

    @h.setter
    def h(self, h):
        self._h = abs(h)

    def draw(self):

        # rysuj sceny w takiej kolejnosci,
        # by warstwy o wyzszym z zaslanialy warstawy o nizszym z
        # (sortowanie jest stabilne, wiec warstwy o takich samych z
        # -- np dla kreatur z = 1 -- beda wyswietlane w takiej kolejnosci,
        # jak oryginalnie wystepowaly w liscie):

        sorted_layers = sorted(self._layers, key=(lambda(layer): layer.z))

        # dodaj warstwe 'tlo':

        bg_layer = Layer(w=self.w, h=self.h, x=0, y=0, z=-1000, fillchar='.')

        # polacz warswy w jedna:

        merged_layers = [bg_layer] + sorted_layers
        merged_layers = reduce((lambda l1, l2: l1 + l2), merged_layers)

        merged_layers.draw()

        # usprawnienia: nalezaloby rysowac tylko skadrowany prostokat [0,0 ; w,h)
