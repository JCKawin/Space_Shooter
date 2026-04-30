import random
import sys
import time
from os.path import join

import pygame
import websockets

import astroid
import bullet
import cloud
import ship
from settings import *


class multiplayer:
    def __init__(self, main):
        self.screen = main.screen
        self.load_asserts()
        self.clock = main.clock  # Clock Variable
        self.rock = pygame.sprite.Group()  # Group for asteroids
        self.bullet = pygame.sprite.Group()  # Group for bullets
        self.missle = pygame.sprite.Group()  # Group for Missles
        self.under_cloud = pygame.sprite.Group()  # clouds under the airplane
        self.over_cloud = pygame.sprite.Group()  # clouds over the airplalne
        self.f_pkl = pygame.font.Font(None, 30)
        self.ship = ship.f14a(self)  # Player's ship
        self.dt = main.dt
        self.internet = websockets.connect("ws://localhost:8080/" + self.name)
        self.running = main.running
        self.score = 0
        self.health_bar_colour = "white"
        self.start_colour = time.time()
        self.time = time.time()
        self.finish_time = time.time()
        self.paused = False
        self.missle_time = 0
        self.blast_list = []
        self.todel_blast = []

    def load_asserts(self):
        self.blast_anime = []
        for i in range(1, 51):
            self.blast_anime.append(
                pygame.image.load(join(IMG_BLAST_DIR, f"blast ({i}).png"))
            )
        # Load images, fonts, and sounds
        self.background = pygame.image.load(IMG_BACKGROUND)
        self.f_uwl_big = pygame.font.Font(FONT_VT323, 360)
        self.f_uwl = pygame.font.Font(FONT_VT323, 30)
        self.bul_img = pygame.image.load(IMG_BULLET).convert_alpha()
        self.rock_img = pygame.image.load(IMG_ASTROID_GREY).convert_alpha()
        self.rock_img = pygame.transform.scale(self.rock_img, (64, 64))
        self.miss_img = pygame.image.load(IMG_MISSILE).convert_alpha()
        self.miss_img = pygame.transform.scale(self.miss_img, (32, 128))
        self.under_cloud_img = pygame.image.load(IMG_CLOUD_UNDER).convert_alpha()
        self.over_cloud_img = pygame.image.load(IMG_CLOUD_OVER).convert_alpha()
        self.bgm = pygame.mixer.music.load(AUDIO_BGM)
        pygame.mixer.music.set_volume(0.5)
        self.shoot_eff = pygame.mixer.Sound(AUDIO_SHOOT)
        self.rock_exp_eff = pygame.mixer.Sound(AUDIO_EXPLOSION)
        self.rock_impact = pygame.mixer.Sound(AUDIO_IMPACT)
        self.ship_heal_eff = pygame.mixer.Sound(AUDIO_HEAL)

    def run(self):
        # Main game loop
        put_astroid = pygame.event.custom_type()
        pygame.time.set_timer(put_astroid, 500)
        pygame.mixer.music.play(loops=-1)
        self.time = time.time()
        cloud.cloud(self.under_cloud, self.under_cloud_img)
        while self.running:
            rock_point = random.randint(0, SCREEN_SIZE[0]), random.randint(0, 20)
            missle_point = random.randint(0, SCREEN_SIZE[0]), random.randint(0, 40)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == put_astroid and not self.paused:
                    astroid.Rock(self.rock, rock_point, self.rock_img)
                    self.missle_time += 1
                    if self.missle_time == 4:
                        self.missle_time = 0
                        astroid.Missle(self.missle, missle_point, self.miss_img)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_j:
                        bullet.bullet(self.bullet, self.ship.rect.midtop, self.bul_img)
                        pygame.mixer.Sound.play(self.shoot_eff)
                    if event.key == pygame.K_l:
                        self._heal()

                    if event.key == pygame.K_ESCAPE:
                        self.paused = not self.paused
                        pygame.mixer.music.pause() if self.paused else pygame.mixer.music.unpause()
            if not bool(len(self.under_cloud)):
                cloud.cloud(self.under_cloud, self.under_cloud_img)
            if not bool(len(self.over_cloud)):
                cloud.cloud(self.over_cloud, self.over_cloud_img)
            self.screen.fill(BG_COLOR)
            self.under_cloud.draw(self.screen)
            self.screen.blit(self.ship.image, self.ship.rect)
            self.over_cloud.draw(self.screen)
            self.rock.draw(self.screen)
            self.bullet.draw(self.screen)
            self.missle.draw(self.screen)
            self._blast_draw()
            self._UI()
            self.dt = self.clock.tick()
            if not self.paused:
                self.under_cloud.update(0.1, self.dt)
                self.over_cloud.update(0.15, self.dt)
                self.rock.update(self.dt)
                self.ship.update(self.dt)
                self.bullet.update(self.dt)
                self.missle.update(self.dt)
                self._damage()
            else:
                self.printf(self.screen, "PAUSED", (0, 0), "red", self.f_uwl_big, True)
            pygame.display.flip()

        else:
            pygame.mixer.music.fadeout(1000)
            self.gameover()
            self._reset()
        return "menu"

    def _damage(self):
        # Handle collisions and update health/score
        if pygame.sprite.spritecollide(self.ship, self.rock, True):
            pygame.mixer.Sound.play(self.rock_impact)
            self.ship.Hp -= 5
            self.health_bar_colour = "red"
            self.start_colour = time.time()

        if pygame.sprite.groupcollide(self.bullet, self.rock, True, True):
            self.score += 1
            pygame.mixer.Sound.play(self.rock_exp_eff)

        if pygame.sprite.spritecollide(self.ship, self.missle, True):
            pygame.mixer.Sound.play(self.rock_impact)
            self.ship.Hp -= 100
            self.health_bar_colour = "black"
            self.start_colour = time.time()

        if self.ship.Hp <= 0:
            self.running = False

        # Reset health bar color after short time
        if round(time.time() - self.start_colour, 1) == 0.3:
            self.health_bar_colour = "white"

    def _heal(self):
        # Heal ship if enough score
        if self.score >= 10 and self.ship.Hp < 95:
            self.score -= 10
            self.ship.Hp += 5
            self.health_bar_colour = "blue"
            self.start_colour = time.time()
            pygame.mixer.Sound.play(self.ship_heal_eff)

    def _UI(self):
        # Draw health bar and game info
        healthbar = pygame.rect.Rect(30, SCREEN_SIZE[1] - 50, self.ship.Hp * 4, 20)
        pygame.draw.rect(self.screen, self.health_bar_colour, healthbar)
        self.printf(
            self.screen,
            f"health {self.ship.Hp}",
            (34, SCREEN_SIZE[1] - 55),
            "black",
            self.f_uwl,
        )
        self.printf(
            self.screen,
            f"FPS: {round(self.clock.get_fps(), 0)}",
            (30, 30),
            "black",
            self.f_pkl,
        )
        self.printf(
            self.screen,
            f"Score : {self.score}",
            (SCREEN_SIZE[0] - 120, 20),
            "black",
            self.f_pkl,
        )
        if self.running:
            self.printf(
                self.screen,
                f"played : {time.time() - self.time: .2f} sec",
                (SCREEN_SIZE[0] - 200, SCREEN_SIZE[1] - 30),
                "black",
                self.f_pkl,
            )

    def _reset(self):
        self.running = True
        self.score = 0
        self.health_bar_colour = "white"
        self.ship.Hp = 100

    def gameover(self):
        # Game over screen loop
        runit = True
        i = 0
        self.finish_time = time.time() - self.time
        while runit:
            self.screen.fill(BG_COLOR)
            self.screen.blit(self.ship.image, self.ship.rect)
            self.rock.draw(self.screen)
            self.printf(self.screen, "GAME OVER", (0, 0), "white", self.f_uwl_big, True)
            self.printf(
                self.screen, "Press Space to continue", (10, 500), "white", self.f_pkl
            )
            self.printf(
                self.screen,
                f" You survived for {round(self.finish_time, 2)} seconds",
                (10, 200),
                "red",
                self.f_pkl,
            )
            self.clock.tick(60)
            self._UI()
            if i < len(self.blast_anime):
                self.screen.blit(self.blast_anime[i], self.ship.rect)
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
        for i in self.blast_list[::-1]:
            if i[0] == 51:
                self.blast_list.remove(i)

        for i in self.blast_list:
            self.screen.blit(self.blast_anime[i[0] % 51], i[1])
            i[0] += 1

    @staticmethod
    def printf(screen, text, rect, colour, font, center: bool = False):
        # Draw text on screen
        tex = font.render(text, True, colour)
        tex_rect = tex.get_rect()
        tex_rect.topleft = rect
        if center:
            tex_rect.center = screen.get_rect().center
        screen.blit(tex, tex_rect)
