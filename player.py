import pygame
import math

GRAVITY = 1

class PLAYER:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.width = math.floor(screen_width / 25)
        self.height = math.floor(screen_height / 25)
        self.x = screen_width / 2 - self.width / 2
        self.y = screen_height - self.height
        self.jump_height = 14  #14
        self.speed_hori = 6    #6
        self.speed_vert = 0
        self.on_platform = False

    def get_tile_rects(self, tile_objects):
        tiles = [tile_object.tile for tile_object in tile_objects]
        return tiles

    def is_platform_collision(self, tile_objects, direction, K_UP_down = False):
        tiles = self.get_tile_rects(tile_objects)
        collision_indx = pygame.Rect.collidelist(self.player, tiles)

        if collision_indx != -1:
            if direction == "left":
                reposition = tiles[collision_indx].x + tiles[collision_indx].width
                self.x = reposition
            elif direction == "right":
                reposition = tiles[collision_indx].x - self.width
                self.x = reposition
            elif direction == "up":
                reposition = tiles[collision_indx].y + tiles[collision_indx].height
                self.y = reposition
                self.speed_vert = 0
            elif direction == "down":
                reposition = tiles[collision_indx].y - self.height
                self.y = reposition 
                self.speed_vert = 0
                self.on_platform = True
                self.jump(tile_objects, jump = K_UP_down)

    def is_screen_collision(self):
        if self.x <= 0:
            self.x = 0
        elif self.x + self.width >= self.screen_width:
            self.x = self.screen_width - self.width

        if self.y + self.height >= self.screen_height:
            self.y = self.screen_height - self.height

    def is_on_ground(self):
        if self.y == self.screen_height - self.height:
            return True
        return self.on_platform

    def walk(self, direction, tile_objects):
        if direction == "left":
            self.x -= self.speed_hori
        elif direction == "right":
            self.x += self.speed_hori

        self.on_platform = False
        
        self.player = pygame.Rect(self.x, self.y, self.width, self.height)
        self.is_platform_collision(tile_objects, direction)

    #always called in event loop
    #somewhere set speed_vert to zero if standing on ground
    def jump(self, tile_objects, jump = False):
        if self.is_on_ground():
            if jump:
                self.speed_vert -= self.jump_height
            else:
                self.speed_vert = 0
        else:
            self.speed_vert += GRAVITY 

        self.y += self.speed_vert
        self.player = pygame.Rect(self.x, self.y, self.width, self.height)

        if self.speed_vert > 0:
            self.is_platform_collision(tile_objects, "down", K_UP_down = jump)
        elif self.speed_vert < 0:
            self.on_platform = False
            self.is_platform_collision(tile_objects, "up")

    def draw_player(self, surface, color):
        self.player = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(surface, color, self.player)