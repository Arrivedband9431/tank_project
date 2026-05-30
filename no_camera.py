import math
import pygame
import pytmx
from pytmx.util_pygame import load_pygame
import os

# ---config---
TMX_FILE = "cant_leave.tmx"
TILE_SIZE = 32
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
PLAYER_SPEED = 4

# Bullet Configurations
last_shot_time = 0
shot_cooldown = 500  # 500 milliseconds = half a second
bullets = []
bullet_speed = PLAYER_SPEED*3

# colors setup
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 220, 80)
yellow = (255, 230, 0)
red = (255, 60, 60)

lives_left = 3

def draw_map(surface, tmx_data):
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    # Draw directly to the screen using world coordinates
                    draw_pos = (x * tmx_data.tilewidth, y * tmx_data.tileheight)
                    surface.blit(tile, draw_pos)


def get_collision_rects(tmx_data):
    rects = []
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer) and layer.name == "blocks":
            for x, y, gid in layer:
                if gid != 0:
                    rect = pygame.Rect(
                        x * TILE_SIZE,
                        y * TILE_SIZE,
                        TILE_SIZE,
                        TILE_SIZE
                    )
                    rects.append(rect)
    return rects


def move_player(player, dx, dy, collision_rects):
    player.x += dx
    for rect in collision_rects:
        if player.colliderect(rect):
            if dx > 0: player.right = rect.left
            if dx < 0: player.left = rect.right

    player.y += dy
    for rect in collision_rects:
        if player.colliderect(rect):
            if dy > 0: player.bottom = rect.top
            if dy < 0: player.top = rect.bottom


def update_and_draw_bullets(surface, map_width, map_height, collision_rects,player2):
    global lives_left
    for bullet_data in bullets[:]:
        bullet_rect = bullet_data[0]
        bullet_angle = bullet_data[1]

        bullet_rect.x += int(math.cos(bullet_angle) * bullet_speed)
        bullet_rect.y += int(math.sin(bullet_angle) * bullet_speed)

        hit_wall = False
        for rect in collision_rects:
            if bullet_rect.colliderect(rect):
                hit_wall = True
                break

        if hit_wall:
            bullets.remove(bullet_data)
            continue

        if bullet_rect.colliderect(player2):
            # add here other tank lives -1
            lives_left = lives_left - 1
            bullets.remove(bullet_data)
            continue

        if (bullet_rect.x < 0 or bullet_rect.x > map_width or
                bullet_rect.y < 0 or bullet_rect.y > map_height):
            bullets.remove(bullet_data)
            continue

        # Draw the bullet directly using its actual coordinates
        pygame.draw.rect(surface, black, bullet_rect)


def main():
    global last_shot_time
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tank Game By Yali")
    tmx_data = load_pygame(TMX_FILE)

    map_width = tmx_data.width * TILE_SIZE
    map_height = tmx_data.height * TILE_SIZE

    tank_path = os.path.join("photos", "tank_try4.png")
    players_img = pygame.image.load(tank_path).convert_alpha()

    tank_path1 = os.path.join("photos", "tank_try5.png")
    players_img2 = pygame.image.load(tank_path1).convert_alpha()

    collision_rects = get_collision_rects(tmx_data)

    player = players_img.get_rect(topleft=(50, 50))

    player2 = players_img2.get_rect(topleft=(map_width/2 , map_height/2))

    clock = pygame.time.Clock()
    running = True

    while running:
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # check if mouse had been clicked
        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()

        dx, dy = 0, 0
        if keys[pygame.K_a]:
            dx = -PLAYER_SPEED
        if keys[pygame.K_d]:
            dx = PLAYER_SPEED
        if keys[pygame.K_w]:
            dy = -PLAYER_SPEED
        if keys[pygame.K_s]:
            dy = PLAYER_SPEED
        if keys[pygame.K_x]:
            running = False
        if mouse_buttons[0]:  # mouse [0] is left click
            if current_time - last_shot_time >= shot_cooldown:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Calculate angle directly using player's actual center position
                angle = math.atan2(mouse_y - player.centery, mouse_x - player.centerx)

                # center bullet on player position
                new_bullet = pygame.Rect(player.centerx - 4, player.centery - 4, 8, 8)
                bullets.append([new_bullet, angle])
                print(bullets)
                last_shot_time = current_time

        # logic updates
        move_player(player, dx, dy, collision_rects)

        # moving the second player
        move_player(player2, -dx, -dy, collision_rects)
        # -------------------------


        # drawing the map
        screen.fill((30, 30, 30))
        draw_map(screen, tmx_data)

        # pass collision list down to handle bullet wall deletion
        update_and_draw_bullets(screen, map_width, map_height, collision_rects,player2)

        # draw player directly to screen
        screen.blit(players_img, player) # drawing player 1
        if lives_left > 0:
            screen.blit(players_img2, player2) #drawing player 2
        else:
            print("----------------------")
            print("player1 won the game")
            print("----------------------")
            pygame.quit()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
