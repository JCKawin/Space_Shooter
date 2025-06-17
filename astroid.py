import random
import settings as Set
import pygame


class Rock(pygame.sprite.Sprite):
    def __init__(self, group , location) -> None:
        super().__init__(group)
        self.o_image =  pygame.image.load("images\\proto#astroid.png").convert_alpha()
        self.o_image = pygame.transform.scale(self.o_image , (64,64))
        self.image = self.o_image.copy()
        self.rect = self.o_image.get_frect(center = location)
        self.direction = pygame.Vector2(random.randint(-1,1) , 1)
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.angle = 0


    def update(self , dt) -> None:
        self.angle += 0.5 * dt
        self.image = pygame.transform.rotozoom(self.o_image , self.angle , 1)
        self.rect.center += self.direction *  Set.ASTROID_SPEED * dt # type: ignore
        if self.rect.bottom > Set.SCREEN_SIZE[1]: #type: ignore
            self.kill()
        


    


