import pygame
from settings import *

class cloud(pygame.sprite.Sprite):
    def __init__(self , group ,  image: pygame.Surface ):
        super().__init__(group)
        self.image = image
        self.rect = self.image.get_frect()
        self.rect.bottomleft = pygame.Vector2(0,0)


    def update(self, speed , dt) -> None:
        self.rect.y += speed * dt  # type: ignore
        if self.rect.y > SCREEN_SIZE[1]:  # type: ignore
            self.kill()

