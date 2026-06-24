"""
+--------------------------------------------------------------------------------------+
|                                   SPACE SHOOTER                                      |
|                                Team: இனிழ் (Inizh)                                  |
|                                                                                      |
|  Copyright (c) Team இனிழ். All rights reserved.                                     |
|                                                                                      |
|  Authors / Contributors:                                                             |
|    - JCKawin                                                                         |
|    - Joseph Daniel                                                                   |
|    - Jai Suriyaa                                                                     |
|                                                                                      |
|  Licensing:                                                                          |
|    See the LICENSE file in this repository for permissions and limitations.          |
|                                                                                      |
|  Notes:                                                                              |
|    Project assets (art, music, and sound effects) are created in-house unless        |
|    explicitly stated otherwise.                                                      |
+--------------------------------------------------------------------------------------+
"""

import sys
from os.path import join

import pygame

import levels
import loading_screen
import menu
import multiplayer
from settings import *


class main:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        logo = pygame.image.load(IMG_LOGO)
        pygame.display.set_caption("Space Shooter")
        pygame.display.set_icon(logo)
        self.clock = pygame.time.Clock()  # Clock Variable
        self.running = True
        self.score = 0
        self.f_pkl = pygame.font.Font(None, 30)
        self.dt = 0
        self.state = "menu"
        load = loading_screen.loader(self)
        load.run()

        self.level = {
            "menu": menu.menu(self),
            "easy": levels.easy(self),
            "medium": levels.medium(self),
        }

    def run(self):
        while True:
            current = self.level[self.state]
            if current.done:
                current.done = False
                self.state = current.next_state
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
            self.level[self.state].run()


if __name__ == "__main__":
    # Start the game
    Game: main = main()

    Game.run()
