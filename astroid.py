import random
import settings as Set
import pygame


class Rock(pygame.sprite.Sprite):
    def __init__(self, group , location) -> None:
        super().__init__(group)
        self.image =  pygame.image.load("images\\proto#astroid.png").convert_alpha()
        self.image = pygame.transform.scale(self.image , (64,64))
        self.rect = self.image.get_frect(center = location)
        self.direction = pygame.Vector2(random.randint(-1,1) , 1)
        self.direction = self.direction.normalize() if self.direction else self.direction

    def update(self , dt) -> None:
        self.rect.center += self.direction * dt # type: ignore
        if self.rect.bottom > Set.SCREEN_SIZE[1]: #type: ignore
            self.kill()
        


    


