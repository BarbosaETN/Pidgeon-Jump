import pygame
import random
from settings import HEIGHT, GROUND_HEIGHT, OBSTACLE_GAP, OBSTACLE_SPEED, BUILDING_PATH

#  classe resposável por criar e controlar os obstáculos do jogo
class Obstacle:
    def __init__(self, x, width=90):
        self.x = x  #  posição inicial do obstáculo
        self.width = width
        self.passed = False

        min_height = 80
        max_height = HEIGHT - GROUND_HEIGHT - OBSTACLE_GAP - 80

        self.top_height = random.randint(min_height, max_height)
        self.bottom_y = self.top_height + OBSTACLE_GAP
        self.bottom_height = HEIGHT - GROUND_HEIGHT - self.bottom_y

        self.top_rect = pygame.Rect(self.x, 0, self.width, self.top_height)
        self.bottom_rect = pygame.Rect(self.x, self.bottom_y, self.width, self.bottom_height)

        self.image = pygame.image.load(BUILDING_PATH).convert_alpha() #  carrega a imagem do prédio como obstáculo
        self.image = pygame.transform.scale(self.image, (self.width, 400)) #  redimensiona a imagem para o tamanho desejado
        self.flipped_image = pygame.transform.flip(self.image, False, True) #  cria uma versão invertida do obstáculo


    def update(self):
        #  move os obstáculos para a esquerda
        self.x -= OBSTACLE_SPEED
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x

    def draw(self, screen):
        top_image_y = self.top_rect.bottom - self.flipped_image.get_height()
        bottom_image_y = self.bottom_rect.y

        screen.blit(self.flipped_image, (self.x, top_image_y)) #  desenha o obstáculo superior invertido
        screen.blit(self.image, (self.x, bottom_image_y))  # desenha o obstáculo inferior

    def off_screen(self):
        #  retorna True caso o obstáculo saia da tela
        return self.x + self.width < 0

