import pygame
from settings import WIDTH, HEIGHT, FPS, GROUND_HEIGHT, OBSTACLE_FREQUENCY, TITLE, BACKGROUND_PATH, FLAP_SOUND_PATH, HIT_SOUND_PATH, SCORE_SOUND_PATH, MUSIC_PATH, BG_SPEED, HIGHSCORE_FILE
from src.player import Player
from src.obstacle import Obstacle
from src.ui import UI

MENU = "menu"
PLAYING: str = "playing"
GAME_OVER = "game_over"

class Game:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.running = True
        self.state = MENU
        self.ui = UI()

        self.player = Player(150, HEIGHT // 2)
        self.obstacles = []
        self.last_obstacle_time = 0
        self.score = 0
        self.highscore = self.load_highscore()
        self.hit_played = False

        #  adicionando cena de fundo ao jogo
        self.background = pygame.image.load(BACKGROUND_PATH).convert()
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT - GROUND_HEIGHT))

        self.bg_x = 0
        self.bg_speed = BG_SPEED

        #  sons de pulo, score e de dano
        self.flap_sound = pygame.mixer.Sound(FLAP_SOUND_PATH)
        self.score_sound = pygame.mixer.Sound(SCORE_SOUND_PATH)
        self.hit_sound = pygame.mixer.Sound(HIT_SOUND_PATH)

        #  ajuste de volume para os audios
        self.flap_sound.set_volume(0.4)
        self.score_sound.set_volume(0.5)
        self.hit_sound.set_volume(0.6)


        #  adiciona a música no jogo
        pygame.mixer.music.load(MUSIC_PATH)
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()

    #  eventos para controle do personagem e do menu
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
                    self.flap_sound.play()

                elif self.state == GAME_OVER and event.key == pygame.K_RETURN:
                    self.state = PLAYING
                    self.reset_game()

    def update(self):
        if self.state == PLAYING:
            self.bg_x -= self.bg_speed

            if self.bg_x <= -WIDTH:
                self.bg_x = 0

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
                    self.score_sound.play()

                    if self.score > self.highscore:
                        self.highscore = self.score
                        self.save_highscore()

            self.obstacles = [obstacle for obstacle in self.obstacles if not obstacle.off_screen()]

            self.check_collisions()

    def draw(self):
        self.screen.blit(self.background, (self.bg_x, 0))
        self.screen.blit(self.background, (self.bg_x + WIDTH, 0))
        self.draw_ground()

        if self.state == MENU:
            self.ui.draw_menu(self.screen, self.highscore)

        elif self.state == PLAYING:
            self.draw_game()

        elif self.state == GAME_OVER:
            self.draw_game()
            self.ui.draw_game_over(self.screen, self.score, self.highscore)

        pygame.display.flip()

    def draw_ground(self):
        ground_rect = pygame.Rect(0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT)
        pygame.draw.rect(self.screen, (80,180, 80), ground_rect)

    def draw_game(self):
        self.player.draw(self.screen)

        for obstacle in self.obstacles:
            obstacle.draw(self.screen)

        self.ui.draw_hud(self.screen, self.score, self.highscore)

    def spawn_obstacle(self):
        obstacle = Obstacle(WIDTH + 50)
        self.obstacles.append(obstacle)

    def check_collisions(self):
        collided = False

        for obstacle in self.obstacles:
            if self.player.rect.colliderect(obstacle.top_rect) or self.player.rect.colliderect(obstacle.bottom_rect):
                collided = True

        if self.player.rect.top <= 0:
            collided = True

        if self.player.rect.bottom >= HEIGHT - GROUND_HEIGHT:
            collided = True

        if collided:
            if not self.hit_played:
                self.hit_sound.play()
                self.hit_played = True
            self.state = GAME_OVER

    def reset_game(self):
        self.player = Player(150, HEIGHT // 2)
        self.obstacles = []
        self.last_obstacle_time = pygame.time.get_ticks()
        self.score = 0
        self.hit_played = False

    def load_highscore(self):
        try:
            with open(HIGHSCORE_FILE, 'r') as file:
                return int(file.read())
        except (FileNotFoundError, ValueError):
            return 0

    def save_highscore(self):
        with open(HIGHSCORE_FILE, 'w') as file:
            file.write(str(self.highscore))
