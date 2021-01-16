import cell
import  random

SPELLS = [['POINT',30,False,50,15]]


class Spells:
    class Spell:
        def __init__(self,spell_cell):
            self.cell=spell_cell
            for spell in SPELLS:
                if spell[1]==self.cell.value:
                    self.type=spell[0]
                    self.isRemembered=spell[2]
                    self.time=spell[3]

    def __init__(self, play):
        self.play=play
        self.spells=[]

    def update(self):
        self.generate()
        for i in range(len(self.spells)):
            self.spells[i].time=self.spells[i].time-1
        new_spells=[]
        for spell in self.spells:
            if spell.time!=0:
                new_spells.append(spell)
        self.spells=new_spells

    def generate(self):
        for spell in SPELLS:
            rand = random.randint(1,spell[4])
            if rand==1:
                while True:
                    x = random.randint(0, self.play.biom.size - 1)
                    y = random.randint(0, self.play.biom.size - 1)
                    new_cell = cell.Cell(x, y, spell[1])
                    if self.check_cell(new_cell):
                        break
                self.spells.append(self.Spell(new_cell))


    def check_cell(self, new_cell):
        if self.play.biom.matrix_cells[new_cell.x][new_cell.y]!=0:
            return False
        for snake in self.play.snakes:
            for segment in snake.segments:
                if segment.x==new_cell.x and segment.y==new_cell.y:
                    return False
        for spell in self.spells:
            if spell.cell.x == new_cell.x and spell.cell.y == new_cell.y:
                return False
        return True


