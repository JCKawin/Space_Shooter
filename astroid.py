import pygame


class Rock(pygame.sprite.Sprite):
    def __init__(self, group) -> None:
        super().__init__(group)
        self.image = pygame.image.load("images\\proto#astroid.png").convert_alpha()
        self.rect = self.image.get_frect()


    


