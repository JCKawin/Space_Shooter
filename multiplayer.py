"""
+--------------------------------------------------------------------------------------+
|                              SPACE SHOOTER - MULTIPLAYER MODULE                      |
|                                Team: இனிழ் (Inizh)                                  |
|                                                                                      |
|  Game level classes containing Multiplayer.                                          |
|  Handles game loop, collision, UI, and game over logic on the multiplayer level.     |
+--------------------------------------------------------------------------------------+
"""

import random
import sys
import time

import pygame
import websockets

import astroid
import bullet
import levels
import ship
from settings import *  # noqa: F403


class multiplayer:
    def __init__(self, main):
        self.screen = main.screen
        self.clock = main.clock
        self.assets = levels.LevelAssets(extended=True)
        self.hud = levels.LevelHUD()
        self.rock = pygame.sprite.Group()
        self.bullet = pygame.sprite.Group()
        self.missle = pygame.sprite.Group()
        self.running = True
        self.score = 0
        self.f_pkl = pygame.font.Font(None, 30)
        self.ship = ship.base_ship(self)
        self.dt = 0
        self.health_bar_colour = "white"
        self.start_colour = time.time()
        self.paused = False
        self.done = False
        self.next_state = "menu"
        self.time = time.time()
        self.missle_time = 0
        self.blast_list = []

    async def run(self):
        self.internet = websockets.connect("ws://localhost:8080/" + self.name)
        await self.internet
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    self.done = True
                    self.next_state = "menu"
                    return
            self.screen.fill((0, 0, 0))
            self.hud.printf(
                self.screen,
                "Press any key to start",
                (SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2),
                "white",
                self.assets.f_uwl_big,
                center=True,
            )
            pygame.display.flip()

        put_astroid = pygame.event.custom_type()
        pygame.time.set_timer(put_astroid, 500)
        pygame.mixer.music.play(loops=-1)
        self.time = time.time()
        while self.running:
            rock_point = random.randint(0, SCREEN_SIZE[0]), random.randint(0, 20)
            missle_point = random.randint(0, SCREEN_SIZE[0]), random.randint(0, 40)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == put_astroid and not self.paused:
                    astroid.Rock(self.rock, rock_point, self.assets.rock_img)
                    self.missle_time += 1
                    if self.missle_time == 4:
                        self.missle_time = 0
                        astroid.Missle(self.missle, missle_point, self.assets.miss_img)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_j:
                        bullet.bullet(
                            self.bullet, self.ship.rect.midtop, self.assets.bul_img
                        )
                        pygame.mixer.Sound.play(self.assets.shoot_eff)
                    if event.key == pygame.K_l:
                        self._heal()

                    if event.key == pygame.K_ESCAPE:
                        self.paused = not self.paused
                        if self.paused:
                            pygame.mixer.music.pause()
                        else:
                            pygame.mixer.music.unpause()

            self._draw()
            self.dt = self.clock.tick()
            if not self.paused:
                self._update()
            else:
                self.hud.printf(
                    self.screen, "PAUSED", (0, 0), "red", self.assets.f_uwl_big, True
                )
            pygame.display.flip()

        else:
            pygame.mixer.music.fadeout(1000)
            self.gameover()
        self.done = True
        self.next_state = "menu"

    def _update(self):
        self.rock.update(self.dt)
        self.ship.update(self.dt)
        self.bullet.update(self.dt)
        self._damage()

    def _draw(self):
        self.screen.fill(BG_COLOR)
        self.screen.blit(self.ship.image, self.ship.rect)
        self.rock.draw(self.screen)
        self.bullet.draw(self.screen)
        self._blast_draw()
        self.hud.draw(self)

    def _damage(self):
        if pygame.sprite.spritecollide(self.ship, self.rock, True):
            pygame.mixer.Sound.play(self.assets.rock_impact)
            self.ship.Hp -= 5
            self.health_bar_colour = "red"
            self.start_colour = time.time()

        if pygame.sprite.groupcollide(self.bullet, self.rock, True, True):
            self.score += 1
            pygame.mixer.Sound.play(self.assets.rock_exp_eff)

        if self.ship.Hp <= 0:
            self.running = False

        if round(time.time() - self.start_colour, 1) == 0.3:
            self.health_bar_colour = "white"

    def _heal(self):
        if self.score >= 10 and self.ship.Hp < 95:
            self.score -= 10
            self.ship.Hp += 5
            self.health_bar_colour = "blue"
            self.start_colour = time.time()
            pygame.mixer.Sound.play(self.assets.ship_heal_eff)

    def gameover(self):
        runit = True
        i = 0
        finish_time = time.time() - self.time
        while runit:
            self.screen.fill(BG_COLOR)
            self.screen.blit(self.ship.image, self.ship.rect)
            self.rock.draw(self.screen)
            self.hud.printf(
                self.screen, "GAME OVER", (0, 0), "white", self.assets.f_uwl_big, True
            )
            self.hud.printf(
                self.screen, "Press Space to continue", (10, 500), "white", self.f_pkl
            )
            self.hud.printf(
                self.screen,
                f" You survived for {round(finish_time, 2)} seconds",
                (10, 200),
                "red",
                self.f_pkl,
            )
            self.clock.tick(60)
            self.hud.draw(self)
            if i < len(self.assets.blast_anime):
                self.screen.blit(self.assets.blast_anime[i], self.ship.rect)
                i += 1
            self.rock.update(self.dt)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        runit = False

    def _blast_draw(self):
        for blast in self.blast_list[::-1]:
            if blast[0] == 51:
                self.blast_list.remove(blast)

        for blast in self.blast_list:
            self.screen.blit(self.assets.blast_anime[blast[0] % 51], blast[1])
            blast[0] += 1