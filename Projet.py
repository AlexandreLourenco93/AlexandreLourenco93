import pygame
import random

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre de jeu
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Breakout")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PINK = (255,192, 203)

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
brick_rows = 6
brick_cols = 10
brick_padding = 10
brick_offset_top = 50
brick_offset_left = 35

# Initialisation de la raquette
paddle_x = (screen_width - paddle_width) // 2
paddle_y = screen_height - paddle_height - 10

# Initialisation de la balle
ball_x = screen_width // 2
ball_y = paddle_y - ball_radius
ball_dx = ball_speed_x
ball_dy = ball_speed_y

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

# Fonction pour dessiner les briques
def draw_bricks():
    for row in bricks:
        for brick in row:
            pygame.draw.rect(screen, RED, brick)

# Fonction pour vérifier les collisions de la balle avec les briques
def check_ball_brick_collisions():
    global ball_dy
    for row in bricks:
        for brick in row:
            if brick.colliderect(ball_rect):
                ball_dy *= -1
                row.remove(brick)
                return

# Fonction pour dessiner la raquette
def draw_paddle():
    pygame.draw.rect(screen, BLUE, (paddle_x, paddle_y, paddle_width, paddle_height))

# Fonction pour dessiner la balle
def draw_ball():
    pygame.draw.circle(screen, GREEN, (ball_x, ball_y), ball_radius)

# Boucle principale du jeu
run = True
while run:
    screen.fill(PINK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle_x > 0:
        paddle_x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle_x < screen_width - paddle_width:
        paddle_x += paddle_speed

    ball_x += ball_dx
    ball_y += ball_dy

    # Vérifier les collisions avec les murs
    if ball_x <= ball_radius or ball_x >= screen_width - ball_radius:
        ball_dx *= -1
    if ball_y <= ball_radius:
        ball_dy *= -1
    if ball_y >= screen_height - ball_radius:
        run = False  # La balle est tombée en bas, fin du jeu

    # Vérifier les collisions avec la raquette
    ball_rect = pygame.Rect(ball_x - ball_radius, ball_y - ball_radius, ball_radius * 2, ball_radius * 2)
    paddle_rect = pygame.Rect(paddle_x, paddle_y, paddle_width, paddle_height)
    if ball_rect.colliderect(paddle_rect):
        ball_dy *= -1

    # Vérifier les collisions avec les briques
    check_ball_brick_collisions()

    # Dessiner les éléments du jeu
    draw_paddle()
    draw_ball()
    draw_bricks()

    pygame.display.update()
    pygame.time.delay(10)

pygame.quit()
