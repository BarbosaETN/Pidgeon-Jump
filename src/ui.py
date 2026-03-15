import pygame
from settings import WIDTH, WHITE, RED

class UI:
    def __init__(self):
        self.title_font = pygame.font.SysFont(None, 60)
        self.main_font = pygame.font.SysFont(None, 42)
        self.small_font = pygame.font.SysFont(None, 36)

    def draw_menu(self, screen, highscore):
        title = self.title_font.render("Pidgeon Jump", True, WHITE)
        instruction = self.small_font.render("Press SPACE to start", True, WHITE)
        highscore_text = self.small_font.render(f"Best Score: {highscore}", True, WHITE)

        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 170))
        screen.blit(instruction, (WIDTH // 2 - instruction.get_width() // 2, 250))
        screen.blit(highscore_text, (WIDTH // 2 - highscore_text.get_width() // 2, 300))

    def draw_hud(self, screen,score, highscore):
        score_text = self.main_font.render(f"Score: {score}", True, WHITE)
        highscore_text = self.main_font.render(f"Best: {highscore}", True, WHITE)

        screen.blit(score_text, (20, 20))
        screen.blit(highscore_text, (20, 60))

    def draw_game_over(self, screen, score, highscore):
        game_over = self.title_font.render("GAME OVER", True, RED)
        score_text = self.small_font.render(f"Score: {score}", True, WHITE)
        highscore_text = self.small_font.render(f"Best Score: {highscore}", True, WHITE)
        restart = self.small_font.render("Press ENTER to restart", True, WHITE)

        screen.blit(game_over, (WIDTH // 2 - game_over.get_width() // 2, 190))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 250))
        screen.blit(highscore_text, (WIDTH // 2 - highscore_text.get_width() // 2, 290))
        screen.blit(restart, (WIDTH // 2 - restart.get_width() // 2, 350))
