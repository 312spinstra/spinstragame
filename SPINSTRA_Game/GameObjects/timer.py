import pygame
from .game_object import GameObject
from GameOperation import Repeat

# Class that implements a Timer
class Timer(GameObject):
    #------------------------------#
    # Constructor Function
    def __init__(self, initialValue=0):
        super().__init__()
        gameRuntime = self.getGlobalDictValue("gameRuntime")
        if gameRuntime == None:
            self.setGlobalDictValue("gameRuntime", 0)
            gameRuntime = self.getGlobalDictValue("gameRuntime")
        gameRuntime = initialValue
        self.actuallyIncrement = False
        self.timerThread = None
    #------------------------------#

    #------------------------------#
    # Destructor Function
    def __del__(self):
        if (self.timerThread != None):
            self.timerThread.cancel()

        super().__del__()
    #------------------------------#
    
    #------------------------------#
    # Function that starts the timer
    def startTimer(self):
        self.actuallyIncrement = True
        self.timerThread = Repeat(1.0, self.incrementTimer)
        self.timerThread.start()
    #------------------------------#

    #------------------------------#
    # Function that pauses the timer   
    def pauseTimer(self):
        self.actuallyIncrement = False
    #------------------------------#

    #------------------------------#
    # Function that resumes the timer   
    def resumeTimer(self):
        self.actuallyIncrement = True
    #------------------------------#

    #------------------------------#
    # Function that increments the timer
    def incrementTimer(self):
        if not self.actuallyIncrement:
            return
        
        gameRuntime = self.getGlobalDictValue("gameRuntime")
        self.setGlobalDictValue("gameRuntime", gameRuntime + 1)
    #------------------------------#