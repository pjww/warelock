class Layer(object):

    def __init__(self, w=None, h=None, x=None, y=None, z=None, content=None, fillchar=None):
        self._w = None
        self._h = None
        self._content = None

        self.w = w or 0
        self.h = h or 0
        self.x = x or 0
        self.y = y or 0
        self.z = z or 0

        fillchar = fillchar or ' '
        self.content = content or [fillchar for _ in range(0, self.w * self.h)]

        if not isinstance(self.content, list):
            # try?
            self.content = list(self.content)

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

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, content):
        self._content = content

    def _validate_pos(self, pos):
        Layer._expect_pair(pos)
        if self.w <= pos[0] or self.h <= pos[1]:
            raise IndexError()

    def __getitem__(self, pos):
        self._validate_pos(pos)

        return self.content[pos[1] * self.w + pos[0]]

    def __setitem__(self, pos, val):
        self._validate_pos(pos)
        assert isinstance(val, basestring)

        self.content[pos[1] * self.w + pos[0]] = val[0]

    def __delitem__(self, pos):
        self._validate_pos(pos)

        self.content[pos[1] * self.w + pos[0]] = '.'

    @staticmethod
    def _expect_layer(op):
        if not isinstance(op, Layer):
            raise ValueError()

    @staticmethod
    def _expect_pair(op):
        if (not isinstance(op, tuple)) or (len(op) != 2)\
                or (not isinstance(op[0], int)) or (not isinstance(op[1], int)):
            raise ValueError()

    def pos_in(self, pos):
        Layer._expect_pair(pos)
        return (self.x <= pos[0] < self.x + self.w) and (self.y <= pos[1] < self.y + self.h)

    def __iadd__(self, other):
        self = self + other
        return self

    def __add__(self, other):
        Layer._expect_layer(other)
        nx = min(self.x, other.x)
        ny = min(self.y, other.y)
        nx2 = max(self.x + self.w, other.x + other.w)
        ny2 = max(self.y + self.h, other.y + other.h)
        new_layer = Layer(w=nx2-nx, h=ny2-ny, x=nx, y=ny, z=min(self.z, other.z))

        for y in range(new_layer.y, new_layer.y + new_layer.h):
            for x in range(new_layer.x, new_layer.x + new_layer.w):

                if self.pos_in((x, y)):
                    if other.pos_in((x, y)):
                        visible_layer = self if self.z > other.z else other
                    else:
                        visible_layer = self

                elif other.pos_in((x, y)):
                    if self.pos_in((x, y)):
                        visible_layer = self if self.z > other.z else other
                    else:
                        visible_layer = other

                else:
                    visible_layer = new_layer

                visible_item = visible_layer[x - visible_layer.x, y - visible_layer.y]

                new_layer[x - new_layer.x, y - new_layer.y] = str(visible_item)

        return new_layer

    def __radd__(self, other):
        return other + self

    def _draw(self):
        output = ''
        for i in range(0, self.w * self.h):
            if (i % self.w) == 0:
                output += '\n'
            output += self.content[i]
        return output

    def draw(self):
        print self._draw()

    def __str__(self):
        return self._draw()

    def __repr__(self):
        return {'x': self.x, 'y': self.y, 'z': self. z, 'w': self. w, 'h': self. h, 'content': self.content.__repr__()}
