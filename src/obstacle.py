import pygame
import random
from settings import HEIGHT, GROUND_HEIGHT, OBSTACLE_GAP, OBSTACLE_SPEED, BUILDING_PATH

class Obstacle:
    def __init__(self, x, width=90):
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

        self.image = pygame.image.load(BUILDING_PATH).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, 400))
        self.flipped_image = pygame.transform.flip(self.image, False, True)


    def update(self):
        self.x -= OBSTACLE_SPEED
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x

    def draw(self, screen):
        top_image_y = self.top_rect.bottom - self.flipped_image.get_height()
        bottom_image_y = self.bottom_rect.y

        screen.blit(self.flipped_image, (self.x, top_image_y))
        screen.blit(self.image, (self.x, bottom_image_y))

    def off_screen(self):
        return self.x + self.width < 0

