import alphabet
import player
import library
import biom
import pygame
import snake
import spells


class Play:
    def __init__(self, height, settings, game):
        self.settings = settings
        self.board_size = self.get_init_size(height)
        self.game = game
        self.is_active = True
        self.biom = biom.Biom(self.board_size, self.settings.items['BIOMES'])
        self.players, self.snakes = self.get_init_players()
        self.spells = spells.Spells(self)
        self.is_stopped = False
        self.game_over=False


    def run(self):
        while True:
            if self.game_over:
                return
            self.game.clock.tick(5)
            events = pygame.event.get()
            keydown1=None
            keydown2 = None
            for ev in events:
                if ev.type == pygame.QUIT:
                    pygame.quit()
                elif ev.type == pygame.KEYDOWN:
                    if ev.key==pygame.K_ESCAPE:
                        self.is_stopped = True
                        return
                    if ev.key==pygame.K_RIGHT or ev.key==pygame.K_LEFT or ev.key==pygame.K_UP or ev.key==pygame.K_DOWN:
                        keydown1=ev
                    if ev.key==pygame.K_a or ev.key==pygame.K_s or ev.key==pygame.K_w or ev.key==pygame.K_d:
                        keydown2=ev
            if not keydown1 is None:
                self.press_key(keydown1.key)
            if not keydown2 is None:
                self.press_key(keydown2.key)
            self.update()
            self.draw()
            self.game.drawing()

    def draw(self):
        self.game.board.delete_element('play')
        self.game.board.add_element('play',
                                    int((self.game.board.rows - len(self.get_pixels())) / 2),
                                    int((self.game.board.columns - len(self.get_pixels()[0])) / 2),
                                    self.get_pixels())

    def update(self):
        if self.check_game_over():
            self.game_over=True
            return
        for sn in self.snakes:
            sn.update()
        for sn in self.snakes:
            sn.check_state()
        self.spells.update()

    def check_game_over(self):
        for sn in self.snakes:
            if not sn.isDied:
                return False
        return True

    def press_key(self, key):
        if key ==pygame.K_UP:
            self.snakes[0].change_direction(0)
        if key ==pygame.K_RIGHT:
            self.snakes[0].change_direction(1)
        if key ==pygame.K_DOWN:
            self.snakes[0].change_direction(2)
        if key ==pygame.K_LEFT:
            self.snakes[0].change_direction(3)
        if not self.settings.isSinglePlayer:
            if key == pygame.K_w:
                self.snakes[1].change_direction(0)
            if key == pygame.K_d:
                self.snakes[1].change_direction(1)
            if key == pygame.K_s:
                self.snakes[1].change_direction(2)
            if key == pygame.K_a:
                self.snakes[1].change_direction(3)

    def get_pixels(self):
        arr = self.get_init_board()
        arr = library.concat_array_to_right(arr, self.get_table())
        arr = self.get_biomes(arr)
        arr = self.get_snakes(arr)
        arr = self.get_spells(arr)
        return arr

    def get_init_size(self, height):
        min_size = 20
        max_size = height - 6
        return min_size + int((max_size - min_size) * self.settings.items['SIZE'] / 10)

    def get_init_players(self):
        players = []
        snakes = []
        if self.settings.isSinglePlayer:
            snakes.append(snake.Snake(self, 20))
            players.append(player.Player('ME', True, 20,snakes[len(snakes)-1]))
            for i in range(self.settings.items['BOTS']):
                snakes.append(snake.Snake(self, i + 21))
                players.append(player.Player('BOT ' + str(i + 1), True, i + 21,snakes[len(snakes)-1]))
        else:
            snakes.append(snake.Snake(self, 24))
            players.append(player.Player(self.settings.items['P1'], False, 24,snakes[len(snakes)-1]))
            snakes.append(snake.Snake(self, 25))
            players.append(player.Player(self.settings.items['P2'], False, 25,snakes[len(snakes)-1]))
        return players, snakes

    def get_table(self):
        arr = []
        width=0
        players = []
        results=[]
        for player in self.players:
            results.append(player.snake.points)
        results.sort()
        results.reverse()
        for i in range(len(results)):
            for player in self.players:
                if results[i]==player.snake.points:
                    is_new=True
                    for pl in players:
                        if player.name==pl.name:
                            is_new=False
                            break
                    if is_new:
                        players.append(player)
        for player in players:
            results.append(player.snake.points)
        for i in range(len(players)):
            width = max(width,len(players[i].get_pixels()[0]))
            arr = library.concat_array_to_bottom(arr, players[i].get_pixels())
        for i in range(len(arr)):
            to_add=width-len(arr[i])
            for j in range(to_add):
                arr[i].append(0)
        return arr

    def get_biomes(self, arr):
        for new_cell in self.biom.cells:
            arr = self.add_cell(arr, new_cell)
        return arr

    def get_snakes(self,arr):
        for snake in self.snakes:
            for new_cell in snake.segments:
                arr = self.add_cell(arr, new_cell)
        return arr

    def get_spells(self,arr):
        for spell in self.spells.spells:
            arr = self.add_cell(arr, spell.cell)
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
