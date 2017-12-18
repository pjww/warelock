import multiple_dispatcher


class CombinedMethod(object):

    def __init__(self, class_a, class_b):

        self.class_a = class_a
        self.class_b = class_b

    def __call__(self, to_decorate):

        # stworz nowa klase pochodna od ObjectCombination jesli jeszcze nie istnieje
        comb = multiple_dispatcher.MultipleDispatcher.get_combination(self.class_a, self.class_b)

        # udekoruj otrzymana funkcje przez dodanie parametru "self", aby mogla byc metoda nowo utworzonej klasy
        def decorated(__self_cc__, *args, **kwargs):
                return to_decorate(__self_cc__.self_a, __self_cc__.self_b, *args, **kwargs)

        # zachowaj oryginalne wlasciwosci funkcji:
        decorated.__name__ = to_decorate.__name__
        decorated.__doc__ = to_decorate.__doc__

        # dodaj ja jako metode klasy kombinacji:
        setattr(comb, decorated.__name__, decorated)

        return decorated
