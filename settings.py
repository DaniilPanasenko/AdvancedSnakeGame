import pygame
import library
import alphabet


class Settings:
    def __init__(self, is_single_player):
        self.isSinglePlayer = is_single_player
        self.active_element = 0
        self.isActive = False
        self.items = {'BIOMES': True,
                      'SPEED': 5,
                      'SIZE': 5}
        if not self.isSinglePlayer:
            self.items['P1'] = 'PLAYER1'
            self.items['P2'] = 'PLAYER2'
        else:
            self.items['BOTS'] = 0
            self.items['DIFFICULTY'] = 3

    def get_pixels(self):
        arr = self.get_array_to_print()
        width = 0
        for item in arr:
            if len(item[0]) + 3 > width:
                width = len(item[0]) + 3
        result_arr = []
        result_arr = library.append_row(result_arr, width)
        for i in range(len(arr)):
            result_arr = library.append_row(result_arr, width)
            if i != len(arr) - 1:
                for row in arr[i]:
                    result_arr = library.append_row(result_arr, width)
                    for i in range(len(row)):
                        result_arr[len(result_arr) - 1][i + 2] = row[i]
            else:
                result_arr = library.append_row(result_arr, width)
                result_arr = library.append_row(result_arr, width)
                for row in arr[i]:
                    result_arr = library.append_row(result_arr, width)
                    save_width = len(row)
                    for i in range(len(row)):
                        result_arr[len(result_arr) - 1][i + int((width - save_width) / 2)] = row[i]
            result_arr = library.append_row(result_arr, width)
            result_arr = library.append_row(result_arr, width)
        return result_arr

    def get_array_to_print(self):
        arr = []
        keys = list(self.items.keys())
        values = list(self.items.values())
        for i in range(len(self.items)):
            if i == self.active_element:
                key = alphabet.translate_with_color(keys[i] + ': ', 5)
            else:
                key = alphabet.translate(keys[i] + ': ')
            if keys[i] == 'BIOMES':
                if values[i]:
                    value = alphabet.translate_with_color('ON', 2)
                else:
                    value = alphabet.translate_with_color('OFF', 3)
            else:
                value = alphabet.translate_with_color(str(values[i]), 4)
            arr.append(library.concat_words(key, value))
        if self.active_element == len(self.items):
            arr.append(alphabet.translate_with_color('SAVE', 5))
        else:
            arr.append(alphabet.translate_with_color('SAVE', 2))
        return arr

    def press_key(self, key):
        if self.active_element != len(self.items):
            name = list(self.items.keys())[self.active_element]
        if key == pygame.K_DOWN:
            if self.active_element != len(self.items):
                self.active_element = self.active_element + 1
        elif key == pygame.K_UP:
            if self.active_element != 0:
                self.active_element = self.active_element - 1
        elif key == pygame.K_LEFT:
            if self.active_element != len(self.items):
                if name == 'BIOMES':
                    self.items[name] = not self.items[name]
                if (name == 'SPEED' or name == 'SIZE') and self.items[name] != 1:
                    self.items[name] = self.items[name] - 1
                if (name == 'BOTS' or name == 'DIFFICULTY') and self.items[name] != 0:
                    self.items[name] = self.items[name] - 1
        elif key == pygame.K_RIGHT:
            if self.active_element != len(self.items):
                if name == 'BIOMES':
                    self.items[name] = not self.items[name]
                if (name == 'SPEED' or name == 'SIZE') and self.items[name] != 10:
                    self.items[name] = self.items[name] + 1
                if name == 'BOTS' and self.items[name] != 3:
                    self.items[name] = self.items[name] + 1
                if name == 'DIFFICULTY' and self.items[name] != 5:
                    self.items[name] = self.items[name] + 1
        elif key == pygame.K_RETURN:
            if self.active_element == len(self.items):
                self.isActive = False
        elif key == pygame.K_BACKSPACE:
            if name == 'P1' or name == 'P2':
                self.items[name] = self.items[name][0:len(self.items[name]) - 1]
        elif name == 'P1' or name == 'P2':
            if len(self.items[name]) != 11:
                if (key >= pygame.K_a and key <= pygame.K_z):
                    self.items[name] = self.items[name] + pygame.key.name(key).upper()
                if (key >= pygame.K_0 and key <= pygame.K_9):
                    self.items[name] = self.items[name] + pygame.key.name(key)
