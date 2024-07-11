#CREER PAR ALEXANDRE, KAGINTHAN, ABDOUL
import pygame
import os

# Initialisation de Pygame
pygame.init()

# Charger les sons et la musique
try:
    bounce_sound = pygame.mixer.Sound('bounce.wav')
    brick_break_sound = pygame.mixer.Sound('brick_break.wav')
    lose_sound = pygame.mixer.Sound('lose.wav')
    win_sound = pygame.mixer.Sound('win.wav')
    pygame.mixer.music.load('background_music.mp3')
except pygame.error as e:
    print(f"Erreur de chargement des sons : {e}")
    bounce_sound = None
    brick_break_sound = None
    lose_sound = None
    win_sound = None
    pygame.mixer.music = None

# Jouer la musique de fond en boucle avec volume réduit
if pygame.mixer.music:
    pygame.mixer.music.set_volume(0.2)  # Réglez le volume entre 0.0 et 1.0
    pygame.mixer.music.play(-1)

# Dimensions de la fenêtre de jeu
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Breakout")

# Charger les images de fond
try:
    background = pygame.image.load('background.png')
    background_hard = pygame.image.load('background_hard.png')
    menu_background = pygame.image.load('menu_background.png')
except pygame.error as e:
    print(f"Erreur de chargement de l'image de fond : {e}")
    background = None
    background_hard = None
    menu_background = None

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PINK = (255, 192, 203)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)  # Jaune foncé

# Police pour les messages
menu_font = pygame.font.SysFont("comicsansms", 72)
small_menu_font = pygame.font.SysFont("comicsansms", 36)
game_font = pygame.font.SysFont("comicsansms", 72)
small_game_font = pygame.font.SysFont("comicsansms", 36)

# Paramètres de la raquette
paddle_width = 100
paddle_height = 10
paddle_speed = 6

# Paramètres de la balle
ball_radius = 10
ball_speed_x = 4
ball_speed_y = -4

# Paramètres des briques
brick_width = 75
brick_height = 20
brick_rows_easy = 6
brick_rows_hard = 10
brick_cols = 10
brick_padding = 10
brick_offset_top = 50
brick_offset_left = 35

# Sons
def play_bounce_sound():
    if bounce_sound:
        bounce_sound.play()

def play_brick_break_sound():
    if brick_break_sound:
        brick_break_sound.play()

def play_lose_sound():
    if lose_sound:
        lose_sound.play()

def play_win_sound():
    if win_sound:
        win_sound.play()

def load_sounds():
    global bounce_sound, brick_break_sound, lose_sound, win_sound
    try:
        bounce_sound = pygame.mixer.Sound('bounce.wav')
        brick_break_sound = pygame.mixer.Sound('brick_break.wav')
        lose_sound = pygame.mixer.Sound('lose.wav')
        win_sound = pygame.mixer.Sound('win.wav')
    except pygame.error as e:
        print(f"Erreur de chargement des sons : {e}")
        bounce_sound = None
        brick_break_sound = None
        lose_sound = None
        win_sound = None

# Initialisation du jeu
def init_game(level):
    global paddle_x, paddle_y, ball_x, ball_y, ball_dx, ball_dy, bricks, game_over, game_won, lose_sound_played, level_difficulty

    # Initialisation de la raquette
    paddle_x = (screen_width - paddle_width) // 2
    paddle_y = screen_height - paddle_height - 10

    # Initialisation de la balle
    ball_x = screen_width // 2
    ball_y = paddle_y - ball_radius
    ball_dx = ball_speed_x
    ball_dy = ball_speed_y

    # Définir le nombre de rangées de briques en fonction du niveau
    level_difficulty = level
    brick_rows = brick_rows_easy if level == "easy" else brick_rows_hard

    # Création des briques
    bricks = []
    for row in range(brick_rows):
        brick_row = []
        for col in range(brick_cols):
            brick_x = brick_offset_left + col * (brick_width + brick_padding)
            brick_y = brick_offset_top + row * (brick_height + brick_padding)
            brick_rect = pygame.Rect(brick_x, brick_y, brick_width, brick_height)
            brick_row.append(brick_rect)
        bricks.append(brick_row)

    game_over = False
    game_won = False
    lose_sound_played = False  # Initialisation de lose_sound_played

# Fonction pour dessiner les briques
def draw_bricks():
    for row in bricks:
        for brick in row:
            pygame.draw.rect(screen, RED, brick)

# Fonction pour vérifier les collisions de la balle avec les briques
def check_ball_brick_collisions():
    global ball_dy, game_won
    for row in bricks:
        for brick in row:
            if brick.colliderect(ball_rect):
                play_brick_break_sound()
                ball_dy *= -1
                row.remove(brick)
                return

