import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPUR = (255,0,255)

WATER = (0,191,255)
STONE = (128,128,128)
LAVA = (255,117,24)

class Pixel(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pygame.Surface((10, 10))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (x + 5, y + 5)
        self.color = 0

    def update(self):
        if self.color == 0:
            self.image.fill(BLACK)
        if self.color == 1:
            self.image.fill(WHITE)
        if self.color == 2:
            self.image.fill(GREEN)
        if self.color == 3:
            self.image.fill(RED)
        if self.color == 4:
            self.image.fill(YELLOW)
        if self.color == 5:
            self.image.fill(BLUE)

        if self.color == 10:
            self.image.fill(WATER)
        if self.color == 11:
            self.image.fill(LAVA)
        if self.color == 12:
            self.image.fill(STONE)

        if self.color == 20:
            self.image.fill(GREEN)
        if self.color == 21:
            self.image.fill(YELLOW)
        if self.color == 22:
            self.image.fill(BLUE)
        if self.color == 23:
            self.image.fill(RED)
        if self.color == 24:
            self.image.fill(RED)
        if self.color == 25:
            self.image.fill(BLUE)

        if self.color == 30:
            self.image.fill(PURPUR)

