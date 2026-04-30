"""
+--------------------------------------------------------------------------------------+
|                              SPACE SHOOTER - LOADING SCREEN                          |
|                                Team: இனிழ் (Inizh)                                  |
|                                                                                      |
|  Loading screen with progress bar and team logo animation.                           |
|  Displays while game assets are being loaded.                                        |
+--------------------------------------------------------------------------------------+
"""

import pygame

from settings import *


class loader:
    def __init__(self, main):
        self.screen = main.screen
        self.clock = main.clock
        self.text = pygame.font.Font(None, 48)
        self.logo = pygame.transform.scale(pygame.image.load(IMG_LOGO), (386, 386))
        self.texter = self.text.render("Loading...", True, (255, 255, 255))
        self.tamil = pygame.font.Font(FONT_TAMIL, 72)
        self.inx = self.tamil.render("இனிழ்", True, (255, 255, 255))
        self.progress = 0

    def run(self):
        cx = SCREEN_SIZE[0] / 2

        while self.progress != 100:
            self.screen.fill((0, 0, 0))

            # Logo
            logo_x = cx - self.logo.get_width() / 2
            logo_y = 25
            self.screen.blit(self.logo, (logo_x, logo_y))

            # ✨இனிழ்___🖌️
            inx_x = cx - self.inx.get_width() / 2
            inx_y = logo_y + self.logo.get_height() + 10
            self.screen.blit(self.inx, (inx_x, inx_y))

            # Loading...
            load_x = cx - self.texter.get_width() / 2
            load_y = inx_y + self.inx.get_height() + 25
            self.screen.blit(self.texter, (load_x, load_y))

            # Progress bar
            bar_w = 600
            bar_h = 24
            bar_x = cx - bar_w / 2
            bar_y = load_y + self.texter.get_height() + 12
            bg_rect = pygame.Rect(bar_x, bar_y, bar_w, bar_h)
            fg_rect = pygame.Rect(bar_x, bar_y, bar_w * self.progress / 100, bar_h)
            pygame.draw.rect(self.screen, (80, 80, 80), bg_rect, border_radius=6)
            pygame.draw.rect(self.screen, (255, 255, 255), fg_rect, border_radius=6)

            self.progress += 0.5
            pygame.display.flip()
            self.clock.tick(60)
