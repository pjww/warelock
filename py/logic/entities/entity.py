from drawing.layer import Layer


class Entity(object):
    def __init__(self):
        # nie powinienem okreslac w ten sposob pozycji jednostki (Layer ma byc do rysowania),
        # ale nie chce juz wiekszego rozrostu kodu:
        self._layer = Layer(w=1, h=1)
