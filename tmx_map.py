import os
import pygame
import sys
import math
import time


white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 220, 80)
yellow = (255, 230, 0)
red = (255, 60, 60)
light_gray = (80, 80, 90)
gray = (40, 40, 50)
Tank_Background_color = (237, 236, 157)


pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.init()

monitor_size = pygame.display.get_desktop_sizes()[0]
width, height = monitor_size

screen = pygame.display.set_mode((width, height))
screen_rect = screen.get_rect()

pygame.display.set_caption("2D tank game")
clock = pygame.time.Clock()

info_font = pygame.font.Font(None, 36)
FPS = 60
players_speed = 10
lives_left = 3
amount_of_kills = 0
target_alive = True
last_shot_time = 0
shot_cooldown = 500
bullets = []
amount_of_bullets_shot = 0
bullet_speed = players_speed * 1.25

tank_path = os.path.join("photos", "tank_try3.png")
player_sprite_path_img = os.path.join("photos", "player_sprite.png")

players_img = pygame.image.load(tank_path).convert_alpha()
player = players_img.get_rect()

player_shot = pygame.image.load(player_sprite_path_img).convert_alpha()
gh = player_shot.get_rect()

gh.center = (width // 2, height // 2)
player.center = (width // 5, height // 2)

print("-----")
print(f"the screens length and width are: {height} , {width}")
print(f"players length are: {player.width} and length: {player.height} ")
print("-----")


def draw_vic():
    screen.blit(player_shot, gh)


def draw_player():
    # pygame.draw.rect(screen, white, player)
    screen.blit(players_img, player)


def draw_bullet():
    global amount_of_kills
    global target_alive
    for bullet_data in bullets[:]:
        bullet_rect = bullet_data[0]
        bullet_angle = bullet_data[1]

        bullet_rect.x += math.cos(bullet_angle) * bullet_speed
        bullet_rect.y += math.sin(bullet_angle) * bullet_speed

        if target_alive and bullet_rect.colliderect(gh):
            amount_of_kills += 1
            target_alive = False
            bullets.remove(bullet_data)

        if (bullet_rect.x < 0 or bullet_rect.x > width or
                bullet_rect.y < 0 or bullet_rect.y > height):
            bullets.remove(bullet_data)

    for bullet_data in bullets:
        pygame.draw.rect(screen, red, bullet_data[0])


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        keys = pygame.key.get_pressed()

        current_time = pygame.time.get_ticks()
        if keys[pygame.K_SPACE] and (current_time - last_shot_time > shot_cooldown):
            #target_alive = True #keeps spawning

            target_alive = True

            last_shot_time = current_time
            amount_of_bullets_shot += 1
            mouse_x, mouse_y = pygame.mouse.get_pos()
            dx, dy = mouse_x - player.centerx, mouse_y - player.centery
            b_angle = math.atan2(dy, dx)
            new_bullet = [pygame.Rect(player.centerx, player.centery, 5, 5), b_angle]
            bullets.append(new_bullet)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_x]:
        pygame.quit()
        exit()
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player.y -= 1 * players_speed
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player.y += 1 * players_speed
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.x -= 1 * players_speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.x += 1 * players_speed

    player.clamp_ip(screen_rect)

    screen.fill(Tank_Background_color)

    kills_text = info_font.render(f"Kills: {amount_of_kills}", True, black)
    bullets_text = info_font.render(f"Bullets Shot: {amount_of_bullets_shot}", True, black)

    screen.blit(kills_text, (20, 20))
    screen.blit(bullets_text, (150, 20))


    if target_alive:
        draw_vic()

    draw_bullet()
    draw_player()
    players_pos = (player.centerx, player.centery)
    pygame.display.update()
    clock.tick(FPS)