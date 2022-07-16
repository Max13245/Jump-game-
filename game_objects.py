import pygame 

WHITE = (255, 255, 255)
RED = (255, 0, 0)

class TILE:
    #types are: static, dynamic_hori, dynamic_vert
    def __init__(self, x, y, platform_length, screen_width, type = "static", max_high = None, min_high = None, max_wide = None, min_wide = None, layer_distance = None):
        self.x = x
        self.y = y
        self.height = 10
        self.tile_width = screen_width / 15
        self.width = self.tile_width * platform_length
        self.type = type
        self.max_high = max_high
        self.min_high = min_high
        self.max_wide = max_wide
        self.min_wide = min_wide

        if type == "dynamic_horizontal":
            self.speed = self.tile_width / 10
        elif type == "dynamic_vertical":
            self.speed = layer_distance / 25

    def move_verticaly(self):
        if self.y >= self.max_high:
            self.speed *= -1
        elif self.y <= self.min_high:
            self.speed *= -1
        
        self.y += self.speed

    def move_horizontaly(self):
        if self.x >= self.max_wide:
            self.speed *= -1
        elif self.x <= self.min_wide:
            self.speed *= -1
        
        self.x += self.speed

    def draw_tile(self, surface):
        if self.type == "dynamic_horizontal":
            self.move_horizontaly()
        elif self.type == "dynamic_vertical":
            self.move_verticaly()

        self.tile = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, WHITE, self.tile)