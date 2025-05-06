from __future__ import annotations

__all__ = ["TEXTURE_DICT"]

import arcade


PATH_CONSTANT = "sprites/soldier_1/"
IDLE = PATH_CONSTANT + "Idle.png"
WALK = PATH_CONSTANT + "Walk.png"
RUN = PATH_CONSTANT + "Run.png"
MELEE = PATH_CONSTANT + "Melee.png"
HIP_FIRE = PATH_CONSTANT + "Hip_shooting.png"
AIM_FIRE = PATH_CONSTANT + "Aimed_down_shooting.png"
CROUCHED_FIRE = PATH_CONSTANT + "Crouched_shooting.png"
RELOAD = PATH_CONSTANT + "Reload.png"
GRENADE = PATH_CONSTANT + "Grenade.png"
ALERT = PATH_CONSTANT + "Alert.png"
HURT = PATH_CONSTANT + "Hurt.png"
DEATH = PATH_CONSTANT + "Death.png"

IDLE_SPRITESHEET = arcade.load_spritesheet(IDLE)
WALK_SPRITESHEET = arcade.load_spritesheet(WALK)
RUN_SPRITESHEET = arcade.load_spritesheet(RUN)
MELEE_SPRITESHEET = arcade.load_spritesheet(MELEE)
HIP_FIRE_SPRITESHEET = arcade.load_spritesheet(HIP_FIRE)
AIM_FIRE_SPRITESHEET = arcade.load_spritesheet(AIM_FIRE)
CROUCHED_FIRE_SPRITESHEET = arcade.load_spritesheet(CROUCHED_FIRE)
RELOAD_SPRITESHEET = arcade.load_spritesheet(RELOAD)
GRENADE_SPRITESHEET = arcade.load_spritesheet(GRENADE)
ALERT_SPRITESHEET = arcade.load_spritesheet(ALERT)
HURT_SPRITESHEET = arcade.load_spritesheet(HURT)
DEATH_SPRITESHEET = arcade.load_spritesheet(DEATH)

TEXTURE_CANVAS = (256, 128)
IDLE_TEXTURE_GRID = IDLE_SPRITESHEET.get_texture_grid(TEXTURE_CANVAS, 7, 7)
WALK_TEXTURE_GRID = WALK_SPRITESHEET.get_texture_grid(TEXTURE_CANVAS, 7, 7)
RUN_TEXTURE_GRID = RUN_SPRITESHEET.get_texture_grid(TEXTURE_CANVAS, 8, 8)
MELEE_TEXTURE_GRID = MELEE_SPRITESHEET.get_texture_grid(TEXTURE_CANVAS, 3, 3)
HIP_FIRE_TEXTURE_GRID = HIP_FIRE_SPRITESHEET.get_texture_grid(TEXTURE_CANVAS, 6, 6)
AIM_FIRE_TEXTURE_GRID = AIM_FIRE_SPRITESHEET.get_texture_grid(TEXTURE_CANVAS, 6, 6)
CROUCHED_FIRE_TEXTURE_GRID = CROUCHED_FIRE_SPRITESHEET.get_texture_grid(TEXTURE_CANVAS, 6, 6)
RELOAD_TEXTURE_GRID = RELOAD_SPRITESHEET.get_texture_grid(TEXTURE_CANVAS, 13, 13)
GRENADE_TEXTURE_GRID = GRENADE_SPRITESHEET.get_texture_grid(TEXTURE_CANVAS, 9, 9)
ALERT_TEXTURE_GRID = ALERT_SPRITESHEET.get_texture_grid(TEXTURE_CANVAS, 4, 4)
HURT_TEXTURE_GRID = HURT_SPRITESHEET.get_texture_grid(TEXTURE_CANVAS, 3, 3)
DEATH_TEXTURE_GRID = DEATH_SPRITESHEET.get_texture_grid(TEXTURE_CANVAS, 10, 10)

IDLE_TEXTURES = [(texture, texture.flip_left_right()) for texture in IDLE_TEXTURE_GRID]
WALK_TEXTURES = [(texture, texture.flip_left_right()) for texture in WALK_TEXTURE_GRID]
RUN_TEXTURES = [(texture, texture.flip_left_right()) for texture in RUN_TEXTURE_GRID]
MELEE_TEXTURES = [(texture, texture.flip_left_right()) for texture in MELEE_TEXTURE_GRID]
HIP_FIRE_TEXTURES = [(texture, texture.flip_left_right()) for texture in HIP_FIRE_TEXTURE_GRID]
AIM_FIRE_TEXTURES = [(texture, texture.flip_left_right()) for texture in AIM_FIRE_TEXTURE_GRID]
CROUCHED_FIRE_TEXTURES = [(texture, texture.flip_left_right()) for texture in CROUCHED_FIRE_TEXTURE_GRID]
RELOAD_TEXTURES = [(texture, texture.flip_left_right()) for texture in RELOAD_TEXTURE_GRID]
GRENADE_TEXTURES = [(texture, texture.flip_left_right()) for texture in GRENADE_TEXTURE_GRID]
ALERT_TEXTURES = [(texture, texture.flip_left_right()) for texture in ALERT_TEXTURE_GRID]
HURT_TEXTURES = [(texture, texture.flip_left_right()) for texture in HURT_TEXTURE_GRID]
DEATH_TEXTURES = [(texture, texture.flip_left_right()) for texture in DEATH_TEXTURE_GRID]

TEXTURE_DICT = {
    "idle": IDLE_TEXTURES,
    "walk": WALK_TEXTURES,
    "run": RUN_TEXTURES,
    "melee": MELEE_TEXTURES,
    "shoot": AIM_FIRE_TEXTURES,
    "hip_shoot": HIP_FIRE_TEXTURES,
    "crouched_shoot": CROUCHED_FIRE_TEXTURES,
    "grenade": GRENADE_TEXTURES,
    "reload": RELOAD_TEXTURES,
    "alert": ALERT_TEXTURES,
    "hurt": HURT_TEXTURES,
    "dead": DEATH_TEXTURES,
    "at_ease": IDLE_TEXTURES
}