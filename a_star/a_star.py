import csv
import heapq
import sys

DIRECTIONS = (
    (-1, 0), (1, 0), (0, -1), (0, 1),  # straights
    (1, 1), (-1, -1), (-1, 1), (1, -1)  # diagonals
)

class Cell:
    def __init__(self, symbol, pos):
        self.symbol = symbol
        self.pos = pos
        self.f, self.g = sys.maxsize,  sys.maxsize
        self.closed, self.open = False, False
        self.parent = None

    @property
    def passable(self):
        return self.symbol.upper() != 'N'

    def __hash__(self):
        return hash((self.symbol, self.pos))

    def __eq__(self, other):
        return (self.symbol, self.pos) == (other.symbol, other.pos)

    def __cmp__(self, other):
        # equivalent to cmp(a, b)
        return (self.f > other.f) - (self.f < other.f)

    def __lt__(self, other):
        return self.g < other.g

class Puzzle:
    def __init__(self, csv_file, x1, y1, x2, y2):
        self.start = x1, y1
        self.end = x2, y2
        self.__parse_puzzle(csv_file)

    def __str__(self):
        s = ''
        for row in self.puzzle:
            s += ''.join(map(lambda c: c.symbol, row))
            s += '\n'
        return s

    def __parse_puzzle(self, file):
        self.puzzle = []
        with open(file, encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            for i, row in enumerate(reader):
                self.puzzle.append([Cell(c, (i, j)) for j, c in enumerate(row)])

    @staticmethod
    def h(start, end):
        return abs(end.pos[0] - start.pos[0]) + abs(end.pos[1] - start.pos[1])

    @staticmethod
    def dist(current, neighbour):
        if Puzzle.h(current, neighbour) > 2:
            raise ValueError('g(current, neighbour) accepts only adjacent cells')
        if not neighbour.passable:
            raise ValueError('Invoking g(current, neighbour) with not passable neighbour')
        if neighbour.symbol == '~':  # water
            return 2
        elif Puzzle.h(current, neighbour) == 2:  # diagonal
            return 1.5
        else:
            return 1

    @staticmethod
    def _reconstruct_path(current):
        path = []
        while current:
            path.append(current.pos)
            current = current.parent
        return path

    def children(self, cell):
        height, width = len(self.puzzle), len(self.puzzle[0])
        x, y = cell.pos
        return [self.puzzle[x + i][y + j] for i, j in DIRECTIONS
                if x + i in range(height) and y + j in range(width)
                and self.puzzle[x + i][y + j].passable]

    def solve(self):
        start = self.puzzle[self.start[0]][self.start[1]]
        end = self.puzzle[self.end[0]][self.end[1]]

        opened = [start]
        start.g = 0
        start.f = start.g + self.h(start, end)
        while opened:
            current = heapq.heappop(opened)
            current.closed = True

            if current == end:
                return self._reconstruct_path(current)

            for c in self.children(current):
                if c.closed or not c.passable:
                    continue

                tentative = current.g + self.dist(current, c)
                if tentative < c.g or not c.open:
                    c.g = tentative
                    c.f = tentative + Puzzle.h(c, end)
                    c.parent = current
                    if not c.open:
                        heapq.heappush(opened, c)
                        # this is set as property for the sake of speed
                        # the check "if not c.open" can be replaced with "if c not in opened"
                        c.open = True

if __name__ == '__main__':
    p = Puzzle(sys.argv[1], *map(int, sys.argv[2:]))
    path = p.solve()
    if path:
        print('Start: %s' % str(path[-1]))
        print('End: %s' % str(path[0]))
        print('Path:')
        while path:
            print(path.pop())
    else:
        print('No way.')
