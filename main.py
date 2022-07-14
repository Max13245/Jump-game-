import pygame
import sys
import player
import math
import map_generator

pygame.init()

WIDTH, HEIGHT = 750, 750
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()
pygame.display.set_caption("Wuble jump")

PLAYER_WIDTH, PLAYER_HEIGHT = math.floor(WIDTH / 25), math.floor(HEIGHT / 25)
PLAYER_COLOR = (255, 255, 255)

START_POSITION = (WIDTH / 2 - PLAYER_WIDTH / 2, HEIGHT - PLAYER_HEIGHT)
game_player = player.PLAYER(START_POSITION[0], START_POSITION[1], PLAYER_WIDTH, PLAYER_HEIGHT, HEIGHT)

map = map_generator.MAP(WIDTH, HEIGHT)
map.create_tiles(WIDTH)

BACKGROUND_COLOR = (28, 7, 54)

def move_map():
    if game_player.y <= HEIGHT - HEIGHT / 2:
        for tile in map.tiles:
            tile.y -= game_player.speed_vert

            if tile.y >= HEIGHT:
                del tile 

        game_player.y -= game_player.speed_vert

def exicute_events(key_is_up, go_right, go_left):
    map.draw_map(SCREEN)

    if go_right:
        game_player.walk("right", map.tiles)
    if go_left:
        game_player.walk("left", map.tiles)
    
    game_player.jump(map.tiles, jump = key_is_up)
    game_player.is_screen_collision(WIDTH)
    move_map()

    game_player.draw_player(SCREEN, PLAYER_COLOR)

def event_loop(key_is_up, go_right, go_left):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                key_is_up = True
            if event.key == pygame.K_RIGHT:
                go_right = True
            if event.key == pygame.K_LEFT:
                go_left = True
            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                go_right = False
            if event.key == pygame.K_LEFT:
                go_left = False   
    
    exicute_events(key_is_up, go_right, go_left)
    return go_right, go_left

def main():
    go_right = False
    go_left = False

    while True:
        key_is_up = False
        SCREEN.fill(BACKGROUND_COLOR)
        go_right, go_left = event_loop(key_is_up, go_right, go_left)
        pygame.display.update()
        CLOCK.tick(60)

if __name__ == "__main__":
    main()