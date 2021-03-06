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

NUM_LAYER_TILES = 15
game_player = player.PLAYER(WIDTH, HEIGHT)
map = map_generator.MAP(WIDTH, HEIGHT, NUM_LAYER_TILES)

BACKGROUND_COLOR = (28, 7, 54)

def delete_passed_build_tiles():
    for tile in map.build_tiles:
        if tile.y >= HEIGHT:
            map.build_tiles.remove(tile)

def delete_passed_tiles():
    passed_tiles = 0
    for tile in map.tiles:
        if tile.type == "dynamic_vertical":
            if tile.max_high >= HEIGHT:
                passed_tiles += 1
        else:
            if tile.y >= HEIGHT:
                passed_tiles += 1

    del map.tiles[0: passed_tiles]
    num_passed_layers = 0

    for layer in map.layers:
        beginnings, endings = map.find_start_end(layer)
        num_tiles = len(beginnings)
        passed_tiles -= num_tiles

        if passed_tiles >= 0:
            num_passed_layers += 1
        else:
            break
    
    del map.layers[0: num_passed_layers]

def move_map():
    if game_player.y <= HEIGHT - HEIGHT / 2:
        if game_player.speed_vert < 0:
            for tile in map.all_tiles:
                tile.y -= game_player.speed_vert
                if tile.type == "dynamic_vertical":
                    tile.max_high -= game_player.speed_vert
                    tile.min_high -= game_player.speed_vert

            game_player.y -= game_player.speed_vert
    
    delete_passed_tiles()
    delete_passed_build_tiles()

def exicute_events(key_is_up, go_right, go_left):
    map.all_tiles = map.tiles + map.build_tiles
    print(len(map.tiles))
    print(len(map.layers))
    if len(map.layers) < int(HEIGHT / map.layer_distance) + 1:
        map.layers.append(map.generate_layer())
        map.create_tiles()

    map.draw_map(SCREEN)

    if go_right:
        game_player.walk("right", map.all_tiles)
    if go_left:
        game_player.walk("left", map.all_tiles)
    
    game_player.jump(map.all_tiles, jump = key_is_up)
    game_player.is_screen_collision()
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

            if event.key == pygame.K_w:
                map.build_tile("top", game_player)
            if event.key == pygame.K_a:
                map.build_barrier("left", game_player)
            if event.key == pygame.K_s:
                map.build_tile("bottom", game_player)
            if event.key == pygame.K_d:
                map.build_barrier("right", game_player)
            

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