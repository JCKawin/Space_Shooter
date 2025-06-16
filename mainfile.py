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
        self.score = 0 
        self.f_uwl = pygame.font.Font("fonts\\VT323-Regular.ttf" , 30)
        self.f_pkl = pygame.font.Font(None, 30)       
        self.ship = ship.ship(self)
        self.dt = 0
        
    def gameloop(self):
        put_astroid = pygame.event.custom_type()
        pygame.time.set_timer(put_astroid , 10)
        
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
            self._UI()      
            pygame.display.flip()
            self.rock.update(self.dt)       
            self.ship.update(self.dt) 
            self.bullet.update(self.dt)
            self._damage()

        else:
            pass 

    def _damage(self):
        if pygame.sprite.spritecollide(self.ship , self.rock , True):
            self.ship.Hp -= 1
            
        if pygame.sprite.groupcollide(self.bullet , self.rock , True , True):
            self.score += 1

        if self.ship.Hp == 0:
            self.running = False



    def _UI(self):
        healthbar = pygame.rect.Rect(30 , Set.SCREEN_SIZE[1] - 50 , self.ship.Hp * 4 , 20 )
        pygame.draw.rect(self.screen , 'white' , healthbar)
        self.printf(self.screen , f"health {self.ship.Hp}" ,  (34 , Set.SCREEN_SIZE[1] - 55) , 'black' , self.f_uwl )
        self.printf(self.screen , f"FPS: {round(self.clock.get_fps() , 0 )}" , (30 , 30) , 'white' , self.f_pkl )
        self.printf(self.screen , f"Score : {self.score}" ,  (Set.SCREEN_SIZE[0] - 120  , 20 ) , 'white' , self.f_pkl)

    def gameover(self):
        pass
    
    @staticmethod
    def printf(screen , text , rect , colour , font ):
        tex = font.render(text , True , colour)
        tex_rect = tex.get_rect()
        tex_rect.topleft = rect
        screen.blit(tex , tex_rect)
        


        



        

    


        
            
    


               



if __name__ == "__main__":
    #initialize
    Game : main = main()
    #GameLoop
    Game.gameloop()
