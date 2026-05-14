import pygame
import pytmx
from pytmx.util_pygame import load_pygame

# --- CONFIG ---
TMX_FILE = "cant_leave.tmx"
TILE_SIZE = 32
# SCREEN_WIDTH = 1280
# SCREEN_HEIGHT = 720
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
PLAYER_SPEED = 4


class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)

    def apply(self, x, y):
        return x + self.camera.x, y + self.camera.y

    def update(self, target):
        # center camera on player
        self.camera.x = -target.x + SCREEN_WIDTH // 2
        self.camera.y = -target.y + SCREEN_HEIGHT // 2



#
def draw_map(surface, tmx_data, camera):
    for layer in tmx_data.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            for x, y, gid in layer:
                tile = tmx_data.get_tile_image_by_gid(gid)
                if tile:
                    draw_pos = camera.apply(
                        x * tmx_data.tilewidth,
                        y * tmx_data.tileheight
                    )
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
#



def move_player(player, dx, dy, collision_rects):

    player.x += dx
    for rect in collision_rects:
        if player.colliderect(rect):
            if dx > 0:
                player.right = rect.left
            if dx < 0:
                player.left = rect.right


    player.y += dy
    for rect in collision_rects:
        if player.colliderect(rect):
            if dy > 0:
                player.bottom = rect.top
            if dy < 0:
                player.top = rect.bottom


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tiled Map + Collision")

    tmx_data = load_pygame(TMX_FILE)

    camera = Camera(
        tmx_data.width * TILE_SIZE,
        tmx_data.height * TILE_SIZE
    )

    collision_rects = get_collision_rects(tmx_data)


    player = pygame.Rect(100, 100, 28, 28)

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0

        if keys[pygame.K_a]:
            dx = -PLAYER_SPEED
        if keys[pygame.K_d]:
            dx = PLAYER_SPEED
        if keys[pygame.K_w]:
            dy = -PLAYER_SPEED
        if keys[pygame.K_s]:
            dy = PLAYER_SPEED
        if keys[pygame.K_q]:
            pygame.quit()

        move_player(player, dx, dy, collision_rects)
        camera.update(player)


        screen.fill((30, 30, 30))
        draw_map(screen, tmx_data, camera)



        pygame.draw.rect(
            screen,
            (255, 50, 50),
            (*camera.apply(player.x, player.y), player.width, player.height)
        )

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()