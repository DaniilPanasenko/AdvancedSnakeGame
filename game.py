import board
import alphabet
import menu
import time
import keyboard
import pygame
import pixel
import settings
import play


class Game:

    def __init__(self, columns, rows, fps, one_pixel):
        self.rows = rows
        self.columns = columns
        self.fps = fps
        self.one_pixel = one_pixel
        self.pixels = []
        self.pages = []
        self.settings = settings.Settings(True)
        self.play=None
        self.game_over=False

    def initial_frame(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((self.columns * self.one_pixel, self.rows * self.one_pixel))
        pygame.display.set_caption("Snake")
        self.load_images()
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()
        for j in range(self.rows):
            internal = []
            for i in range(self.columns):
                pxl = pixel.Pixel(i * 10, j * 10, self)
                self.all_sprites.add(pxl)
                internal.append(pxl)
            self.pixels.append(internal)
        self.board = board.Board(self.pixels)
        self.transition_by_menu()

    def load_images(self):
        self.IMG_POINT = pygame.image.load('img/point.png')

    def start_game(self):
        self.initial_frame()
        self.running()
        pygame.quit()

    def running(self):
        running = True
        while running:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if self.game_over and event.key==pygame.K_RETURN:
                        self.enter_game_over()
                    elif self.active_menu.isActive:
                        self.handle_menu(event.key)
                    elif self.settings.isActive:
                        self.handle_settings(event.key)

            self.drawing()

    def drawing(self):
        self.screen.fill((0, 0, 0))
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def enter_game_over(self):
        self.board.delete_element('game_over')
        self.board.delete_element('results')
        self.pages = []
        self.transition_by_menu()
        self.game_over=False

    def add_menu(self, items):
        arr = alphabet.translate_with_zoom('SNAKE', 2)
        self.board.add_element('logo', 10, int((self.board.columns - len(arr[0])) / 2), arr)
        main_menu = menu.Menu(items)
        self.board.add_element('menu', 30, int((self.board.columns - len(main_menu.pixels[0])) / 2), main_menu.pixels)
        return main_menu

    def handle_settings(self, key):
        self.settings.press_key(key)
        self.board.delete_element('settings')
        self.board.add_element('settings', 25, int((self.board.columns - len(self.settings.get_pixels()[0])) / 2),
                               self.settings.get_pixels())
        if not self.settings.isActive:
            self.pages.pop()
            self.board.delete_element('settings')
            self.transition_by_menu()

    def handle_menu(self, key):
        if key == pygame.K_DOWN:
            self.active_menu.change_active(False)
            self.board.add_element('menu', 30, int((self.board.columns - len(self.active_menu.pixels[0])) / 2),
                                   self.active_menu.pixels)
        elif key == pygame.K_UP:
            self.active_menu.change_active(True)
            self.board.add_element('menu', 30, int((self.board.columns - len(self.active_menu.pixels[0])) / 2),
                                   self.active_menu.pixels)
        elif key == pygame.K_RETURN:
            self.active_menu.dispose()
            self.board.delete_element('menu')
            self.pages.append(self.active_menu.items[self.active_menu.active])
            self.transition_by_menu()

    def play_run(self):
        self.play.run()
        if self.play.is_stopped:
            self.board.delete_element('play')
            self.active_menu = self.add_menu(['RETURN', 'RESTART', 'MENU','EXIT'])
        if self.play.game_over:
            self.board.delete_element('play')
            arr = alphabet.translate_with_zoom('GAME OVER', 3)
            self.board.add_element('game_over', 10, int((self.board.columns - len(arr[0])) / 2), arr)
            results=self.play.get_table()
            self.board.add_element('results', 30, int((self.board.columns - len(results[0])) / 2),
                                   results)
            self.game_over=True

    def transition_by_menu(self):
        if len(self.pages) == 0:
            self.active_menu = self.add_menu(['NEW GAME', 'EXIT'])
        else:
            page = self.pages[len(self.pages) - 1]
            if page == 'EXIT':
                pygame.quit()
            if page == 'NEW GAME':
                self.active_menu = self.add_menu(['SINGLE PLAYER', 'MULTI PLAYER', 'BACK'])
            if page == 'MULTI PLAYER':
                self.active_menu = self.add_menu(['START', 'SETTINGS', 'BACK'])
            if page == 'SINGLE PLAYER':
                self.active_menu = self.add_menu(['START', 'SETTINGS', 'BACK'])
            if page == 'SETTINGS':
                if self.pages[len(self.pages) - 2] == 'SINGLE PLAYER' and not self.settings.isSinglePlayer:
                    self.settings = settings.Settings(True)
                if self.pages[len(self.pages) - 2] == 'MULTI PLAYER' and self.settings.isSinglePlayer:
                    self.settings = settings.Settings(False)
                self.settings.isActive = True
                self.settings.active_element = 0
                arr = alphabet.translate_with_zoom('SNAKE', 2)
                self.board.add_element('logo', 10, int((self.board.columns - len(arr[0])) / 2), arr)
                self.board.add_element('settings', 25,
                                       int((self.board.columns - len(self.settings.get_pixels()[0])) / 2),
                                       self.settings.get_pixels())
            if page == 'BACK':
                self.pages.pop()
                self.pages.pop()
                self.transition_by_menu()
            if page == 'START':
                if self.pages[len(self.pages) - 2] == 'SINGLE PLAYER' and not self.settings.isSinglePlayer:
                    self.settings = settings.Settings(True)
                if self.pages[len(self.pages) - 2] == 'MULTI PLAYER' and self.settings.isSinglePlayer:
                    self.settings = settings.Settings(False)
                self.board.delete_element('logo')
                self.play = play.Play(self.rows, self.settings, self)
                self.play_run()
            if page=='RETURN':
                self.board.delete_element('logo')
                self.play.is_stopped=False
                self.play_run()
            if page=='RESTART':
                self.board.delete_element('logo')
                self.play = play.Play(self.rows, self.settings, self)
                self.play_run()
            if page=='MENU':
                self.pages=[]
                self.transition_by_menu()

