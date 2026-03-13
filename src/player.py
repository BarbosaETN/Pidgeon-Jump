import pygame
from settings import GRAVITY, JUMP_STRENGTH

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.velocity_y = 0

        self.frames = [
            pygame.image.load("asset/images/Pidgeon1.png").convert_alpha(),
            pygame.image.load("asset/images/Pidgeon2.png").convert_alpha(),
            pygame.image.load("asset/images/Pidgeon3.png").convert_alpha()
        ]

        self.frames = [pygame.transform.scale(frame, (50, 40)) for frame in self.frames]

        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 6

        self.image = self.frames[self.current_frame]
        self.rotated_image = self.image
        self.angle = 0

        self.rect = self.image.get_rect(center=(self.x, self.y))

    def jump(self):
        self.velocity_y = JUMP_STRENGTH

    def update(self):
        self.velocity_y += GRAVITY
        self.y += self.velocity_y

        self.animate()
        self.rotate()

        self.rect = self.rotated_image.get_rect(center=(self.x, self.y))

    def animate(self):
        self.animation_timer += 1

        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame += 1

            if self.current_frame >= len(self.frames):
                self.current_frame = 0

        self.image = self.frames[self.current_frame]

    def rotate(self):
        self.angle = -self.velocity_y * 3

        if self.angle > 25:
            self.angle = 25
        if self.angle < -90:
            self.angle = -90

        self.rotated_image = pygame.transform.rotate(self.image, self.angle)

    def draw(self, screen):
        screen.blit(self.rotated_image, self.rect)



















