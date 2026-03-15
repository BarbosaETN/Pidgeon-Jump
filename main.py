import pygame
from settings import WIDTH, HEIGHT, FPS, TITLE
from src.game import Game

#  função principal para iniciar o jogo
def main():
    pygame.init()
    pygame.mixer.init() #  inicializa o sistema de áudio

    screen = pygame.display.set_mode((WIDTH, HEIGHT)) #  cria a janela do jogo
    pygame.display.set_caption(TITLE) #  define o titulo da janela
    clock = pygame.time.Clock() #  relógio que controla o FPS do jogo

    game = Game(screen, clock) #  instância principal do jogo
    game.run() #  inicia o loop principal do jogo

    pygame.quit() #  finaliza o pygame ao fechar o jogo

if __name__ == '__main__': #  o jogo só é executado caso esse arquivo for rodado diretamente
    main()