# Fonction pour dessiner la raquette
def draw_paddle():
    pygame.draw.rect(screen, RED, (paddle_x, paddle_y, paddle_width, paddle_height))

# Fonction pour dessiner la balle
def draw_ball():
    pygame.draw.circle(screen, ORANGE, (ball_x, ball_y), ball_radius)

# Fonction pour afficher le message de fin de jeu en cas de défaite
def draw_game_over_message():
    global lose_sound_played  # Déclaration de lose_sound_played comme globale
    if not lose_sound_played:
        play_lose_sound()
        lose_sound_played = True
    game_over_text = game_font.render("Game Over", True, ORANGE)
    screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2,
                                 screen_height // 2 - game_over_text.get_height() // 2))
    restart_text = small_game_font.render("Press R to Restart", True, ORANGE)
    screen.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2,
                               screen_height // 2 + game_over_text.get_height()))
    pygame.display.update()

# Fonction pour afficher le message de victoire
def draw_game_won_message():
    global game_won  # Déclaration de game_won comme globale
    if not game_won:
        play_win_sound()
        game_won = True
    game_won_text = game_font.render("You Win!", True, GREEN)
    screen.blit(game_won_text, (screen_width // 2 - game_won_text.get_width() // 2,
                                screen_height // 2 - game_won_text.get_height() // 2))
    restart_text = small_game_font.render("Press R to Restart", True, GREEN)
    screen.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2,
                               screen_height // 2 + game_won_text.get_height()))
    pygame.display.update()

# Fonction pour afficher le menu
def draw_menu():
    if menu_background:
        screen.blit(menu_background, (0, 0))
    else:
        screen.fill(BLUE)  # Fond bleu si aucune image de fond n'est chargée
    title_text = menu_font.render("Breakout", True, BLUE)  # Titre en blanc
    easy_text = small_menu_font.render("Press E for Easy", True, BLUE)  # Texte en blanc
    hard_text = small_menu_font.render("Press H for Hard", True, BLUE)  # Texte en blanc
    screen.blit(title_text, (50, 50))  # Position du titre en haut à gauche
    screen.blit(easy_text, (50, 150))  # Position du texte Easy
    screen.blit(hard_text, (50, 200))  # Position du texte Hard
    pygame.display.update()

# Boucle principale du jeu
clock = pygame.time.Clock()
run = True
level_selected = False
init_game("easy")  # Initialiser avec un niveau par défaut
load_sounds()  # Charger les sons au démarrage

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if not level_selected:
        draw_menu()
        if keys[pygame.K_e]:
            level_selected = True
            init_game("easy")
        elif keys[pygame.K_h]:
            level_selected = True
            init_game("hard")

    elif not game_over and not game_won:
        if keys[pygame.K_LEFT] and paddle_x > 0:
            paddle_x -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle_x < screen_width - paddle_width:
            paddle_x += paddle_speed

        ball_x += ball_dx
        ball_y += ball_dy

        # Vérifier les collisions avec les murs
        if ball_x <= ball_radius or ball_x >= screen_width - ball_radius:
            ball_dx *= -1
            play_bounce_sound()
        if ball_y <= ball_radius:
            ball_dy *= -1
            play_bounce_sound()
        if ball_y >= screen_height - ball_radius:
            game_over = True  # La balle est tombée en bas, fin du jeu
            draw_game_over_message()

        # Vérifier les collisions avec la raquette
        ball_rect = pygame.Rect(ball_x - ball_radius, ball_y - ball_radius, ball_radius * 2, ball_radius * 2)
        paddle_rect = pygame.Rect(paddle_x, paddle_y, paddle_width, paddle_height)
        if ball_rect.colliderect(paddle_rect):
            ball_dy *= -1
            play_bounce_sound()

        # Vérifier les collisions avec les briques
        check_ball_brick_collisions()

        # Vérifier si toutes les briques sont détruites
        if all(len(row) == 0 for row in bricks):
            game_won = True
            draw_game_won_message()

        # Dessiner tous les éléments
        if level_selected:
            if level_difficulty == "easy":
                if background:
                    screen.blit(background, (0, 0))
                else:
                    screen.fill(BLACK)
            elif level_difficulty == "hard":
                if background_hard:
                    screen.blit(background_hard, (0, 0))
                else:
                    screen.fill(BLACK)
            draw_bricks()
            draw_paddle()
            draw_ball()

    else:
        if keys[pygame.K_r]:
            level_selected = False
            init_game(level_difficulty)
            load_sounds()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
