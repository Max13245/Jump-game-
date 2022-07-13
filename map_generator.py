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
        self.layers = self.generate_map()
        self.tiles = []

    def draw_map(self, surface):
        for tile in self.tiles:
            tile.draw_tile(surface)

    def change_tile(self, layer, created_layer):
        chosen_layer = random.choice(["layer", "created_layer"]) 
        chosen_direction = random.choice(["hori", "vert"]) 

        if chosen_layer == "layer":
            if chosen_direction == "vert":
                (chosen_direction, "down")
            elif chosen_direction == "hori":
                pass
        elif chosen_layer == "created_layer":
            if chosen_direction == "vert":
                (chosen_direction, "up")
            elif chosen_direction == "hori":
                pass

    def is_posible_jump(self, layer, created_layer):
        #veranderen, want tile is miss niet altijd 1
        for indx, tile in enumerate(layer):
            if tile == 1:
                if layer[indx - 1] == 0 and indx != 0:
                    for num in created_layer[indx - 5, indx]:
                        if num == 1:
                            return layer, created_layer

                elif layer[indx + 1] == 0 and indx != 15:
                    for num in created_layer[indx, indx + 5]:
                        if num == 1:
                            return layer, created_layer
            
            self.change_tile(layer, created_layer)

    def create_tiles(self, screen_width):
        for layer_indx, layer in enumerate(self.layers):
            
            for indx, tile in enumerate(layer):
                #make it one tile 
                if tile != 0:
                    if tile == 1:
                        tile = game_objects.TILE(indx * self.tile_width, layer_indx * self.layer_distance, screen_width)
                    elif tile[0] == "hori":
                        pass
                    elif tile[0] == "vert":
                        pass
                    
                    self.tiles.append(tile)

    def adjust_list(self, platform_pos, platform_length, layer):
        #loc is miss niet goed, omdat indx niet hetzelfde is als loc
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
        platform_lengths = [random.randrange(1, max_tiles) for _ in range(num_platforms)] #not debuged yet!

        if sum(platform_lengths) >= 15:
            layer = [1 for _ in range(15)]
        else:
            for platform_length in platform_lengths:
                platform_pos = self.random_pos(layer, platform_length)
                layer = self.adjust_list(platform_pos, platform_length, layer)

        return layer

    def generate_map(self):
        num_layers = int(self.screen_height / self.layer_distance)
        layers = [self.generate_layer() for _ in range(num_layers)]
        
        return layers