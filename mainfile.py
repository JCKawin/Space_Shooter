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
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.dt = self.clock.tick()
            self.screen.fill(Set.BG_COLOR)
            self.screen.blit(self.ship.image , self.ship.rect)
            pygame.display.flip()
            self.ship.update(self.dt)        

    def _draw_fps(self):
        fps = self.font.render(self.clock.get_fps(),True ,(0,0,0))
        fps_rect = fps.get_frect()
        fps_rect.topleft = (0,0)


        
            
    


               



if __name__ == "__main__":
    #initialize
    Game : main = main()
    #GameLoop
    Game.gameloop()
