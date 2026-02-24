"""
+--------------------------------------------------------------------------------------+
|                              SPACE SHOOTER - SETTINGS                                |
|                                Team: இனிழ் (Inizh)                                  |
|                                                                                      |
|  Game configuration constants and global settings.                                   |
|  Screen size, colors, speeds, and FPS settings.                                      |
+--------------------------------------------------------------------------------------+
"""

from os.path import join

# ========================= GAME SETTINGS =========================
SCREEN_SIZE: tuple[int, int] = (1280, 720)
BG_COLOR: str = "#00b5e2"
MOVEMENT_SPEED: float = 1
BULLET_SPEED: float = 2
ASTROID_SPEED: float = 0.5
MISSLE_SPEED: float = 4
FPS : int = 144
STATE : str = "menu"

# ========================= IMAGE PATHS =========================
IMG_LOGO = join("images", "logo.jpg")
IMG_MENU_BG = join("images", "menu_bg.jpeg")
IMG_BACKGROUND = join("images", "proto#background.bmp")
IMG_SHIP = join("images", "proto#ship.png")
IMG_SHIP_F14A = join("images", "ship", "F-14A.png")
IMG_BULLET = join("images", "proto#bullet.png")
IMG_ASTROID = join("images", "proto#astroid.png")
IMG_ASTROID_GREY = join("images", "astroid_grey.png")
IMG_MISSILE = join("images", "missile.png")
IMG_CLOUD_UNDER = join("images", "cloud", "under_cloud.png")
IMG_CLOUD_OVER = join("images", "cloud", "over_cloud.png")
IMG_BLAST_DIR = join("images", "blast_anime1")

# ========================= FONT PATHS =========================
FONT_VT323 = join("fonts", "VT323-Regular.ttf")
FONT_UNWAVE = join("fonts", "UnwaveLover-PV9AZ.otf")
FONT_TAMIL = join("fonts", "tamil.ttf")

# ========================= AUDIO PATHS =========================
AUDIO_BGM = join("audio", "Project_Space Shooter_Final_Loop.mp3")
AUDIO_SHOOT = join("audio", "Space Shooter_Fire.mp3")
AUDIO_EXPLOSION = join("audio", "Space Shooter_Explosion.mp3")
AUDIO_IMPACT = join("audio", "Space Shooter_Asteroid Impact.mp3")
AUDIO_HEAL = join("audio", "Space Shooter_Healing.mp3")