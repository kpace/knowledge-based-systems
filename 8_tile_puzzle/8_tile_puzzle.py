from collections import deque
import random

CORRECT_TILES = (
    'x', '1', '2',
    '3', '4', '5',
    '6', '7', '8'
)


class State:
    def __init__(self, tiles, parent=None):
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

    def hash(self):
        return hash(self.tiles)


class Puzzle:
    def __init__(self, root):
        self.root = root

    def solve(self):
        q = deque()
        visited = set()
        q.append(self.root)

        count = 0

        while q:
            count +=1
            curr = q.popleft()

            if curr.tiles == CORRECT_TILES:
                print('Solved in %s steps' % count)
                return self._reconstruct_path(curr)

            for c in curr.children():
                count +=1
                if c.hash() not in visited:
                    visited.add(c.hash())
                    c.parent = curr
                    q.append(c)

    def _reconstruct_path(self, final):
        path = []
        while final.parent:
            path.append(final)
            final = final.parent
        path.append(final)
        return path

TEST_TILES_1 = (
    '3', '8', '4',
    '2', '6', '1',
    '7', '5', 'x'
)

TEST_TILES_2 = (
    '1', '2', 'x',
    '3', '4', '5',
    '6', '7', '8'
)

s = State(TEST_TILES_1)
p = Puzzle(s)
path = p.solve()

c = 0
while path:
    print('Step: %s' % c)
    c += 1
    print(path.pop())



