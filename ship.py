"""
+--------------------------------------------------------------------------------------+
|                              SPACE SHOOTER - SHIP MODULE                             |
|                                Team: இனிழ் (Inizh)                                  |
|                                                                                      |
|  Player ship classes with different ship types (base_ship, f14a).                    |
|  Handles player movement, health, and ship rendering.                                |
+--------------------------------------------------------------------------------------+
"""

import pygame
from settings import *


class base_ship():
    def __init__(self, main):
        self.screen = main.screen
        self.scr_rect = self.screen.get_rect()
        self.image = pygame.image.load(IMG_SHIP).convert_alpha()
        self.image = pygame.transform.scale(self.image, (154, 154))
        self.rect = self.image.get_frect(center=(SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2))
        self.direction = pygame.Vector2(0, 0)
        self.ismoving = False
        self.Hp = 100

    def update(self, dt):
        keypressed = pygame.key.get_pressed()
        self.direction.x = (int(keypressed[pygame.K_d] | keypressed[pygame.K_RIGHT]) - int(keypressed[pygame.K_a] | keypressed[pygame.K_LEFT]))
        self.direction.y = (int(keypressed[pygame.K_s] | keypressed[pygame.K_DOWN]) - int(keypressed[pygame.K_w] | keypressed[pygame.K_UP])) 
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * MOVEMENT_SPEED * dt
        if self.rect.right < self.scr_rect.left:
            self.rect.left = self.scr_rect.right
        elif self.rect.left > self.scr_rect.right:
            self.rect.right = self.scr_rect.left
        elif self.rect.bottom < self.scr_rect.top:
            self.rect.top = self.scr_rect.bottom
        elif self.rect.top > self.scr_rect.bottom:
            self.rect.bottom = self.scr_rect.top


class f14a(base_ship):
    def __init__(self, main):
        super().__init__(main)
        self.image = pygame.image.load(IMG_SHIP_F14A).convert_alpha()
        self.image = pygame.transform.scale(self.image, (154, 154)) 

    def update(self, dt):
        keypressed = pygame.key.get_pressed()
        self.direction.x = (int(keypressed[pygame.K_d] | keypressed[pygame.K_RIGHT]) - int(keypressed[pygame.K_a] | keypressed[pygame.K_LEFT]))
        self.direction.y = (int(keypressed[pygame.K_s] | keypressed[pygame.K_DOWN]) - int(keypressed[pygame.K_w] | keypressed[pygame.K_UP])) 
        self.direction = self.direction.normalize() if self.direction else self.direction
        mul = 2 if keypressed[pygame.K_SPACE] else 1 
        self.rect.center += self.direction * MOVEMENT_SPEED * dt * mul
        if self.rect.right < self.scr_rect.left:
            self.rect.left = self.scr_rect.right
        elif self.rect.left > self.scr_rect.right:
            self.rect.right = self.scr_rect.left
        elif self.rect.bottom < self.scr_rect.top:
            self.rect.top = self.scr_rect.bottom
        elif self.rect.top > self.scr_rect.bottom:
            self.rect.bottom = self.scr_rect.top