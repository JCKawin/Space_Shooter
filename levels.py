"""
+--------------------------------------------------------------------------------------+
|                              SPACE SHOOTER - LEVELS MODULE                           |
|                                Team: இனிழ் (Inizh)                                  |
|                                                                                      |
|  Game level classes containing difficulty modes (Easy, Medium).                      |
|  Handles game loop, collision, UI, and game over logic.                              |
+--------------------------------------------------------------------------------------+
"""

import random
import sys
import time
from dataclasses import dataclass
from os.path import join
from typing import Callable

import pygame

import astroid
import bullet
import cloud
import ship
from settings import *


@dataclass(frozen=True)
class LevelConfig:
    ship_factory: Callable
    extended_assets: bool = False
    spawn_missiles: bool = False
    use_clouds: bool = False
    backgrond_image: bool = True

class LevelAssets:
    def __init__(self, extended: bool = False):
        self.load_base()
        if extended:
            self.load_medium()

    def load_base(self):
        self.background = pygame.image.load(IMG_BACKGROUND)
        self.f_uwl_big = pygame.font.Font(FONT_VT323, 360)
        self.f_uwl = pygame.font.Font(FONT_VT323, 30)
        self.bul_img = pygame.image.load(IMG_BULLET).convert_alpha()
        self.rock_img = pygame.image.load(IMG_ASTROID).convert_alpha()
        self.rock_img = pygame.transform.scale(self.rock_img, (64, 64))
        self.bgm = pygame.mixer.music.load(AUDIO_BGM)
        pygame.mixer.music.set_volume(0.5)
        self.shoot_eff = pygame.mixer.Sound(AUDIO_SHOOT)
        self.rock_exp_eff = pygame.mixer.Sound(AUDIO_EXPLOSION)
        self.rock_impact = pygame.mixer.Sound(AUDIO_IMPACT)
        self.ship_heal_eff = pygame.mixer.Sound(AUDIO_HEAL)

    def load_medium(self):
        self.blast_anime = []
        for i in range(1, 51):
            self.blast_anime.append(
                pygame.image.load(join(IMG_BLAST_DIR, f"blast ({i}).png"))
            )
        self.miss_img = pygame.image.load(IMG_MISSILE).convert_alpha()
        self.miss_img = pygame.transform.scale(self.miss_img, (32, 128))
        self.under_cloud_img = pygame.image.load(IMG_CLOUD_UNDER).convert_alpha()
        self.over_cloud_img = pygame.image.load(IMG_CLOUD_OVER).convert_alpha()


class LevelHUD:
    @staticmethod
    def printf(screen, text, rect, colour, font, center: bool = False):
        tex = font.render(text, True, colour)
        tex_rect = tex.get_rect()
        tex_rect.topleft = rect
        if center:
            tex_rect.center = screen.get_rect().center
        screen.blit(tex, tex_rect)

    def draw(self, level):
        healthbar = pygame.rect.Rect(30, SCREEN_SIZE[1] - 50, level.ship.Hp * 4, 20)
        pygame.draw.rect(level.screen, level.health_bar_colour, healthbar)
        self.printf(
            level.screen,
            f"health {level.ship.Hp}",
            (34, SCREEN_SIZE[1] - 55),
            "black",
            level.assets.f_uwl,
        )
        self.printf(
            level.screen,
            f"FPS: {round(level.clock.get_fps(), 0)}",
            (30, 30),
            "black",
            level.f_pkl,
        )
        self.printf(
            level.screen,
            f"Score : {level.score}",
            (SCREEN_SIZE[0] - 120, 20),
            "white",
            level.f_pkl,
        )
        if level.running:
            self.printf(
                level.screen,
                f"played : {time.time() - level.time: .2f} sec",
                (SCREEN_SIZE[0] - 200, SCREEN_SIZE[1] - 30),
                "white",
                level.f_pkl,
            )


