import random
import cell
import biom

class Snake:
    def __init__(self, play, color):
        self.play=play
        self.color = color
        self.segments = [self.get_init_head_position()]
        self.isDied=False
        self.points=1
        self.direction=0

    def get_init_head_position(self):
        while True:
            x = random.randint(0,self.play.biom.size)
            y = random.randint(0, self.play.biom.size)
            EMPTY = 3
            all_empty=True
            for i in range(2*EMPTY+1):
                for j in range(2*EMPTY+1):
                    checking_cell=cell.Cell(x-EMPTY+i,y-EMPTY+j,self.color)
                    if not self.play.biom.check_cell(checking_cell):
                        all_empty=False
                        break
                if not all_empty:
                    break
            if all_empty:
                break
        return cell.Cell(x, y, self.color)

    def update(self):
        self.run()

    def change_direction(self,direct):
        if (self.direction-direct)%2==1:
            self.direction=direct

    def run(self):
        if len(self.segments)!=0:
            new_head_cell = biom.get_cell_by_side(self.segments[0],self.direction)
            self.segments.insert(0, new_head_cell)
            self.segments.pop()


