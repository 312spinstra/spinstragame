import pygame
import math

# Class that implements a Spritesheet Interface
class Spritesheet:
    #------------------------------#
    # Constructor Function
    def __init__(self, filename):
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename).convert()
    #------------------------------#

    #------------------------------#
    # Function that returns a specified section of a spritesheet
    def get_sprite(self, x, y, width, height, scale=None):
        sprite = pygame.Surface((width, height)).convert()
        color_key = self.sprite_sheet.get_at((0, 0))
        sprite.blit(self.sprite_sheet, (0,0), (x, y, width, height))
        sprite.set_colorkey((0,0,0))
        if scale != None:
            sprite = pygame.transform.scale(sprite, (math.ceil(width * scale), math.ceil(height * scale)))
        return sprite
    #------------------------------#