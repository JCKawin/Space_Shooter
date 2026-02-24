"""
+--------------------------------------------------------------------------------------+
|                              SPACE SHOOTER - BULLET MODULE                           |
|                                Team: இனிழ் (Inizh)                                  |
|                                                                                      |
|  Bullet sprite fired by the player's ship.                                           |
|  Handles bullet movement and collision detection.                                    |
+--------------------------------------------------------------------------------------+
"""

from settings import *
import pygame

class bullet(pygame.sprite.Sprite):
    def __init__(self , group  , location , image) -> None:
        super().__init__(group)
        self.image = image
        self.image = pygame.transform.scale(self.image , (16,64))
        self.rect = self.image.get_frect(midbottom = location)

    def update(self , dt) -> None:
        self.rect.centery -= BULLET_SPEED * dt # type: ignore
        if self.rect.bottom < 0: #type: ignore
            self.kill()
        

