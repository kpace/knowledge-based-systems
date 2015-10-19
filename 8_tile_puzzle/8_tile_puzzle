import random

CORRECT_TILES = (
    'x', '1', '2',
    '3', '4', '5',
    '6', '7', '8'
)


class State:
    def __init__(self, tiles, parent):
        self.tiles = tiles
        self.parent = parent
        self.x_pos = tiles.index('x')

    def children(self):
        children = []
        if self.x_pos + 3 <= 8:  # DOWN
            children.append(
                State(self._swaped(self.tiles, self.x_pos, self.x_pos + 3), self)
            )
        if self.x_pos - 3 >= 0:  # UP
            children.append(
                State(self._swaped(self.tiles, self.x_pos, self.x_pos - 3), self)
            )
        if self.x_pos % 3 != 0:  # LEFT
            children.append(
                State(self._swaped(self.tiles, self.x_pos, self.x_pos - 1), self)
            )
        if (self.x_pos + 1) % 3 != 0:  # RIGHT
            children.append(
                State(self._swaped(self.tiles, self.x_pos, self.x_pos + 1), self)
            )
        return children

    def _swaped(self, tiles, i, j):
        ls_copy = list(tiles)
        ls_copy[i], ls_copy[j] = ls_copy[j], ls_copy[i]
        return tuple(ls_copy)

    def __str__(self):
        s = ''
        for i, t in enumerate(self.tiles):
            s += str(t) + ' '
            if (i + 1) % 3 == 0:
                s += '\n'
        return s

s = State(CORRECT_TILES, '')
for c in s.children():
    print(c)





