import pygame
import random

# Initialisation de pygame
pygame.init()

# Définition des couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Configuration de la fenêtre
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jeu de Ping-Pong")

# Configuration des paddles
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
PADDLE_SPEED = 7

# Configuration de la balle
BALL_SIZE = 15
BALL_SPEED_X, BALL_SPEED_Y = 5, 5

# Initialisation des scores
score_left = 0
score_right = 0
MAX_SCORE = 10

# Position initiale des paddles et de la balle
paddle_left = pygame.Rect(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
paddle_right = pygame.Rect(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

# Horloge pour contrôler la fréquence de rafraîchissement
clock = pygame.time.Clock()

# Fonction pour dessiner tous les éléments
def draw():
    window.fill(BLACK)
    pygame.draw.rect(window, WHITE, paddle_left)
    pygame.draw.rect(window, WHITE, paddle_right)
    pygame.draw.ellipse(window, WHITE, ball)
    pygame.draw.aaline(window, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    score_text = pygame.font.SysFont(None, 50).render(f"{score_left} - {score_right}", True, WHITE)
    window.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))

    pygame.display.flip()

# Fonction pour afficher GAME OVER
def display_game_over():
    window.fill(BLACK)
    game_over_text = pygame.font.SysFont(None, 75).render("GAME OVER", True, WHITE)
    window.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
    restart_text = pygame.font.SysFont(None, 50).render("Press R to Restart or Q to Quit", True, WHITE)
    window.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + game_over_text.get_height()))
    pygame.display.flip()

# Fonction pour déplacer les paddles
def move_paddles(keys):
    if keys[pygame.K_w] and paddle_left.top > 0:
        paddle_left.y -= PADDLE_SPEED
    if keys[pygame.K_s] and paddle_left.bottom < HEIGHT:
        paddle_left.y += PADDLE_SPEED
    if keys[pygame.K_UP] and paddle_right.top > 0:
        paddle_right.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and paddle_right.bottom < HEIGHT:
        paddle_right.y += PADDLE_SPEED

# Fonction pour déplacer la balle et gérer les collisions
def move_ball():
    global BALL_SPEED_X, BALL_SPEED_Y, score_left, score_right

    ball.x += BALL_SPEED_X
    ball.y += BALL_SPEED_Y

    if ball.top <= 0 or ball.bottom >= HEIGHT:
        BALL_SPEED_Y = -BALL_SPEED_Y

    if ball.colliderect(paddle_left) or ball.colliderect(paddle_right):
        BALL_SPEED_X = -BALL_SPEED_X

    if ball.left <= 0:
        score_right += 1
        reset_ball()
    if ball.right >= WIDTH:
        score_left += 1
        reset_ball()

# Fonction pour réinitialiser la balle au centre
def reset_ball():
    global BALL_SPEED_X, BALL_SPEED_Y
    ball.x, ball.y = WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2
    BALL_SPEED_X, BALL_SPEED_Y = random.choice([-5, 5]), random.choice([-5, 5])

# Fonction pour afficher le menu de démarrage et saisir les noms des joueurs
def start_menu():
    font = pygame.font.SysFont(None, 50)
    input_box1 = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 - 60, 400, 50)
    input_box2 = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 + 10, 400, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active1 = False
    active2 = False
    text1 = ''
    text2 = ''
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None, None, False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box1.collidepoint(event.pos):
                    active1 = not active1
                    active2 = False
                elif input_box2.collidepoint(event.pos):
                    active2 = not active2
                    active1 = False
                else:
                    active1 = False
                    active2 = False
                color = color_active if active1 or active2 else color_inactive
            if event.type == pygame.KEYDOWN:
                if active1:
                    if event.key == pygame.K_RETURN:
                        active1 = False
                    elif event.key == pygame.K_BACKSPACE:
                        text1 = text1[:-1]
                    else:
                        text1 += event.unicode
                elif active2:
                    if event.key == pygame.K_RETURN:
                        active2 = False
                    elif event.key == pygame.K_BACKSPACE:
                        text2 = text2[:-1]
                    else:
                        text2 += event.unicode
                if event.key == pygame.K_RETURN and text1 and text2:
                    done = True

        window.fill(BLACK)
        title_text = font.render("Enter Player Names", True, WHITE)
        window.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 2 - 150))
        
        txt_surface1 = font.render(text1, True, color)
        txt_surface2 = font.render(text2, True, color)

        width1 = max(400, txt_surface1.get_width() + 10)
        input_box1.w = width1
        window.blit(txt_surface1, (input_box1.x + 5, input_box1.y + 5))
        pygame.draw.rect(window, color, input_box1, 2)
        
        width2 = max(400, txt_surface2.get_width() + 10)
        input_box2.w = width2
        window.blit(txt_surface2, (input_box2.x + 5, input_box2.y + 5))
        pygame.draw.rect(window, color, input_box2, 2)

        pygame.display.flip()
        clock.tick(30)
    
    return text1, text2, True

# Boucle principale du jeu
def main():
    global score_left, score_right, ball, paddle_left, paddle_right
    running = True
    game_over = False

    player1, player2, start_game = start_menu()
    if not start_game:
        return

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        if not game_over:
            keys = pygame.key.get_pressed()
            move_paddles(keys)
            move_ball()
            
            draw()
            
            if score_left >= MAX_SCORE or score_right >= MAX_SCORE:
                game_over = True
                display_game_over()
        else:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                # Réinitialiser le jeu
                score_left = 0
                score_right = 0
                reset_ball()
                game_over = False
            elif keys[pygame.K_q]:
                running = False

        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
