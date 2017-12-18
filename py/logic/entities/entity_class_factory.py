from xml.dom import minidom

from logic.entities.creature.playable import Playable
from logic.entities.creature.npc import NPC
from logic.entities.obstacle.obstacle import Obstacle

from tools.misc.id_conversion import xml_to_py


class EntityClassFactory(object):

    @staticmethod
    def from_xml(path):
        if not isinstance(path, basestring):
            raise ValueError()

        dom = minidom.parse(path)

        data = dom.firstChild

        if not data.nodeName == 'data':
            raise StandardError()

        props = {}

        for data_child in data.childNodes:

            if data_child.nodeName == '#text':
                pass

            elif data_child.nodeName == 'properties':

                for prop_child in data_child.childNodes:

                    if not prop_child.nodeName == '#text':

                        # jesli trzeba, skonwertuj odpowiednio wartosc atrybutu:
                        if prop_child.getAttribute('type') == 'int':
                            val = int(prop_child.getAttribute('val'))
                        elif prop_child.getAttribute('type') == 'char':
                            val = str(list(prop_child.getAttribute('val'))[0])
                        else:
                            val = prop_child.getAttribute('val')

                        props[xml_to_py(prop_child.nodeName)] = val

            elif data_child.nodeName == 'entity':

                for prop_child in data_child.childNodes:

                    if prop_child.nodeName == '#text':
                        pass

                    elif prop_child.nodeName == 'base-class':
                        base_class_name = prop_child.getAttribute('name')

                    elif prop_child.nodeName == 'class':
                        class_name = prop_child.getAttribute('name')

                    else:
                        raise StandardError()

            else:
                raise StandardError()

        try:
            new_class = type(str(class_name), (globals()[xml_to_py(base_class_name)],), props)
        except NameError:
            # nie okreslono klasy bazowej:
            raise StandardError()

        return new_class
