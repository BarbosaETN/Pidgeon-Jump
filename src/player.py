import pygame
from settings import GRAVITY, JUMP_STRENGTH

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.width = 40
        self.height = 30

        self.velocity_y = 0
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def jump(self):
        self.velocity_y = JUMP_STRENGTH

    def update(self):
        self.velocity_y += GRAVITY
        self.y += self.velocity_y
        self.rect.y = int(self.y)

    def draw(self, screen):
        pygame.draw.rect(screen, (220, 220, 220), self.rect)
