import pygame
import settings as Set

class main:
    def __init__(self):
        self.screen = pygame.display.set_mode(Set.SCREEN_SIZE)
        self.clock = pygame.time.Clock()
        self.running = True


    def gameloop(self):
        while self.running:
            self._update_events()
            self.dt = self.clock.tick()
            self.screen.fill(Set.BG_COLOR)
            pygame.display.flip()

    def _update_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.running = False

        self.key_pressed = pygame.key.get_pressed()


               



if __name__ == "__main__":
    #initialize
    Game : main = main()
    #GameLoop
    Game.gameloop()
