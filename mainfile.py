import random
import sys
import time
import pygame
from settings import *
import ship
import astroid
import bullet



class main:
    def __init__(self):
        pygame.init()
        pygame.display.init()
        pygame.font.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption("Sky Shooter")
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
        self.f_uwl_big = pygame.font.Font("fonts\\VT323-Regular.ttf" , 360)
        self.f_uwl = pygame.font.Font("fonts\\VT323-Regular.ttf" , 30)
        self.bul_img = pygame.image.load("images\\proto#bullet.png").convert_alpha()
        self.rock_img = pygame.image.load("images\\proto#astroid.png").convert_alpha()
        self.rock_img = pygame.transform.scale(self.rock_img , (64,64))
        self.bgm = pygame.mixer.music.load("audio\\Project_Space Shooter_Final_Loop.mp3")
        pygame.mixer.music.set_volume(0.5)
        self.shoot_eff=pygame.mixer.Sound("audio\\Space Shooter_Fire.mp3")
        self.rock_exp_eff=pygame.mixer.Sound("audio\\Space Shooter_Explosion.mp3")
        self.rock_impact=pygame.mixer.Sound("audio\\Space Shooter_Asteroid Impact.mp3")
        self.ship_heal_eff=pygame.mixer.Sound("audio\\Space Shooter_Healing.mp3")

    def menu(self):
        pass


    def gameloop(self):
        put_astroid = pygame.event.custom_type()
        pygame.time.set_timer(put_astroid, 500)
        pygame.mixer.music.play(loops=-1)

        while self.running:
            rock_point = random.randint(
                0, SCREEN_SIZE[0]), random.randint(0, 20)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == put_astroid:
                    astroid.Rock(self.rock, rock_point, self.rock_img)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_j:
                        bullet.bullet(self.bullet, self.ship.rect.midtop, self.bul_img)
                        pygame.mixer.Sound.play(self.shoot_eff)

                    if event.key == pygame.K_l:
                        self._heal()
            self.screen.fill(BG_COLOR)
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.ship.image, self.ship.rect)
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
            pygame.mixer.music.fadeout(1000)
            self.gameover()

        pygame.quit()

    def _damage(self):
        if pygame.sprite.spritecollide(self.ship, self.rock, True):
            pygame.mixer.Sound.play(self.rock_impact)
            self.ship.Hp -= 5
            self.health_bar_colour = 'red'
            self.start_colour = time.time()

        if pygame.sprite.groupcollide(self.bullet, self.rock, True, True):
            self.score += 1
            pygame.mixer.Sound.play(self.rock_exp_eff)

        if self.ship.Hp == 0:
            self.running = False

        if round(time.time() - self.start_colour, 1) == 0.3:
            self.health_bar_colour = 'white'

    def _heal(self):
        if self.score >= 10 and self.ship.Hp < 95:
            self.score -= 10
            self.ship.Hp += 5
            self.health_bar_colour = 'blue'
            self.start_colour = time.time()
            pygame.mixer.Sound.play(self.ship_heal_eff)

    def _UI(self):
        healthbar = pygame.rect.Rect(30, SCREEN_SIZE[1] - 50, self.ship.Hp * 4, 20)
        pygame.draw.rect(self.screen, self.health_bar_colour, healthbar)
        self.printf(self.screen, f"health {self.ship.Hp}", (34, SCREEN_SIZE[1] - 55), 'black', self.f_uwl) 
        self.printf(self.screen, f"FPS: {round(self.clock.get_fps(), 0)}", (30, 30), 'white', self.f_pkl)
        self.printf(self.screen, f"Score : {self.score}",(SCREEN_SIZE[0] - 120, 20), 'white', self.f_pkl)

    def gameover(self):
        while True:
            self.screen.fill(BG_COLOR)
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.ship.image, self.ship.rect)
            self.rock.draw(self.screen)
            self.printf(self.screen , "GAME OVER" , (0,0) , "white" , self.f_uwl_big , True )
            self.printf(self.screen , "Press Space to continue" , (10 , 500) , 'white' ,  self.f_pkl)
            self.clock.tick()
            self._UI()
            self.rock.update(self.dt)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        sys.exit()
            
        

    @staticmethod
    def printf(screen, text, rect, colour, font , center : bool = False):
        tex = font.render(text, True, colour)
        tex_rect = tex.get_rect()
        tex_rect.topleft = rect
        if center : tex_rect.center = screen.get_rect().center 
        screen.blit(tex, tex_rect)
        


if __name__ == "__main__":
    # initialize
    Game: main = main()
    # GameLoop
    Game.gameloop()
