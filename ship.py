import pygame
import settings as Set

class ship():
    def __init__(self):
       
        self.image = pygame.image.load("images\\ship.jpg")
        self.image = pygame.transform.scale(self.image , (128 , 128))
        self.rect = self.image.get_frect()
        self.direction = pygame.Vector2()

    def update(self):
        keypressed = pygame.key.get_just_pressed()
        self.direction.x += (keypressed[pygame.K_d] - keypressed[pygame.K_a]) * Set.MOVEMENT_SPEED 
        self.direction.y += (keypressed[pygame.K_s] - keypressed[pygame.K_w]) * Set.MOVEMENT_SPEED 
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction


      



    




