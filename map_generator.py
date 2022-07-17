import pygame
import game_objects
import random

class MAP:
    def __init__(self, screen_width, screen_height, num_layer_tiles):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.layer_distance = screen_height / 10
        self.num_layer_tiles = num_layer_tiles
        self.tile_width = screen_width / self.num_layer_tiles
        self.tile_height = screen_height / 75
        self.layers = []
        self.tiles = []
        self.build_tiles = []
        self.all_tiles = None

    def get_tile_rects(self, tile_objects):
        tiles = [tile_object.tile for tile_object in tile_objects]
        return tiles

    def tiles_colliding(self):
        all_tiles = self.get_tile_rects(self.all_tiles)
        for build_tile in self.build_tiles:
            tile_collindex = pygame.Rect.collidelist(build_tile.tile, all_tiles)

            if tile_collindex > 0:
                tile = all_tiles[tile_collindex]
                if build_tile.tile == tile:
                    continue

                self.build_tiles.remove(build_tile)

    def draw_map(self, surface):
        self.tiles_colliding()
        for tile in self.tiles:
            tile.draw_tile(surface, self.get_tile_rects(self.all_tiles))
        for tile in self.build_tiles:
            tile.draw_tile(surface, None) 

    def build_tile(self, side, player):
        if side == "top":
            x_pos = (player.x + player.width / 2) - self.tile_width / 2
            y_pos = player.y - self.tile_height
        elif side == "bottom":
            x_pos = (player.x + player.width / 2) - self.tile_width / 2
            y_pos = player.y + player.height
        
        tile = game_objects.TILE(x_pos, y_pos, self.tile_width, 1, self.tile_height, self.layer_distance, "static", self.screen_width, self.screen_height)
        self.build_tiles.append(tile)

    def build_barrier(self, side, player):
        distance_to_player = 10
        if side == "left":
            x_pos = player.x - self.tile_height - distance_to_player
            y_pos = player.y + player.height - player.height
        elif side == "right":
            x_pos = player.x + player.width + distance_to_player
            y_pos = player.y + player.height - player.height

        tile = game_objects.TILE(x_pos, y_pos, self.tile_height, 1, player.height, self.tile_width, self.layer_distance, self.screen_width)
        self.build_tiles.append(tile)

    def random_moving_tiles(self):
        if random.randint(1, 10) == 1:
            type = random.choice(["dynamic_horizontal", "dynamic_vertical"])
        else:
            type = "static"
        
        return type
        

    def find_start_end(self, tile_positions):
        platform_beginnings = []
        platform_endings = []

        for tile_indx in range(len(tile_positions)):
            if tile_indx == len(tile_positions) - 1 and tile_positions[-1] == 1:
                platform_endings.append(tile_indx)
                break

            two_part_list = tile_positions[tile_indx: tile_indx + 2]
            if tile_indx == 0 and two_part_list[0] == 1:
                platform_beginnings.append(tile_indx)
                if two_part_list == [1, 0]:
                    platform_endings.append(tile_indx)
            elif two_part_list == [0, 1]:
                platform_beginnings.append(tile_indx + 1)
            elif two_part_list == [1, 0]:
                platform_endings.append(tile_indx)
        
        return platform_beginnings, platform_endings

    def create_tiles(self):
        if len(self.tiles) > 0:
            beneith_layer_y_pos = self.tiles[-1].y
        else:
            beneith_layer_y_pos = self.screen_height

        platform_beginnings, platform_endings = self.find_start_end(self.layers[-1])

        for pos in range(len(platform_beginnings)):
            tile_x_position = platform_beginnings[pos] * self.tile_width
            tile_y_position = beneith_layer_y_pos - self.layer_distance
            platform_length = platform_endings[pos] - platform_beginnings[pos] + 1
            type = self.random_moving_tiles()
            tile = game_objects.TILE(tile_x_position, tile_y_position, self.tile_width, platform_length, self.tile_height, self.layer_distance, type, self.screen_width, self.screen_width) 
            self.tiles.append(tile)

    def adjust_list(self, platform_pos, platform_length, layer):
        zipped = zip([loc for loc in range(platform_pos, platform_pos + platform_length)], [1 for _ in range(platform_length)])
        
        for pos, length in zipped:
            layer[pos] = length

        return layer

    def get_posible_positions(self, layer, platform_length):
        posible_positions = []

        for indx, tile in enumerate(layer):
            if tile == 0:
                posible_positions.append(indx)
            if len(layer) - platform_length == indx:
                break
        
        return posible_positions

    def random_pos(self, layer, platform_length):
        posible_positions = self.get_posible_positions(layer, platform_length)
        random_pos = random.choice(posible_positions)
        return random_pos

    def generate_layer(self):
        num_platforms = random.randrange(2, 4)
        max_tiles = 12 / num_platforms #- 1 #doen als verder in map (later -2, niet meer)
        platform_lengths = []
        layer = [0 for _ in range(15)]
        platform_lengths = [random.randrange(1, max_tiles) for _ in range(num_platforms)]

        if sum(platform_lengths) >= 15:
            layer = [1 for _ in range(15)]
        else:
            for platform_length in platform_lengths:
                platform_pos = self.random_pos(layer, platform_length)
                layer = self.adjust_list(platform_pos, platform_length, layer)

        return layer