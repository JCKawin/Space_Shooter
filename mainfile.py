import pygame
import settings as Set
import ship

class main:
    def __init__(self):
        pygame.init()
        pygame.display.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode(Set.SCREEN_SIZE , pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.Background = pygame.image.load("images\\proto#background.bmp")
        
        self.running = True
        
        self.ship = ship.ship(self)
        self.dt = 0
        
    def gameloop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.dt = self.clock.tick()
            self.screen.blit(self.Background , (0,0))
            self.screen.blit(self.ship.image , self.ship.rect)
            pygame.display.flip()
            self.ship.update(self.dt)        

    def _draw_fps(self):
        fps = self.f_uwl.render(self.clock.get_fps(),True ,(0,0,0))
        fps_rect = fps.get_frect()
        fps_rect.topleft = (0,0)
        self.screen.blit(fps , fps_rect)


        
            
    


               



if __name__ == "__main__":
    #initialize
    Game : main = main()
    #GameLoop
    Game.gameloop()
