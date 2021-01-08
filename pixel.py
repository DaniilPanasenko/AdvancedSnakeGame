import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255,255,0)

class Pixel(pygame.sprite.Sprite):
    def __init__(self, x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (x+5, y+5)
        self.color=0

    def update(self):
        if self.color==0:
            self.image.fill(BLACK)
        if self.color==1:
            self.image.fill(WHITE)
        if self.color==2:
            self.image.fill(GREEN)
        if self.color==3:
            self.image.fill(RED)
        if self.color==4:
            self.image.fill(YELLOW)
        if self.color==5:
            self.image.fill(BLUE)