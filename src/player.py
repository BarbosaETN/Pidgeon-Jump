import pygame
from settings import GRAVITY, JUMP_STRENGTH, PIGEON_1_PATH, PIGEON_2_PATH, PIGEON_3_PATH

#  Classe que controle o personagem do jogador
class Player:
    def __init__(self, x, y):
        #  posição inicial do jogador
        self.x = x
        self.y = y

        #  velocidade do pombo na vertical
        self.velocity_y = 0

        #  adiciona as imagens do pombo para animação
        self.frames = [
            pygame.image.load(PIGEON_1_PATH).convert_alpha(),
            pygame.image.load(PIGEON_2_PATH).convert_alpha(),
            pygame.image.load(PIGEON_3_PATH).convert_alpha()
        ]

        #  redimensiona as imagens para ficarem com tamanho igual
        self.frames = [pygame.transform.scale(frame, (50, 40)) for frame in self.frames]

        #  controla a animação
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 6

        #  imagem atual do pombo
        self.image = self.frames[self.current_frame]
        self.rotated_image = self.image  #  rotaciona a imagem
        self.angle = 0


        #  hitbox para a colisão
        self.rect = self.image.get_rect(center=(self.x, self.y))


    #  função de pulo do personagem
    def jump(self):
        self.velocity_y = JUMP_STRENGTH

    #  atualiza a posição do personagem a cada frame do jogo
    def update(self):
        self.velocity_y += GRAVITY
        self.y += self.velocity_y

        self.animate()
        self.rotate()

        self.rect = self.rotated_image.get_rect(center=(self.x, self.y))

    #  controla a animação das asas do pombo
    def animate(self):
        self.animation_timer += 1

        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame += 1

            if self.current_frame >= len(self.frames):
                self.current_frame = 0

        self.image = self.frames[self.current_frame]

    #  Conforme a velocidade no eixo Y ele controla a rotação do pombo
    def rotate(self):
        self.angle = -self.velocity_y * 3

        if self.angle > 25:
            self.angle = 25
        if self.angle < -90:
            self.angle = -90

        self.rotated_image = pygame.transform.rotate(self.image, self.angle)

    #  desenha o personagem na tela
    def draw(self, screen):
        screen.blit(self.rotated_image, self.rect)



















