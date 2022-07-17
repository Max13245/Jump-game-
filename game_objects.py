import pygame 

WHITE = (255, 255, 255)

class TILE:
    #types are: static, dynamic_hori, dynamic_vert
    def __init__(self, x, y, tile_width, platform_length, tile_height, screen_width, screen_height, type = "static", layer_distance = None):
        self.x = x
        self.y = y
        self.tile_width = tile_width
        self.width = self.tile_width * platform_length
        self.height = tile_height
        self.type = type
        self.tile = pygame.Rect(self.x, self.y, self.width, self.height)

        if type == "dynamic_horizontal":
            self.speed = self.tile_width / 10
        elif type == "dynamic_vertical":
            self.speed = layer_distance / 25

    def move_verticaly(self, min_high, max_high):
        if self.y >= max_high:
            self.speed *= -1
        elif self.y <= min_high:
            self.speed *= -1
        
        self.y += self.speed

    def move_horizontaly(self, min_wide, max_wide):
        if self.x >= max_wide:
            self.speed *= -1
        elif self.x <= min_wide:
            self.speed *= -1
        
        self.x += self.speed

    def draw_tile(self, surface):
        if self.type == "dynamic_horizontal":
            self.move_horizontaly()
        elif self.type == "dynamic_vertical":
            self.move_verticaly()

        self.tile = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, WHITE, self.tile)