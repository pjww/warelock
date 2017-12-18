import object_combination
from collections import OrderedDict


class MultipleDispatcher(object):

    # (klasa a, klasa b) -> klasa ObjectCombination
    combinations = OrderedDict()

    # mozna uzyc po prostu dict,
    # ale po tym, jak wprowadzilem sprawdzanie podklas
    # musze brac jakies kryterium, ktore dopasowanie jest lepsze -
    # teraz wiec liczy sie kolejnosc definiowania multimetod

    @staticmethod
    def concatenate_names(names):
        res = "__Comb_"
        for name in names:
            res += name + "_"
        res += "_"
        return res

    @staticmethod
    def get_combination(class_a, class_b):
        combination_key = (class_a, class_b)

        # poszukaj dokladnej kombinacji klas:
        comb = MultipleDispatcher.combinations.get((class_a, class_b))

        if comb is None:

            # sprawdz jeszcze, czy dane klasy nie sa podklasami ktorejs z klas w rejestrze:
            for key in MultipleDispatcher.combinations:
                if issubclass(class_a, key[0]) and issubclass(class_b, key[1]):
                    comb = MultipleDispatcher.combinations[key]
                    break

            if comb is None:

                # jesli brak, to utworz nowa klase kombinacji:
                comb = type(MultipleDispatcher.concatenate_names([class_a.__name__, class_b.__name__]),
                            (object_combination.ObjectCombination,), {})
                MultipleDispatcher.combinations[combination_key] = comb

        return comb

    @staticmethod
    def comb_instance(instance_a, instance_b):
        return MultipleDispatcher.get_combination(instance_a.__class__, instance_b.__class__)(instance_a, instance_b)
