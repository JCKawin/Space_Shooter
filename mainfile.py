import pygame
import settings as Set

class main:
    def __init__(self):
        self.screen = pygame.display.set_mode(Set.SCREEN_SIZE)
        self.clock = pygame.time.Clock()


    def gameloop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.dt = self.clock.tick()
            self.screen.fill(Set.BG_COLOR)
            pygame.display.flip()



if __name__ == "__main__":
    #initialize
    Game : main = main()
    #GameLoop
    Game.gameloop()
