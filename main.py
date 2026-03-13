import pygame
from settings import WIDTH, HEIGHT, FPS, TITLE
from src.game import Game

def main():
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    game = Game(screen, clock)
    game.run()

    pygame.quit()

if __name__ == '__main__':
    main()

