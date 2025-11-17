import pygame
from settings import *

class menu:
    def __init__(self,main) -> None:
        self.screen = main.screen
        self.clock = main.clock

    def run(self):
        while True:
            self.clock.tick(60)
            self.screen.fill("#2F0A33")
            pygame.display.flip()
            for e in pygame.event.get():
                if e.type == pygame.KEYDOWN:
                    return "base"

