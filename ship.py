
import pygame
import settings as Set

class ship():
    def __init__(self ):
        
        self.image = pygame.image.load("images\\ship.jpg")
        self.image = pygame.transform.scale(self.image , (128 , 128))
        self.rect = self.image.get_rect(center = (Set.SCREEN_SIZE[0]/2 , Set.SCREEN_SIZE[1]/2))
        self.direction = pygame.Vector2(0,0)
        self.ismoving = False

    def update(self , dt):
        keypressed = pygame.key.get_pressed()
        self.direction.x = (int(keypressed[pygame.K_d]) - int(keypressed[pygame.K_a])) * Set.MOVEMENT_SPEED * dt
        self.direction.y = (int(keypressed[pygame.K_s]) - int(keypressed[pygame.K_w])) * Set.MOVEMENT_SPEED * dt

        self.rect.center += self.direction
        


      



    




