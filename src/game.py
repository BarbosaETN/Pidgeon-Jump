import pygame
from settings import ( WIDTH,
                       HEIGHT,
                       FPS,
                       GROUND_HEIGHT,
                       OBSTACLE_FREQUENCY,
                       BACKGROUND_PATH,
                       FLAP_SOUND_PATH,
                       HIT_SOUND_PATH,
                       SCORE_SOUND_PATH,
                       MUSIC_PATH,
                       BG_SPEED,
                       HIGHSCORE_FILE)
from src.player import Player
from src.obstacle import Obstacle
from src.ui import UI

#  possíveis estados do jogo
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
        #  loop principal do jogo
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

            #  detecta as teclas pressionadas
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
        #  atualiza a lógica principal enquanto estiver jogando
        if self.state == PLAYING:
            self.bg_x -= self.bg_speed #  move a imagem de fundo para a esquerda

            if self.bg_x <= -WIDTH:
                self.bg_x = 0

            self.player.update()

            current_time = pygame.time.get_ticks()

            #  condição para gerar objetos em intervalos definidos
            if current_time - self.last_obstacle_time > OBSTACLE_FREQUENCY:
                self.spawn_obstacle()
                self.last_obstacle_time = current_time

            for obstacle in self.obstacles:
                obstacle.update()

                # verifica se o jogador passou pelo obstaculo
                if not obstacle.passed and obstacle.x + obstacle.width < self.player.x:
                    obstacle.passed = True
                    self.score += 1
                    self.score_sound.play()

                    #  atualiza o sistema de pontuação cada vez que passa entre os obstáculos
                    if self.score > self.highscore:
                        self.highscore = self.score
                        self.save_highscore()

            self.obstacles = [obstacle for obstacle in self.obstacles if not obstacle.off_screen()]

            self.check_collisions()

    def draw(self):
        #  desenha o fundo em duas posições para gerar rolagem contínua
        self.screen.blit(self.background, (self.bg_x, 0))
        self.screen.blit(self.background, (self.bg_x + WIDTH, 0))
        self.draw_ground()  #  desenha o chão do jogo

        #  escolhe o que vai ser mostrado com base no estado do jogo atual
        if self.state == MENU:
            self.ui.draw_menu(self.screen, self.highscore)

        elif self.state == PLAYING:
            self.draw_game()

        elif self.state == GAME_OVER:
            self.draw_game()
            self.ui.draw_game_over(self.screen, self.score, self.highscore)

        pygame.display.flip()

    def draw_ground(self):
        #  faz a criação do retângulo do chão e desenha na tela
        ground_rect = pygame.Rect(0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT)
        pygame.draw.rect(self.screen, (128,128, 128), ground_rect)

    def draw_game(self):
        self.player.draw(self.screen) #  desenha o jogador na tela

        for obstacle in self.obstacles: #  desenha todos os obstáculos ativos
            obstacle.draw(self.screen)

        #  desenha um HUD com score e recorde
        self.ui.draw_hud(self.screen, self.score, self.highscore)

    def spawn_obstacle(self):
        #  cria obstáculos fora da tela
        obstacle = Obstacle(WIDTH + 50)
        self.obstacles.append(obstacle)

    def check_collisions(self):
        collided = False

        #  verifica colisão do jogador com os obstáculos
        for obstacle in self.obstacles:
            if self.player.rect.colliderect(obstacle.top_rect) or self.player.rect.colliderect(obstacle.bottom_rect):
                collided = True

        #  verifica colisão do jogador com o topo da tela
        if self.player.rect.top <= 0:
            collided = True

        #  verifica colisão com o chão da tela
        if self.player.rect.bottom >= HEIGHT - GROUND_HEIGHT:
            collided = True

        #  se houver colisão toca o som e muda a tela para GAME OVER
        if collided:
            if not self.hit_played:
                self.hit_sound.play()
                self.hit_played = True
            self.state = GAME_OVER

    def reset_game(self):
        self.player = Player(150, HEIGHT // 2) #  volta o jogador na posição inicial
        self.obstacles = [] #  remove os obstáculos do jogo anterior
        self.last_obstacle_time = pygame.time.get_ticks() #  reinicia o temporizador de criação dos obstáculos
        self.score = 0
        self.hit_played = False

    def load_highscore(self):
        #  tenta carregar o recorde salvo em um arquivo
        try:
            with open(HIGHSCORE_FILE, 'r') as file:
                return int(file.read())
        except (FileNotFoundError, ValueError):
            #  se o arquivo não existir, retorna 0
            return 0

    def save_highscore(self):
        #  salva o recorde atual em um arquivo
        with open(HIGHSCORE_FILE, 'w') as file:
            file.write(str(self.highscore))
