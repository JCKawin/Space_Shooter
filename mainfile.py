import pygame
import settings as Set
import ship

class main:
    def __init__(self):
        self.screen = pygame.display.set_mode(Set.SCREEN_SIZE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.ship = ship.ship()
        self.dt = 0
        
    def gameloop(self):
        while self.running:
            self._update_events()
            self.dt = self.clock.tick(60)
            self.screen.fill(Set.BG_COLOR)
            self.screen.blit(self.ship.image , self.ship.rect)
            pygame.display.flip()

    def _update_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.running = False

           
            self.ship.update()


    


               



if __name__ == "__main__":
    #initialize
    Game : main = main()
    #GameLoop
    Game.gameloop()
