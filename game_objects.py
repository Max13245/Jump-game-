import pygame 

WHITE = (255, 255, 255)

class TILE:
    #types are: static, dynamic_hori, dynamic_vert
    def __init__(self, x, y, tile_width, platform_length, tile_height, layer_distance, type, screen_width, screen_height):
        self.x = x
        self.y = y
        self.tile_width = tile_width
        self.width = self.tile_width * platform_length
        self.height = tile_height
        self.tile = pygame.Rect(self.x, self.y, self.width, self.height)
        self.type = type
        self.layer_distance = layer_distance
        self.screen_width = screen_width
        self.screen_height = screen_height

        if type == "dynamic_horizontal":
            self.speed = self.tile_width / 10
        elif type == "dynamic_vertical":
            self.speed = layer_distance / 25
            self.max_high = self.y
            self.min_high = self.y + 2 * self.layer_distance

    def screen_collision(self):
        if self.x <= 0:
            self.x = 0
            self.speed *= -1
        elif self.x + self.width >= self.screen_width:
            self.x = self.screen_width - self.width
            self.speed *= -1

    def tile_collision(self, all_tiles):
        if self.tile in all_tiles:
            all_tiles.remove(self.tile)
        collision_indx = pygame.Rect.collidelist(self.tile, all_tiles)

        if collision_indx > 0:
            if self.speed > 0:
                self.x = all_tiles[collision_indx].x - self.width
            elif self.speed < 0:
                self.x = all_tiles[collision_indx].x + all_tiles[collision_indx].width
            self.speed *= -1

    def move_verticaly(self):
        if self.y < self.max_high:
            self.y = self.max_high
            self.speed *= -1
        elif self.y > self.min_high:
            self.y = self.min_high
            self.speed *= -1
        
        self.y += self.speed

    def move_horizontaly(self, all_tiles):
        self.screen_collision()
        self.tile_collision(all_tiles)
        self.x += self.speed

    def draw_tile(self, surface, all_tiles):
        if self.type == "dynamic_horizontal":
            self.move_horizontaly(all_tiles)
        elif self.type == "dynamic_vertical":
            self.move_verticaly()

        self.tile = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, WHITE, self.tile)

class DISTANCE_BLOK:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.width = 10
        self.height = 10
        self.x = screen_width / 2 - self.width
        self.y = screen_height
        self.blok = pygame.Rect(self.x, self.y, self.width, self.height)

    def get_traveled_distance(self, player_y, player_height):
        return self.y - player_y - player_height

    def get_score(self):
        pass