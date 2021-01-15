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
        self.snail =0

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
        if not self.isDied and self.snail==0:
            self.run()

    def check_state(self):
        if len(self.segments)==0:
            self.isDied=True
        if not self.isDied:
            head = self.segments[0]
            if self.check_stone_hit(head) or self.check_snake_hit(head):
                self.isDied=True
                self.segments=[]
            elif self.check_lava_hit(head):
                self.segments.pop()
                self.points=self.points-1
                if len(self.segments)==0:
                    self.isDied = True
            elif self.check_water_hit(head):
                if self.snail==0:
                    self.snail=3
                else:
                    self.snail=self.snail-1

    def check_stone_hit(self, head):
        if head.x==-1 or head.y==-1 or head.x==self.play.biom.size or head.y==self.play.biom.size:
            return True
        if self.play.biom.matrix_cells[head.x][head.y]==biom.STONE:
            return True
        return False

    def check_lava_hit(self, head):
        if self.play.biom.matrix_cells[head.x][head.y]==biom.LAVA:
            return True
        return False

    def check_water_hit(self, head):
        if self.play.biom.matrix_cells[head.x][head.y]==biom.WATER:
            return True
        return False

    def check_snake_hit(self, head):
        for snake in self.play.snakes:
            for j in range(len(snake.segments)):
                if head.x == snake.segments[j].x and head.y == snake.segments[j].y:
                    if self.color!=snake.color or j!=0:
                        return True
        return False


    def change_direction(self, direct):
        if (self.direction - direct) % 2 == 1:
            self.direction = direct

    def check_spells(self, new_head_cell):
        for i in range(len(self.play.spells.spells)):
            spell=self.play.spells.spells[i]
            if spell.cell.x==new_head_cell.x and spell.cell.y==new_head_cell.y:
                if spell.type=='POINT':
                    self.play.spells.spells.pop(i)
                    tail = self.segments[len(self.segments)-1]
                    self.segments.append(cell.Cell(tail.x,tail.y,tail.value))
                    self.points=self.points+1
                break


    def run(self):
        if len(self.segments) != 0:
            new_head_cell = biom.get_cell_by_side(self.segments[0], self.direction)
            self.check_spells(new_head_cell)
            self.segments.insert(0, new_head_cell)
            self.segments.pop()


