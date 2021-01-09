import alphabet
import player
import library
import biom
import pygame


class Play:
    def __init__(self, height, settings, game):
        self.settings = settings
        self.board_size = self.get_init_size(height)
        self.game = game
        self.isActive = True
        self.players = self.get_init_players()
        self.biom = biom.Biom(self.board_size, self.settings.items['BIOMES'])

    def run(self):
        while True:
            self.game.clock.tick(5)
            events = pygame.event.get()
            keydown=None
            for ev in events:
                if ev.type == pygame.QUIT:
                    self.quit()
                elif ev.type == pygame.KEYDOWN:
                    keydown=ev
            if not keydown is None:
                self.press_key(keydown.key)
            self.draw()
            self.game.drawing()

    def draw(self):
        self.game.board.delete_element('play')
        self.game.board.add_element('play',
                                    int((self.game.board.rows - len(self.get_pixels())) / 2),
                                    int((self.game.board.columns - len(self.get_pixels()[0])) / 2),
                                    self.get_pixels())

    def press_key(self, key):
        if key ==pygame.K_ESCAPE:
            self.quit()

    def quit(self):
        pygame.quit()

    def get_pixels(self):
        arr = self.get_init_board()
        arr = library.concat_array_to_right(arr, self.get_table())
        arr = self.get_biomes(arr)
        return arr

    def get_init_size(self, height):
        min_size = 20
        max_size = height - 6
        return min_size + int((max_size - min_size) * self.settings.items['SIZE'] / 10)

    def get_init_players(self):
        arr = []
        if self.settings.isSinglePlayer:
            arr.append(player.Player('ME', True, 20))
            for i in range(self.settings.items['BOTS']):
                arr.append(player.Player('BOT ' + str(i + 1), True, i + 21))
        else:
            arr.append(player.Player(self.settings.items['P1'], False, 24))
            arr.append(player.Player(self.settings.items['P2'], False, 25))
        return arr

    def get_table(self):
        arr = []
        for i in range(len(self.players)):
            arr = library.concat_array_to_bottom(arr, self.players[i].get_pixels())
        return arr

    def get_biomes(self, arr):
        for new_cell in self.biom.cells:
            arr = self.add_cell(arr, new_cell)
        return arr

    def add_cell(self, arr, new_cell):
        arr[new_cell.x + 1][new_cell.y + 1] = new_cell.value
        return arr

    def get_init_board(self):
        arr = []
        for i in range(self.board_size + 2):
            internal = []
            for j in range(self.board_size + 2):
                internal.append(0)
            arr.append(internal)
        for i in range(len(arr)):
            arr[i][0] = 12
            arr[i][len(arr[i]) - 1] = 12
        for i in range(len(arr[0])):
            arr[0][i] = 12
            arr[len(arr[i]) - 1][i] = 12
        return arr
