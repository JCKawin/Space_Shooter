import pygame

class ship(pygame.sprite.Sprite):
    def __init__(self,main):
        self.screen = main.screen
        self.rect = self.screen.get_rect()

        self.Ship_image = pygame.image.load("images\\ship.jpg")
        self.Ship_rect = self.Ship_image.get_rect()



