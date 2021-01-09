import alphabet
import library

class Player:
    def __init__(self, name,  in_row, color, snake):
        self.name =name
        self.spells = []
        self.in_row=in_row
        self.color=color
        self.snake = snake

    def get_pixels(self):

        arr=[]
        width=0
        if self.in_row:
            width = max(len(alphabet.translate(str(self.snake.points))[0]), len(alphabet.translate('000')[0]))
            arr=library.concat_words(alphabet.translate_with_color(self.name+': ',self.color),alphabet.translate(str(self.snake.points)))
        else:
            arr=alphabet.translate_with_color(self.name,self.color)
            width=max(len(arr[0]), len(alphabet.translate('000')[0]))
        for i in range(len(arr)):
            for j in range(width-len(arr[i])):
                arr[i].append(0)
        if not self.in_row:
            arr = library.append_row(arr, len(arr[0]))
            arr_points = alphabet.translate(str(self.snake.points))
            for i in range(len(arr_points)):
                arr.append(arr_points[i])
        arr=library.append_row(arr,len(arr[0]))
        arr = library.append_row(arr,len(arr[0]))
        for i in range(len(self.spells)):
            arr[len(arr)-1][i]=self.spells[i]
        arr = library.append_row(arr, len(arr[0]))
        arr = library.append_column_left(arr)
        arr = library.append_column_left(arr)
        return arr


