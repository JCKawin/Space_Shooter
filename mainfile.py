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
        self.f_uwl = pygame.font.Font("fonts\\UnwaveLover-PV9AZ.otf" , 25)
        self.f_pkl = pygame.font.Font(None, 30)       
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
            self._healthbar()      
            pygame.display.flip()
            self.rock.update(self.dt)       
            self.ship.update(self.dt) 
            self.bullet.update(self.dt)
            self._damage() 

    def _damage(self):
        if pygame.sprite.spritecollide(self.ship , self.rock , True):
            self.ship.Hp -= 1
            
        if pygame.sprite.groupcollide(self.bullet , self.rock , True , True):
            self.score += 1
            print(self.score)

    def _healthbar(self):
        healthbar = pygame.rect.Rect(30 , Set.SCREEN_SIZE[1] - 50 , self.ship.Hp * 4 , 20 )
        pygame.draw.rect(self.screen , 'white' , healthbar)
        text = self.f_uwl.render("health" , True , 'black')
        text_rect = text.get_rect()
        text_rect.topleft = (34 , Set.SCREEN_SIZE[1] - 55)
        self.screen.blit(text , text_rect)
        fps = self.f_pkl.render(f"FPS: {round(self.clock.get_fps() , 0)}" , True , 'white')
        fps_rect = fps.get_rect()
        fps_rect.topleft = (30 , 30)
        self.screen.blit(fps , fps_rect)
        score = self.f_pkl.render(f"Score : {self.score}" , True , 'white')
        score_rect = score.get_rect()
        score_rect.topright = (Set.SCREEN_SIZE[0] - 50 , 20 )
        self.screen.blit(score , score_rect)

        



        

    


        
            
    


               



if __name__ == "__main__":
    #initialize
    Game : main = main()
    #GameLoop
    Game.gameloop()
