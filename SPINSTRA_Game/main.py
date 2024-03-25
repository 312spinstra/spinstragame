import threading
import sys
from GameObjects import GameManager
from engine_initialization import GameEngine

#------------------------------#
# Main function
def main():
    # Start the game logic in a separate thread
    gameManager = GameManager()
    gameThread = threading.Thread(target=gameManager.begin)
    gameThread.start()

    # Use the Game Engine to render the active game objects in this thread so long as the user doesn't want to quit
    while not GameEngine.quit:
        GameEngine.runGame()

    # Stop the game logic thread
    gameThread.join()

    # Exit the program
    sys.exit(0)
#------------------------------#

# Run the main function
if __name__ == "__main__":
    main()

""" (Note from the Programmer):
    I know I could just write the contents of "main" directly in the file, but 
    I'm a C programmer at heart and like to see a definitive "main" entry point 
    to an application. Feel free to refactor as you wish! """