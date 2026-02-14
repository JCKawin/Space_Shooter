import sys
import levels
import menu
import pygame
from settings import *

class main:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption("Space Shooter")
        self.clock = pygame.time.Clock() #Clock Variable
        self.running = True
        self.score = 0
        self.f_pkl = pygame.font.Font(None, 30)
        self.dt = 0
        self.state = "menu"


        self.level = {
            "menu" : menu.menu(self),
            "easy" : levels.easy(self),
            "midi" : levels.medium(self)

        }

        
    def run(self):
        while True:
            dt = self.clock.tick(FPS) if FPS else self.clock.tick()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                
            self.state = self.level[self.state].run()



    




if __name__ == "__main__":
    # Start the game
    Game: main = main()

    Game.run()