class Board:
    class Element:
        def __init__(self, x, y, arr):
            self.x = x
            self.y = y
            self.width = len(arr[0])
            self.height = len(arr)

    def __init__(self, pixels):
        self.rows = len(pixels)
        self.columns = len(pixels[0])
        self.board = pixels
        self.set_bound()
        self.elements = {}

    def set_bound(self):
        for i in range(self.rows):
            self.board[i][0].color = 1
            self.board[i][self.columns - 1].color = 1
        for i in range(self.columns):
            self.board[0][i].color = 1
            self.board[self.rows - 1][i].color = 1

    def add_element(self, name, x, y, arr):
        self.elements[name] = self.Element(x, y, arr)
        for i in range(len(arr)):
            for j in range(len(arr[i])):
                self.board[i + x][j + y].color = arr[i][j]

    def delete_element(self, name):
        element = self.elements[name]
        for i in range(element.height):
            for j in range(element.width):
                self.board[i + element.x][j + element.y].color = 0
        self.elements.pop(name)

