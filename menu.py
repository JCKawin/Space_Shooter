from os.path import join
import pygame
from settings import *
import sys

class menu:
    def __init__(self,main) -> None:
        self.screen : pygame.surface.Surface = main.screen
        self.clock = main.clock
        pygame.mouse.set_visible(False)
        self.font = pygame.font.Font(join("fonts" , "UnwaveLover-PV9AZ.otf") , 80) 

    def run(self):
        while True:
            self.clock.tick(60)
            self.screen.fill("#000000")
            classic = self.font.render("Classic" , True , "white" , "black")
            sky = self.font.render("Sky" , True , "white" , "black")
            classic_rect = classic.get_frect()
            sky_rect = classic.get_frect()
            classic_rect.topleft = (30 , 350)
            sky_rect.topright = (1250 , 350)
            self.screen.blit(classic ,classic_rect)
            self.screen.blit(sky,sky_rect)
            pygame.draw.circle(self.screen , "white" , pygame.mouse.get_pos() , 5)
            pygame.display.flip()

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                
            m_pressed = pygame.mouse.get_pressed()
            if sky_rect.collidepoint(pygame.mouse.get_pos()) and m_pressed[0]:
                return "main"
            elif classic_rect.collidepoint(pygame.mouse.get_pos()) and m_pressed[0]:
                return "base"