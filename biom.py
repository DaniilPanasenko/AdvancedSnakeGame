import random
import cell

STONE = 12
LAVA = 11
WATER = 10


def get_cell_by_side(old_cell, side):
    new_cell = cell.Cell(old_cell.x, old_cell.y, old_cell.value)
    if side == 0:
        new_cell.x = new_cell.x - 1
    if side == 1:
        new_cell.y = new_cell.y + 1
    if side == 2:
        new_cell.x = new_cell.x + 1
    if side == 3:
        new_cell.y = new_cell.y - 1
    return new_cell


class Biom:
    def __init__(self, size, on_mode):
        self.size = size
        self.cells = []
        self.matrix_cells = []
        for i in range(size):
            self.matrix_cells.append([])
            for j in range(size):
                self.matrix_cells[i].append(0)
        if on_mode:
            self.generate()

    def get_biom_values(self):
        count_cells = int(random.uniform(0, 8) * self.size * self.size / 100)
        count_biomes = random.randint(1, 4)
        return count_cells, count_biomes

    def get_biom(self, value):
        count_cells, count_biomes = self.get_biom_values()
        biomes = []
        for i in range(count_biomes):
            while True:
                x = random.randint(0, self.size - 1)
                y = random.randint(0, self.size - 1)
                new_cell = cell.Cell(x, y, value)
                if self.check_cell(new_cell):
                    break
            self.add_cell(new_cell)
            biomes.append([new_cell])
        for i in range(count_cells):
            possible_biomes = []
            for j in range(len(biomes)):
                if len(biomes[j]) != 0:
                    possible_biomes.append(j)
            cur_biom = possible_biomes[random.randint(0, len(possible_biomes) - 1)]
            cur_cell = random.randint(0, len(biomes[cur_biom]) - 1)
            possible_sides = self.get_sides_around_cell(biomes[cur_biom][cur_cell])
            side = random.randint(0, len(possible_sides) - 1)
            new_cell = get_cell_by_side(biomes[cur_biom][cur_cell], possible_sides[side])
            self.add_cell(new_cell)
            biomes[cur_biom].append(new_cell)
            new_biomes = []
            for i in range(len(biomes)):
                new_biomes.append([])
                for j in range(len(biomes[i])):
                    if len(self.get_sides_around_cell(biomes[i][j])) != 0:
                        new_biomes[i].append(biomes[i][j])
            biomes = new_biomes

    def generate(self):
        self.get_biom(STONE)
        self.get_biom(LAVA)
        self.get_biom(WATER)

    def check_cell(self, new_cell):
        if new_cell.x < 0 or new_cell.y < 0 or new_cell.x >= self.size or new_cell.y >= self.size:
            return False
        if not self.matrix_cells[new_cell.x][new_cell.y] == 0:
            return False
        return True

    def get_sides_around_cell(self, checking_cell):
        arr = []
        for i in range(4):
            new_cell = get_cell_by_side(checking_cell, i)
            if self.check_cell(new_cell):
                arr.append(i)
        return arr

    def add_cell(self, new_cell):
        self.cells.append(new_cell)
        self.matrix_cells[new_cell.x][new_cell.y] = new_cell.value
