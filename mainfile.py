import random
import pygame
import settings as Set
import ship
import astroid

class main:
    def __init__(self):
        pygame.init()
        pygame.display.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode(Set.SCREEN_SIZE , pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.Background = pygame.image.load("images\\proto#background.bmp")
        self.Rock = pygame.sprite.Group()        
        self.running = True
        
        self.ship = ship.ship(self)
        self.dt = 0
        
    def gameloop(self):
        put_astroid = pygame.event.custom_type()
        pygame.time.set_timer(put_astroid , 1000)
        
        while self.running:
            rock_point = random.randint(0 , Set.SCREEN_SIZE[0]) , random.randint(0 , 20) 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == put_astroid:
                    astroid.Rock(self.Rock , rock_point)
            self.dt = self.clock.tick()
            self.screen.blit(self.Background , (0,0))
            self.screen.blit(self.ship.image , self.ship.rect)
            self.Rock.draw(self.screen)
            pygame.display.flip()
            self.Rock.update(self.dt)       
            self.ship.update(self.dt)        

    


        
            
    


               



if __name__ == "__main__":
    #initialize
    Game : main = main()
    #GameLoop
    Game.gameloop()
