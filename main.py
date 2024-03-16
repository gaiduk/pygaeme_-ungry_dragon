import pygame, random

pygame.init()

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 400
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

pygame.display.set_caption("Hungry Dragon Game")

# Set FPS and clock
FPS = 60
clock = pygame.time.Clock()

# Set game values
PLAYER_STARTING_LIVES = 3
PLAYER_VELOCITY = 6
COIN_STARTING_VELOCITY = 9
COIN_ACCELERATION = 0.5
BUFFER_DISTANCE = 100
POINTS_TO_WIN = 50

score = 0
player_lives = PLAYER_STARTING_LIVES
coin_velocity = COIN_STARTING_VELOCITY

# Set colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARKGREEN = (15, 60, 15)
GREEN = (0, 255, 0)

# Set fonts
font = pygame.font.Font("assets/AttackGraffiti.ttf", 30)
win_font = pygame.font.Font("assets/AttackGraffiti.ttf", 50)

# Set text
score_text = font.render("Score : " + str(score), True, GREEN, DARKGREEN)
score_rect = score_text.get_rect()
score_rect.topleft = (10, 10)

title_text = font.render("Hungry Dragon Game", True, GREEN, BLACK)
title_rect = title_text.get_rect()
title_rect.centerx = WINDOW_WIDTH//2
title_rect.y = 10

live_text = font.render("Lives : " + str(player_lives), True, GREEN, DARKGREEN)
live_rect = live_text.get_rect()
live_rect.topright = (WINDOW_WIDTH - 10, 10)

game_over_text = font.render("GAMEOVER", True, GREEN, DARKGREEN)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

win_text = win_font.render("YOU WIN", True, WHITE, GREEN)
win_text_rect = win_text.get_rect()
win_text_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2)

continue_text = font.render("Press any kay to try again", True, GREEN, DARKGREEN)
continue_rect = continue_text.get_rect()
continue_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 32)

# Set audio
coin_sound = pygame.mixer.Sound("assets/coin_sound.wav")
miss_sound = pygame.mixer.Sound("assets/miss_sound.wav")
miss_sound.set_volume(0.1)
pygame.mixer.music.load("assets/ftd_background_music.wav")

# Set img
player_img = pygame.image.load("assets/dragon_right.png")
player_rect = player_img.get_rect()
player_rect.x = 32
player_rect.centery = WINDOW_HEIGHT//2

coin_img = pygame.image.load("assets/coin.png")
coin_rect = coin_img.get_rect()
coin_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
coin_rect.y = random.randint(64, WINDOW_HEIGHT - 32)

# main game loop
pygame.mixer.music.play(-1, 0.0)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # User control
    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP] and player_rect.top > 64:
        player_rect.y = player_rect.y - PLAYER_VELOCITY
    if keys[pygame.K_DOWN] and player_rect.bottom < WINDOW_HEIGHT:
        player_rect.y = player_rect.y + PLAYER_VELOCITY

    # move the coin
    if coin_rect.x < 0:
        player_lives -= 1
        miss_sound.play()
        coin_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
        coin_rect.y = random.randint(64, WINDOW_HEIGHT - 32)
    else:
        coin_rect.x -= coin_velocity

    # check collision
    if player_rect.colliderect(coin_rect):
        score += 1
        coin_sound.play()
        coin_velocity += COIN_ACCELERATION

        coin_rect.x = WINDOW_WIDTH + BUFFER_DISTANCE
        coin_rect.y = random.randint(64, WINDOW_HEIGHT - 32)

    # Update texts
    score_text = font.render("Score : " + str(score), True, GREEN, DARKGREEN)
    live_text = font.render("Lives : " + str(player_lives), True, GREEN, DARKGREEN)

    # check for game over
    if player_lives <= 0:
        display_surface.blit(game_over_text, game_over_rect)
        display_surface.blit(continue_text, continue_rect)
        pygame.display.update()

        # pause the game until player pressed key
        pygame.mixer.music.stop()
        is_paused = True

        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    score = 0
                    player_lives = PLAYER_STARTING_LIVES
                    player_rect.y = WINDOW_HEIGHT//2
                    coin_velocity = COIN_STARTING_VELOCITY
                    pygame.mixer.music.play(-1, 0.0)
                    is_paused = False
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False

    # check for WIN
    if score >= POINTS_TO_WIN:
        display_surface.blit(win_text, win_text_rect)
        display_surface.blit(score_text, score_rect)
        pygame.display.update()

        # pause the game until player pressed key
        pygame.mixer.music.stop()
        is_paused = True

        while is_paused:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    score = 0
                    player_lives = PLAYER_STARTING_LIVES
                    player_rect.y = WINDOW_HEIGHT // 2
                    coin_velocity = COIN_STARTING_VELOCITY
                    pygame.mixer.music.play(-1, 0.0)
                    is_paused = False
                if event.type == pygame.QUIT:
                    is_paused = False
                    running = False

    # Fill display
    display_surface.fill(BLACK)

    # Blit objects
    display_surface.blit(score_text, score_rect)
    display_surface.blit(title_text, title_rect)
    display_surface.blit(live_text, live_rect)
    pygame.draw.line(display_surface, WHITE, (0, 64), (WINDOW_WIDTH, 64), 2)

    display_surface.blit(player_img, player_rect)
    display_surface.blit(coin_img, coin_rect)

    # update display and tick the clock
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()