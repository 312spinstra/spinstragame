from .game_object import GameObject
from Primitives.spritesheet import Spritesheet

# Class that implements an icon
class Icon(GameObject):
    #------------------------------#
    # Constructor Function
    def __init__(self, sourceFile, centerX, centerY, x=0, y=0, width=16, height=16, scale=1, zIndex=0):
        super().__init__(zIndex=zIndex)
        self.centerX = centerX
        self.centerY = centerY
        self.iconSpritesheet = Spritesheet(sourceFile)
        self.icon = self.iconSpritesheet.get_sprite(x, y, width, height, scale)
    #------------------------------#

    #------------------------------#
    # Function that renders the icon on the screen
    def render(self, canvas):
        if self.icon != None:
            sprite_TLx = self.centerX - self.icon.get_width()//2
            sprite_TLy = self.centerY - self.icon.get_height()//2
            canvas.blit(self.icon, (sprite_TLx, sprite_TLy))
    #------------------------------#

    #------------------------------#
    # Function that updates the icon's location
    def updateLocation(self, newX, newY):
        self.centerX = newX
        self.centerY = newY
    #------------------------------#