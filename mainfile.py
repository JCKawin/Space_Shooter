import random
import time
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
        pygame.mixer.init()
        self.screen = pygame.display.set_mode(Set.SCREEN_SIZE)
        self.load_asserts()
        self.clock = pygame.time.Clock()
        self.rock = pygame.sprite.Group()  
        self.bullet = pygame.sprite.Group()     
        self.running = True
        self.score = 0 
        self.f_pkl = pygame.font.Font(None, 30)       
        self.ship = ship.ship(self)
        self.dt = 0
        self.health_bar_colour = 'white'
        self.start_colour = time.time()

    def load_asserts(self):
        self.background = pygame.image.load("images\\proto#background.bmp")
        self.f_uwl = pygame.font.Font("fonts\\VT323-Regular.ttf" , 30)
        self.bul_img = pygame.image.load("images\\proto#bullet.png").convert_alpha()
        self.rock_img = pygame.image.load("images\\proto#astroid.png").convert_alpha()
        self.rock_img = pygame.transform.scale(self.rock_img , (64,64))
        self.bgm = pygame.mixer.music.load("audio\\Project_Space Shooter_Final.mp3")
        pygame.mixer.music.set_volume(0.7)
        self.shoot_eff=pygame.mixer.Sound("audio\\Space Shooter_Fire.mp3")
        self.rock_exp_eff=pygame.mixer.Sound("audio\\Space Shooter_Explosion.mp3")

        
    def gameloop(self):
        put_astroid = pygame.event.custom_type()
        pygame.time.set_timer(put_astroid , 500)
        pygame.mixer.music.play(loops= -1)
        
        while self.running:
            rock_point = random.randint(0 , Set.SCREEN_SIZE[0]) , random.randint(0 , 20) 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == put_astroid:
                    astroid.Rock(self.rock , rock_point , self.rock_img)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_j:
                        bullet.bullet(self.bullet , self.ship.rect.midtop , self.bul_img )
                        pygame.mixer.Sound.play(self.shoot_eff)

                    if event.key == pygame.K_l:
                        self._heal()
            
            self.screen.blit(self.background , (0,0))
            self.screen.blit(self.ship.image , self.ship.rect)
            self.rock.draw(self.screen)
            self.bullet.draw(self.screen)
            self._UI()      
            self.dt = self.clock.tick()
            self.rock.update(self.dt)       
            self.ship.update(self.dt) 
            self.bullet.update(self.dt)
            self._damage()
            pygame.display.flip()

        else:
            self.gameover()

    def _damage(self):
        if pygame.sprite.spritecollide(self.ship , self.rock , True):
            self.ship.Hp -= 1
            self.health_bar_colour = 'red'
            self.start_colour = time.time()
    
        if pygame.sprite.groupcollide(self.bullet , self.rock , True , True):
            self.score += 1
            pygame.mixer.Sound.play(self.rock_exp_eff)

        if self.ship.Hp == 0:
            self.running = False

        if round(time.time() - self.start_colour , 1) == 0.3 : 
            self.health_bar_colour = 'white'

    def _heal(self):
        if self.score >= 10 and self.ship.Hp < 90:
            self.score -= 10
            self.ship.Hp += 10
            self.health_bar_colour = 'blue'
            self.start_colour = time.time()



    def _UI(self):
        healthbar = pygame.rect.Rect(30 , Set.SCREEN_SIZE[1] - 50 , self.ship.Hp * 4 , 20 )
        pygame.draw.rect(self.screen , self.health_bar_colour , healthbar)
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
