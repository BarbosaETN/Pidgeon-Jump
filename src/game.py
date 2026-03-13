import pygame
from settings import WIDTH, HEIGHT, FPS, GROUND_HEIGHT, OBSTACLE_FREQUENCY, TITLE
from src.player import Player
from src.obstacle import Obstacle

MENU = "menu"
PLAYING: str = "playing"
GAME_OVER = "game_over"

class Game:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.running = True
        self.state = MENU

        self.player = Player(150, HEIGHT // 2)
        self.obstacles = []
        self.last_obstacle_time = 0
        self.score = 0

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if self.state == MENU and event.key == pygame.K_SPACE:
                    self.state = PLAYING
                    self.reset_game()

                elif self.state == PLAYING and event.key == pygame.K_SPACE:
                    self.player.jump()

                elif self.state == GAME_OVER and event.key == pygame.K_RETURN:
                    self.state = PLAYING
                    self.reset_game()

    def update(self):
        if self.state == PLAYING:
            self.player.update()

            current_time = pygame.time.get_ticks()

            if current_time - self.last_obstacle_time > OBSTACLE_FREQUENCY:
                self.spawn_obstacle()
                self.last_obstacle_time = current_time

            for obstacle in self.obstacles:
                obstacle.update()

                if not obstacle.passed and obstacle.x + obstacle.width < self.player.x:
                    obstacle.passed = True
                    self.score += 1

            self.obstacles = [obstacle for obstacle in self.obstacles if not obstacle.off_screen()]

            self.check_collisions()

    def draw(self):
        self.screen.fill((100, 180, 255))
        self.draw_ground()

        if self.state == MENU:
            self.draw_menu()

        elif self.state == PLAYING:
            self.draw_game()

        elif self.state == GAME_OVER:
            self.draw_game()
            self.draw_game_over()

        pygame.display.flip()

    def draw_ground(self):
        ground_rect = pygame.Rect(0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT)
        pygame.draw.rect(self.screen, (80,180, 80), ground_rect)

    def draw_menu(self):
        font = pygame.font.SysFont(None, 52)
        small_font = pygame.font.SysFont(None, 36)

        title = font.render("Pidgeon Jump", True, (255, 255, 255))
        instruction = small_font.render("Press SPACE to start", True, (255, 255, 255))

        self.screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 180))
        self.screen.blit(instruction, (WIDTH // 2 - instruction.get_width() // 2, 260))

    def draw_game(self):
        self.player.draw(self.screen)

        for obstacle in self.obstacles:
            obstacle.draw(self.screen)

        font = pygame.font.SysFont(None, 42)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (20, 20))

    def draw_game_over(self):
        font = pygame.font.SysFont(None, 52)
        small_font = pygame.font.SysFont(None, 36)

        game_over = font.render("GAME OVER", True, (255, 80, 80))
        restart = small_font.render("Press ENTER to restart", True, (255, 255, 255))

        self.screen.blit(game_over,(WIDTH // 2 - game_over.get_width() // 2, 220))
        self.screen.blit(restart, (WIDTH // 2 - restart.get_width() // 2, 280))

    def spawn_obstacle(self):
        obstacle = Obstacle(WIDTH + 50)
        self.obstacles.append(obstacle)

    def check_collisions(self):
        for obstacle in self.obstacles:
            if self.player.rect.colliderect(obstacle.top_rect) or self.player.rect.colliderect(obstacle.bottom_rect):
                self.state = GAME_OVER

        if self.player.rect.top <= 0:
            self.state = GAME_OVER

        if self.player.rect.bottom >= HEIGHT - GROUND_HEIGHT:
            self.state = GAME_OVER

    def reset_game(self):
        self.player = Player(150, HEIGHT // 2)
        self.obstacles = []
        self.last_obstacle_time = pygame.time.get_ticks()
        self.score = 0



