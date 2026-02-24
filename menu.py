"""
+--------------------------------------------------------------------------------------+
|                              SPACE SHOOTER - MENU MODULE                             |
|                                Team: இனிழ் (Inizh)                                  |
|                                                                                      |
|  Main menu screen with game mode selection.                                          |
|  Handles user input for starting different game levels.                              |
+--------------------------------------------------------------------------------------+
"""

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
        self.bg = pygame.image.load(join("images" , "menu_bg.jpeg")) 
        self.bg = pygame.transform.scale(self.bg , (1280 , 720))

    def run(self):
        while True:
            self.clock.tick(60)
            self.screen.fill("#000000")
            self.screen.blit(self.bg , (0,0))
            easy = self.font.render("Easy" , True , "white")
            medium = self.font.render("Hard" , True , "white")
            multi = self.font.render("Multiplayer" , True , "white")
            easy_rect = easy.get_rect()
            medium_rect = medium.get_rect()
            easy_rect.topleft = (30 , 350)
            medium_rect.topright = (1250 , 350)
            multi_rect = multi.get_rect()
            multi_rect.center = (640 , 500)
            self.screen.blit(easy ,easy_rect)
            self.screen.blit(medium,medium_rect)
            self.screen.blit(multi , multi_rect)
            pygame.draw.circle(self.screen , "white" , pygame.mouse.get_pos() , 5)
            pygame.display.flip()

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                
            m_pressed = pygame.mouse.get_pressed()
            if easy_rect.collidepoint(pygame.mouse.get_pos()) and m_pressed[0]:
                return "easy"
            elif medium_rect.collidepoint(pygame.mouse.get_pos()) and m_pressed[0]:
                return "midi"
            elif multi_rect.collidepoint(pygame.mouse.get_pos()) and m_pressed[0]:
                return "multi"