import alphabet
import library

class Player:
    def __init__(self, name,  in_row, color, snake, is_bot):
        self.name =name
        self.spells = []
        self.in_row=in_row
        self.color=color
        self.snake = snake
        self.is_bot=is_bot

    def get_pixels(self):
        arr=[]
        width=0
        if self.in_row:
            points = alphabet.translate(str(self.snake.points))
            name = alphabet.translate_with_color(self.name+': ',self.color)
            width = len(name[0])+max(len(points[0]), len(alphabet.translate('000')[0]))
            arr=library.concat_words(name,points)
        else:
            arr=alphabet.translate_with_color(self.name,self.color)
            width=max(len(arr[0]), len(alphabet.translate('000')[0]))
            arr = library.append_row(arr, len(arr[0]))
            arr = library.concat_array_to_bottom(arr,alphabet.translate(str(self.snake.points)))
        for i in range(len(arr)):
            for j in range(width-len(arr[i])):
                arr[i].append(0)
        arr=library.append_row(arr,len(arr[0]))
        arr = library.append_row(arr,len(arr[0]))
        for i in range(len(self.spells)):
            arr[len(arr)-1][i]=self.spells[i]
        arr = library.append_row(arr, len(arr[0]))
        arr = library.append_column_left(arr)
        arr = library.append_column_left(arr)
        return arr


