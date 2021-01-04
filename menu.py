import alphabet


def append_row(arr, width):
    internal_arr = []
    for j in range(width):
        internal_arr.append(0)
    arr.append(internal_arr)
    return arr


class Menu:
    def __init__(self, items):
        self.items = items
        self.active = 0
        self.pixels = self.set_pixels()
        self.isActive = True

    def set_pixels(self):
        arr = []
        for i in range(len(self.items)):
            if i == self.active:
                arr.append(alphabet.translate_with_color(self.items[i], 2))
            else:
                arr.append(alphabet.translate(self.items[i]))
        width = 0
        for item in arr:
            if len(item[0]) + 3 > width:
                width = len(item[0]) + 3
        result_arr = []
        result_arr = append_row(result_arr, width)
        for item in arr:
            result_arr = append_row(result_arr, width)
            for row in item:
                result_arr = append_row(result_arr, width)
                for i in range(len(row)):
                    result_arr[len(result_arr) - 1][i + 2] = row[i]
            result_arr = append_row(result_arr, width)
            result_arr = append_row(result_arr, width)
        return result_arr

    def change_active(self, isUp):
        if isUp and self.active != 0:
            self.active = self.active - 1
        if not isUp and self.active != len(self.items) - 1:
            self.active = self.active + 1
        self.pixels = self.set_pixels()

    def dispose(self):
        self.isActive = False
