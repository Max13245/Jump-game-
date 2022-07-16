import game_objects
import random

class MAP:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.layer_distance = screen_height / 10

        #is also in object file 
        self.tile_height = 10
        self.tile_width = screen_width / 15

        self.num_layer_tiles = self.screen_width / self.tile_width
        self.layers = []
        self.tiles = []

    def draw_map(self, surface):
        for tile in self.tiles:
            tile.draw_tile(surface)

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

    def create_tiles(self, screen_width, screen_height):
        if len(self.tiles) > 0:
            beneith_layer_y_pos = self.tiles[-1].y
        else:
            beneith_layer_y_pos = screen_height

        platform_beginnings, platform_endings = self.find_start_end(self.layers[-1])

        for pos in range(len(platform_beginnings)):
            tile_x_position = platform_beginnings[pos] * self.tile_width
            tile_y_position = beneith_layer_y_pos - self.layer_distance
            platform_length = platform_endings[pos] - platform_beginnings[pos] + 1
            tile = game_objects.TILE(tile_x_position, tile_y_position, platform_length, screen_width) 
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