class LevelCollision:
    @staticmethod
    def process_easy(level):
        if pygame.sprite.spritecollide(level.ship, level.rock, True):
            pygame.mixer.Sound.play(level.assets.rock_impact)
            level.ship.Hp -= 5
            level.health_bar_colour = "red"
            level.start_colour = time.time()

        if pygame.sprite.groupcollide(level.bullet, level.rock, True, True):
            level.score += 1
            pygame.mixer.Sound.play(level.assets.rock_exp_eff)

        if level.ship.Hp <= 0:
            level.running = False

        if round(time.time() - level.start_colour, 1) == 0.3:
            level.health_bar_colour = "white"

    @staticmethod
    def process_medium(level):
        if pygame.sprite.spritecollide(level.ship, level.rock, True):
            pygame.mixer.Sound.play(level.assets.rock_impact)
            level.ship.Hp -= 5
            level.health_bar_colour = "red"
            level.start_colour = time.time()

        if pygame.sprite.groupcollide(level.bullet, level.rock, True, True):
            level.score += 1
            pygame.mixer.Sound.play(level.assets.rock_exp_eff)

        if pygame.sprite.spritecollide(level.ship, level.missle, True):
            pygame.mixer.Sound.play(level.assets.rock_impact)
            level.ship.Hp -= 100
            level.health_bar_colour = "black"
            level.start_colour = time.time()

        if level.ship.Hp <= 0:
            level.running = False

        if round(time.time() - level.start_colour, 1) == 0.3:
            level.health_bar_colour = "white"


class LevelRenderer:
    @staticmethod
    def draw_easy(level):
        level.screen.fill(BG_COLOR)
        level.screen.blit(level.assets.background, (0, 0))
        level.screen.blit(level.ship.image, level.ship.rect)
        level.rock.draw(level.screen)
        level.bullet.draw(level.screen)

    @staticmethod
    def draw_medium(level):
        level.screen.fill(BG_COLOR)
        level.under_cloud.draw(level.screen)
        level.screen.blit(level.ship.image, level.ship.rect)
        level.over_cloud.draw(level.screen)
        level.rock.draw(level.screen)
        level.bullet.draw(level.screen)
        level.missle.draw(level.screen)
        LevelRenderer._blast_draw(level)

    @staticmethod
    def _blast_draw(level):
        for blast in level.blast_list[::-1]:
            if blast[0] == 51:
                level.blast_list.remove(blast)

        for blast in level.blast_list:
            level.screen.blit(level.assets.blast_anime[blast[0] % 51], blast[1])
            blast[0] += 1


class LevelUpdater:
    @staticmethod
    def update_easy(level):
        level.rock.update(level.dt)
        level.ship.update(level.dt)
        level.bullet.update(level.dt)
        LevelCollision.process_easy(level)

    @staticmethod
    def update_medium(level):
        level.under_cloud.update(0.1, level.dt)
        level.over_cloud.update(0.15, level.dt)
        level.rock.update(level.dt)
        level.ship.update(level.dt)
        level.bullet.update(level.dt)
        level.missle.update(level.dt)
        LevelCollision.process_medium(level)


