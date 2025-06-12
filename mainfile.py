import random
import pygame
import settings as Set
import ship
import astroid
import bullet

class main:
    def __init__(self):
        pygame.init()
        pygame.display.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode(Set.SCREEN_SIZE)
        self.clock = pygame.time.Clock()
        self.background = pygame.image.load("images\\proto#background.bmp")
        self.rock = pygame.sprite.Group()  
        self.bullet = pygame.sprite.Group()     
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
                    astroid.Rock(self.rock , rock_point)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_j:
                        bullet.bullet(self.bullet , self.ship.rect.midtop )
            self.dt = self.clock.tick()
            self.screen.blit(self.background , (0,0))
            self.screen.blit(self.ship.image , self.ship.rect)
            self.rock.draw(self.screen)
            self.bullet.draw(self.screen)
            pygame.display.flip()
            self.rock.update(self.dt)       
            self.ship.update(self.dt) 
            self.bullet.update(self.dt)
            self._damage()       

    def _damage(self):
        if pygame.sprite.spritecollide(self.ship , self.rock , True):
            self.ship.Hp -= 1
            print(self.ship.Hp)

    


        
            
    


               



if __name__ == "__main__":
    #initialize
    Game : main = main()
    #GameLoop
    Game.gameloop()
