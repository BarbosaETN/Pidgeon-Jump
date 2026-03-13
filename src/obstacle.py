import pygame
import random
from settings import HEIGHT, GROUND_HEIGHT, OBSTACLE_GAP, OBSTACLE_SPEED

class Obstacle:
    def __init__(self, x, width=80):
        self.x = x
        self.width = width
        self.passed = False

        min_height = 80
        max_height = HEIGHT - GROUND_HEIGHT - OBSTACLE_GAP - 80

        self.top_height = random.randint(min_height, max_height)
        self.bottom_y = self.top_height + OBSTACLE_GAP
        self.bottom_height = HEIGHT - GROUND_HEIGHT - self.bottom_y

        self.top_rect = pygame.Rect(self.x, 0, self.width, self.top_height)
        self.bottom_rect = pygame.Rect(self.x, self.bottom_y, self.width, self.bottom_height)

    def update(self):
        self.x -= OBSTACLE_SPEED
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x

    def draw(self, screen):
        pygame.draw.rect(screen, (70, 70, 70), self.top_rect)
        pygame.draw.rect(screen, (90, 90, 90), self.bottom_rect)

    def off_screen(self):
        return self.x + self.width < 0

