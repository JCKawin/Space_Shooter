import settings as Set
import pygame

class bullet(pygame.sprite.Sprite):
    def __init__(self , group  , location) -> None:
        super().__init__(group)
        self.image = pygame.image.load("images\\proto#bullet.png").convert_alpha()
        self.image = pygame.transform.scale(self.image , (16,64))
        self.rect = self.image.get_frect(midbottom = location)

    def update(self , dt) -> None:
        self.rect.centery -= Set.MOVEMENT_SPEED * dt # type: ignore
        

