import mainfile
import menu
import pygame
from settings import *

class main:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption("Sky Shooter")
        self.clock = pygame.time.Clock() #Clock Variable
        self.running = True
        self.score = 0
        self.f_pkl = pygame.font.Font(None, 30)
        self.dt = 0
        self.state = "menu"


        self.level = {
            "main" : mainfile.level1(self)

        }

        
    def run(self):
        self.level[self.state].run()


    




if __name__ == "__main__":
    # Start the game
    Game: main = main()

    Game.run()