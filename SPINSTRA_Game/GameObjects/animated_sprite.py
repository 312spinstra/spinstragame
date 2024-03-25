import os
import pygame
from .game_object import GameObject
from Primitives.spritesheet import Spritesheet
from constants import *
from utils import loadJSONFile

# Class that implements an animated sprite
class AnimatedSprite(GameObject):
    #------------------------------#
    # Constructor Function
    def __init__(self, sourceDir, animationData, startingAnimation="Idle", scaleFactor=1, mirror=False, centerX=0, centerY=0, parentID="", sendSignals=False, zIndex=0):
        super().__init__(zIndex=zIndex)
        self.sourceDir = sourceDir
        self.animationData = animationData
        self.selectedAnimation = None
        self.currentAnimationSpritesheet = None
        self.currentAnimationFrames = None
        self.currentAnimationScale = None
        self.currentAnimationFPS = None
        self.currentFrame = None
        self.modFactor = 1
        self.runOnce = False
        self.fallbackToStartingAnimation = False
        self.currentAnimationFrameIndex = -1
        self.scaleFactor = scaleFactor
        self.mirror = mirror
        self.centerX = centerX
        self.centerY = centerY
        self.parentID = parentID
        self.startingAnimation = startingAnimation
        self.sendSignals = sendSignals
        self.selectAnimation(startingAnimation)
    #------------------------------#

    #------------------------------#
    # Function that updates the sprite
    def update(self, frameCounter, deltaTime):
        self.progressCurrentAnimation(frameCounter)
        return
    #------------------------------#

    #------------------------------#
    # Function that renders the sprite on the screen
    def render(self, canvas):
        if self.currentFrame != None:
            sprite_TLx = self.centerX - self.currentFrame.get_width()//2
            sprite_TLy = self.centerY - self.currentFrame.get_height()//2
            canvas.blit(self.currentFrame, (sprite_TLx, sprite_TLy))
    #------------------------------#

    #------------------------------#
    # Function that selects a requested animation
    def selectAnimation(self, animationName, runOnce=False, fallbackToStartingAnimation=False):
        # Find the requested animation in the sprite's animation list
        self.selectedAnimation = None
        for animation in self.animationData:
            if animation["name"] == animationName:
                self.selectedAnimation = animation
                break
        
        if self.selectedAnimation == None:
            print('ERROR: Could not find the requested animation - ' + animationName)
            return

        # Load the animation source image
        sourceImagePath = os.path.join(self.selectedAnimation["path"], self.selectedAnimation["source"])
        self.currentAnimationSpritesheet = Spritesheet(sourceImagePath)

        # Load the animation frames
        framesPath = os.path.join(self.selectedAnimation["path"], self.selectedAnimation["frames"])
        self.currentAnimationFrames = loadJSONFile(framesPath)

        # Get the animation's scale
        self.currentAnimationScale = self.selectedAnimation["scale"] * self.scaleFactor

        # Get the animation's FPS
        self.currentAnimationFPS = self.selectedAnimation["FPS"]
        self.modFactor = GAME_FPS // self.currentAnimationFPS

        # Set the "run once" property
        self.runOnce = runOnce

        # Set the "fallback to starting animation" property
        self.fallbackToStartingAnimation = fallbackToStartingAnimation

        # Set the current animation frame
        self.currentAnimationFrameIndex = -1
    #------------------------------#
        
    #------------------------------#
    # Function that returns the next frame in the animation
    def progressCurrentAnimation(self, frameCount):
        if self.currentAnimationFrames == None:
            return
        
        if frameCount % self.modFactor == 0:
            if (self.currentAnimationFrameIndex < len(self.currentAnimationFrames)-1):
                self.currentAnimationFrameIndex += 1
            else:
                if not self.runOnce:
                    self.currentAnimationFrameIndex = 0
                else:
                    if self.fallbackToStartingAnimation:
                        self.selectAnimation(self.startingAnimation)
                        self.fallbackToStartingAnimation = False
                    if self.sendSignals:
                        self.emitSignal(msg="animation-finished", data=None, targetID=self.parentID)

        frame = self.currentAnimationFrames[self.currentAnimationFrameIndex]

        currentFrame = self.currentAnimationSpritesheet.get_sprite(frame["x"], frame["y"], frame["width"], frame["height"], self.currentAnimationScale)
        if self.mirror:
            currentFrameCopy = currentFrame.copy()
            currentFrame = pygame.transform.flip(currentFrameCopy, True, False)

        self.currentFrame = currentFrame
    #------------------------------#

    #------------------------------#
    # Function that updates the sprite's location
    def updateLocation(self, newX, newY):
        self.centerX = newX
        self.centerY = newY
    #------------------------------#