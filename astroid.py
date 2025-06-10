import settings as Set
import pygame


class Rock(pygame.sprite.Sprite):
    def __init__(self, group , location) -> None:
        super().__init__(group)
        self.image = pygame.image.load("images\\proto#astroid.png").convert_alpha()
        self.image = pygame.transform.scale(self.image , (64,64))
        self.rect = self.image.get_frect(center = location)

    def update(self , dt) -> None:
        self.rect.centery += Set.MOVEMENT_SPEED * dt


    


