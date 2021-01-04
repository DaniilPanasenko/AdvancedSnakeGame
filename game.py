import board
import alphabet
import menu
import time
import keyboard
import pygame
import pixel


class Game:

    def __init__(self, columns, rows, fps, one_pixel):
        self.rows = rows
        self.columns = columns
        self.fps = fps
        self.one_pixel = one_pixel
        self.pixels = []
        self.pages=[]

    def initial_frame(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((self.columns * self.one_pixel, self.rows * self.one_pixel))
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()
        for j in range(self.rows):
            internal = []
            for i in range(self.columns):
                pxl = pixel.Pixel(i * 10, j * 10)
                self.all_sprites.add(pxl)
                internal.append(pxl)
            self.pixels.append(internal)
        self.board = board.Board(self.pixels)
        self.active_menu = self.main_menu()

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
                    if self.active_menu.isActive:
                        self.handle_menu(event.key)

            self.drawing()

    def drawing(self):
        self.screen.fill((0, 0, 0))
        self.all_sprites.update()
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

    def main_menu(self):
        arr = alphabet.translate_with_zoom('SNAKE', 2)
        self.board.add_element('logo', 10, int((self.board.columns - len(arr[0])) / 2), arr)
        main_menu = menu.Menu(['NEW GAME', 'CONTINUE', 'EXIT'])
        self.board.add_element('menu', 30, int((self.board.columns - len(main_menu.pixels[0])) / 2), main_menu.pixels)
        return main_menu

    def handle_menu(self, key):
        if key == pygame.K_DOWN:
            self.active_menu.change_active(False)
            self.board.delete_element('menu')
            self.board.add_element('menu', 30, int((self.board.columns - len(self.active_menu.pixels[0])) / 2), self.active_menu.pixels)
        elif key == pygame.K_UP:
            self.active_menu.change_active(True)
            self.board.delete_element('menu')
            self.board.add_element('menu', 30, int((self.board.columns - len(self.active_menu.pixels[0])) / 2), self.active_menu.pixels)
        elif key == pygame.K_RETURN:
            self.active_menu.dispose()
            self.board.delete_element('menu')
            self.pages.append(self.active_menu.items[self.active_menu.active])
            self.transition_by_menu()

    def transition_by_menu(self):
        page = self.pages[len(self.pages)-1]
        if page=='EXIT':
            pygame.quit()