class GameLevel:
    def __init__(self, main, config: LevelConfig):
        self.config = config
        self.screen = main.screen
        self.clock = main.clock
        self.assets = LevelAssets(extended=config.extended_assets)
        self.hud = LevelHUD()
        self.rock = pygame.sprite.Group()
        self.bullet = pygame.sprite.Group()
        self.running = True
        self.score = 0
        self.f_pkl = pygame.font.Font(None, 30)
        self.ship = config.ship_factory(self)
        self.dt = 0
        self.health_bar_colour = "white"
        self.start_colour = time.time()
        self.paused = False
        self.done = False
        self.next_state = "menu"
        self.time = time.time()

        if config.use_clouds:
            self.missle = pygame.sprite.Group()
            self.under_cloud = pygame.sprite.Group()
            self.over_cloud = pygame.sprite.Group()
            self.missle_time = 0
            self.blast_list = []

        if config.use_clouds:
            self.draw_scene = LevelRenderer.draw_medium
            self.update_world = LevelUpdater.update_medium
        else:
            self.draw_scene = LevelRenderer.draw_easy
            self.update_world = LevelUpdater.update_easy

    def _heal(self):
        if self.score >= 10 and self.ship.Hp < 95:
            self.score -= 10
            self.ship.Hp += 5
            self.health_bar_colour = "blue"
            self.start_colour = time.time()
            pygame.mixer.Sound.play(self.assets.ship_heal_eff)

    def _spawn_on_timer(self, rock_point, missle_point):
        astroid.Rock(self.rock, rock_point, self.assets.rock_img)
        if not self.config.spawn_missiles:
            return

        self.missle_time += 1
        if self.missle_time == 4:
            self.missle_time = 0
            astroid.Missle(self.missle, missle_point, self.assets.miss_img)

    def _ensure_clouds(self):
        if not len(self.under_cloud):
            cloud.cloud(self.under_cloud, self.assets.under_cloud_img)
        if not len(self.over_cloud):
            cloud.cloud(self.over_cloud, self.assets.over_cloud_img)

    def _handle_input(self, event, put_astroid):
        if event.type == put_astroid and not self.paused:
            rock_point = random.randint(0, SCREEN_SIZE[0]), random.randint(0, 20)
            missle_point = random.randint(0, SCREEN_SIZE[0]), random.randint(0, 40)
            self._spawn_on_timer(rock_point, missle_point)

        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_j:
            bullet.bullet(self.bullet, self.ship.rect.midtop, self.assets.bul_img)
            pygame.mixer.Sound.play(self.assets.shoot_eff)
        elif event.key == pygame.K_l:
            self._heal()
        elif event.key == pygame.K_ESCAPE:
            self.paused = not self.paused
            if self.paused:
                pygame.mixer.music.pause()
            else:
                pygame.mixer.music.unpause()

    def gameover(self):
        finish_time = time.time() - self.time
        waiting = True
        while waiting:
            # self.screen.fill(BG_COLOR)
            # self.screen.blit(self.assets.background, (0, 0))
            # self.screen.blit(self.ship.image, self.ship.rect)
            # self.rock.draw(self.screen)

            self.draw_scene(self)
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
            self.clock.tick()
            self.hud.draw(self)
            self.rock.update(self.dt)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    waiting = False

    def _prepare_run(self):
        self.running = True
        self.score = 0
        self.health_bar_colour = "white"
        self.ship.Hp = 100
        self.paused = False
        self.done = False
        self.next_state = "menu"
        self.time = time.time()
        self.start_colour = time.time()
        self.rock.empty()
        self.bullet.empty()

        if self.config.use_clouds:
            self.missle.empty()
            self.under_cloud.empty()
            self.over_cloud.empty()
            self.missle_time = 0
            self.blast_list = []
            cloud.cloud(self.under_cloud, self.assets.under_cloud_img)

    def run(self):
        put_astroid = pygame.event.custom_type()
        pygame.time.set_timer(put_astroid, 500)
        pygame.mixer.music.play(loops=-1)
        self._prepare_run()

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                self._handle_input(event, put_astroid)

            if self.config.use_clouds:
                self._ensure_clouds()

            self.draw_scene(self)
            self.hud.draw(self)
            self.dt = self.clock.tick()

            if not self.paused:
                self.update_world(self)
            else:
                self.hud.printf(
                    self.screen, "PAUSED", (0, 0), "red", self.assets.f_uwl_big, True
                )

            pygame.display.flip()

        pygame.mixer.music.fadeout(1000)
        self.gameover()
        self.done = True
        self.next_state = "menu"


EASY_CONFIG = LevelConfig(ship_factory=ship.base_ship)
MEDIUM_CONFIG = LevelConfig(
    ship_factory=ship.f14a,
    backgrond_image= False,
    extended_assets=True,
    spawn_missiles=True,
    use_clouds=True,
)


class easy:
    def __init__(self, main):
        self._level = GameLevel(main, EASY_CONFIG)

    def run(self):
        return self._level.run()

    @property
    def done(self):
        return self._level.done

    @done.setter
    def done(self, value):
        self._level.done = value

    @property
    def next_state(self):
        return self._level.next_state

    @next_state.setter
    def next_state(self, value):
        self._level.next_state = value


class medium:
    def __init__(self, main):
        self._level = GameLevel(main, MEDIUM_CONFIG)

    def run(self):
        return self._level.run()

    @property
    def done(self):
        return self._level.done

    @done.setter
    def done(self, value):
        self._level.done = value

    @property
    def next_state(self):
        return self._level.next_state

    @next_state.setter
    def next_state(self, value):
        self._level.next_state = value
