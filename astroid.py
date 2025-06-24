import random
from settings import *
import pygame


class Rock(pygame.sprite.Sprite):
    def __init__(self, group , location , image) -> None:
        super().__init__(group)        
        self.o_image = image
        self.image = self.o_image.copy()
        self.rect = self.o_image.get_frect(center = location)
        self.direction = pygame.Vector2(random.randint(-1,1) , 1)
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.angle = 0


    def update(self , dt) -> None:
        self.angle += 0.5 * dt
        self.image = pygame.transform.rotozoom(self.o_image , self.angle , 1)
        self.rect.center += self.direction *  ASTROID_SPEED * dt # type: ignore
        if self.rect.bottom > SCREEN_SIZE[1]: #type: ignore
            self.kill()
        


    


