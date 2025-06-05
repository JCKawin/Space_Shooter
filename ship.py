import pygame
import settings as Set

class ship():
    def __init__(self):
       
        self.image = pygame.image.load("images\\ship.jpg")
        self.image = pygame.transform.scale(self.image , (128 , 128))
        self.rect = self.image.get_frect()
        self.direction = pygame.Vector2()
        self.ismoving = False

    def update(self , dt):
        if self.ismoving:
            self.move(dt)

    
    def move(self ,dt):
        key = pygame.key.get_pressed()
        self.direction.x = (int(key[pygame.K_d]) - int(key[pygame.K_a])) * Set.MOVEMENT_SPEED / dt
        self.direction.y = (int(key[pygame.K_s]) - int(key[pygame.K_w])) * Set.MOVEMENT_SPEED / dt
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction
        


      



    




