import random
import cell
import biom
import spells


class Snake:
    def __init__(self, play, color):
        self.play = play
        self.color = color
        self.segments = [self.get_init_head_position()]
        self.isDied = False
        self.points = 1
        self.direction = 0
        self.snail = 0

    def get_init_head_position(self):
        while True:
            x = random.randint(0, self.play.biom.size)
            y = random.randint(0, self.play.biom.size)
            CONST_EMPTY = 3
            all_empty = True
            for i in range(2 * CONST_EMPTY + 1):
                for j in range(2 * CONST_EMPTY + 1):
                    checking_cell = cell.Cell(x - CONST_EMPTY + i, y - CONST_EMPTY + j, self.color)
                    if not self.play.biom.check_cell(checking_cell):
                        all_empty = False
                        break
                if not all_empty:
                    break
            if all_empty:
                break
        return cell.Cell(x, y, self.color)

    def update(self):
        if not self.isDied and self.snail == 0:
            self.run()

    def check_state(self):
        if len(self.segments) == 0:
            self.isDied = True
        if not self.isDied:
            head = self.segments[0]
            if self.check_stone_hit(head) or self.check_snake_hit(head):
                self.isDied = True
                self.segments = []
            elif self.check_lava_hit(head):
                self.segments.pop()
                self.points = self.points - 1
                if len(self.segments) == 0:
                    self.isDied = True
            elif self.check_water_hit(head):
                if self.snail == 0:
                    self.snail = 3
                else:
                    self.snail = self.snail - 1

    def check_stone_hit(self, head):
        if head.x == -1 or head.y == -1 or head.x == self.play.biom.size or head.y == self.play.biom.size:
            return True
        if self.play.biom.matrix_cells[head.x][head.y] == biom.STONE:
            return True
        return False

    def check_lava_hit(self, head):
        if self.play.biom.matrix_cells[head.x][head.y] == biom.LAVA:
            return True
        return False

    def check_water_hit(self, head):
        if self.play.biom.matrix_cells[head.x][head.y] == biom.WATER:
            return True
        return False

    def check_snake_hit(self, head):
        for snake in self.play.snakes:
            for j in range(len(snake.segments)):
                if head.x == snake.segments[j].x and head.y == snake.segments[j].y:
                    if self.color != snake.color or j != 0:
                        return True
        return False

    def change_direction(self, direct):
        if (self.direction - direct) % 2 == 1:
            self.direction = direct

    def check_spells(self, new_head_cell):
        for i in range(len(self.play.spells.spells)):
            spell = self.play.spells.spells[i]
            if spell.cell.x == new_head_cell.x and spell.cell.y == new_head_cell.y:
                if spell.type == 'POINT':
                    self.play.spells.spells.pop(i)
                    tail = self.segments[len(self.segments) - 1]
                    self.segments.append(cell.Cell(tail.x, tail.y, tail.value))
                    self.points = self.points + 1
                break

    def check_hit(self, head):
        if self.check_stone_hit(head):
            return True
        if self.check_snake_hit(head):
            return True
        if self.check_lava_hit(head):
            return True
        if self.check_water_hit(head):
            return True
        return False

    def bot(self, difficulty):
        rand = random.randint(0,10)
        if rand<=5+difficulty:
            spells_distance = []
            times = []
            points = []
            for spell in self.play.spells.spells:
                if spell.type == 'POINT':
                    points.append(spell)
                    spells_distance.append(abs(self.segments[0].x - spell.cell.x) + abs(self.segments[0].y - spell.cell.y))
                    times.append(spell.time)
            indices = list(range(len(spells_distance)))
            spells_distance_copy=spells_distance.copy()
            for i in range(len(spells_distance_copy) - 1):
                for j in range(len(spells_distance_copy) - i - 1):
                    if spells_distance_copy[j] > spells_distance_copy[j + 1]:
                        spells_distance_copy[j], spells_distance_copy[j + 1] = spells_distance_copy[j + 1], spells_distance_copy[j]
                        indices[j], indices[j + 1] = indices[j + 1], indices[j]
            current_direction = self.direction
            for i in range(len(indices)):
                choose_point = False
                if spells_distance[indices[i]] < times[indices[i]]:
                    for j in range(3):
                        if j == 1:
                            self.change_direction((current_direction + 1) % 4)
                        if j == 2:
                            self.change_direction((current_direction - 1) % 4)
                        new_cell = biom.get_cell_by_side(self.segments[0], self.direction)
                        new_distance = abs(new_cell.x - points[indices[i]].cell.x) + \
                                       abs(new_cell.y - points[indices[i]].cell.y)
                        if new_distance < spells_distance[indices[i]]:
                            if not self.check_hit(new_cell):
                                choose_point = True
                                break
                        self.change_direction(current_direction)
                if choose_point:
                    break
            if not self.check_hit(biom.get_cell_by_side(self.segments[0], self.direction)):
                return
            if not self.check_hit(biom.get_cell_by_side(self.segments[0], (self.direction+1)%4)):
                self.change_direction((current_direction + 1) % 4)
                return
            if not self.check_hit(biom.get_cell_by_side(self.segments[0], (self.direction-1)%4)):
                self.change_direction((current_direction - 1) % 4)
                return

    def run(self):
        if len(self.segments) != 0:
            new_head_cell = biom.get_cell_by_side(self.segments[0], self.direction)
            self.check_spells(new_head_cell)
            self.segments.insert(0, new_head_cell)
            self.segments.pop()
