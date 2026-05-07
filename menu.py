"""
+--------------------------------------------------------------------------------------+
|                              SPACE SHOOTER - MENU MODULE                             |
|                                Team: இனிழ் (Inizh)                                  |
|                                                                                      |
|  Main menu screen with game mode selection.                                          |
|  Handles user input for starting different game levels.                              |
+--------------------------------------------------------------------------------------+
"""

import sys

import pygame

from settings import *


class menu:
    def __init__(self, main) -> None:
        self.screen: pygame.surface.Surface = main.screen
        self.clock = main.clock
        pygame.mouse.set_visible(False)
        self.font = pygame.font.Font(FONT_UNWAVE, 80)
        self.bg = pygame.image.load(IMG_MENU_BG)
        self.bg = pygame.transform.scale(self.bg, (1280, 720))
        self.done = False
        self.next_state = None

    def run(self):
        while True:
            self.clock.tick(60)
            self.screen.fill("#000000")
            # self.screen.blit(self.bg, (0, 0))
            self.m_pressed = pygame.mouse.get_pressed()
            self.modes("Easy", (30, 190))
            self.modes("Medium", (30, 300))
            self.modes("Multiplayer", (30, 500))
            self.text_box("Name: ", (30, 600))
            if self.done:
                return
            pygame.draw.circle(self.screen, "white", pygame.mouse.get_pos(), 5)
            pygame.display.flip()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()

    def modes(self, return_state, pos):
        easy = self.font.render(f"{return_state}", True, "white")
        easy_rect = easy.get_rect()
        easy_rect.topleft = pos
        self.screen.blit(easy, easy_rect)
        if easy_rect.collidepoint(pygame.mouse.get_pos()) and self.m_pressed[0]:
            print(return_state)
            self.next_state = return_state.lower()
            self.done = True

    def text_box(self, text, pos):
        isactive = False
        box = pygame.Rect(pos, (500, 80))
        capture_buffer = ""
        if box.collidepoint(pygame.mouse.get_pos()) and self.m_pressed[0]:
            isactive = True
        elif self.m_pressed[0] and isactive:
            isactive = False

        if isactive:
            chracters = [
                pygame.key.name(event.key)
                for event in pygame.event.get()
                if event.type == pygame.KEYDOWN
            ]
            text = "".join(chracters)
            capture_buffer += text
        else:
            text = capture_buffer

        text_surface = self.font.render(text, True, "white")
        text_rect = text_surface.get_rect()
        text_rect.topleft = pos
        self.screen.blit(text_surface, text_rect)
