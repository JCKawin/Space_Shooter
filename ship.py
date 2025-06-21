import pygame
from settings import *


class ship():
    def __init__(self, main):
        self.screen = main.screen
        self.scr_rect = self.screen.get_rect()
        self.image = pygame.image.load("images\\F-14A.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (154, 154))
        self.rect = self.image.get_frect(center=(SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2))
        self.direction = pygame.Vector2(0, 0)
        self.ismoving = False
        self.Hp = 100

    def update(self, dt):
        keypressed = pygame.key.get_pressed()
        self.direction.x = (int(keypressed[pygame.K_d] | keypressed[pygame.K_RIGHT]) - int(keypressed[pygame.K_a] | keypressed[pygame.K_LEFT])) * MOVEMENT_SPEED * dt
        self.direction.y = (int(keypressed[pygame.K_s] | keypressed[pygame.K_DOWN]) - int(keypressed[pygame.K_w] | keypressed[pygame.K_UP])) * MOVEMENT_SPEED * dt

        self.rect.center += self.direction
        if self.rect.right < self.scr_rect.left:
            self.rect.left = self.scr_rect.right
        elif self.rect.left > self.scr_rect.right:
            self.rect.right = self.scr_rect.left
        elif self.rect.bottom < self.scr_rect.top:
            self.rect.top = self.scr_rect.bottom
        elif self.rect.top > self.scr_rect.bottom:
            self.rect.bottom = self.scr_rect.top
