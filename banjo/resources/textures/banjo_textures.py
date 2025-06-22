from __future__ import annotations

__all__ = ["TEXTURE_DICT"]

import arcade


PATH_CONSTANT = "sprites/banjo/"
IDLE = PATH_CONSTANT + "Banjo_idle.png"
WALK = PATH_CONSTANT + "Banjo_walk.png"
TURN = PATH_CONSTANT + "Banjo_turn.png"
BARK = PATH_CONSTANT + "Banjo_bark.png"
MELEE = PATH_CONSTANT + "Banjo_melee.png"
DEATH = PATH_CONSTANT + "Banjo_death.png"

IDLE_SPRITESHEET = arcade.load_spritesheet(IDLE)
WALKING_SPRITESHEET = arcade.load_spritesheet(WALK)
TURN_SPRITE = arcade.load_texture(TURN)
BARKING_SPRITESHEET = arcade.load_spritesheet(BARK)
MELEE_SPRITESHEET = arcade.load_spritesheet(MELEE)
DEATH_SPRITESHEET = arcade.load_spritesheet(DEATH)

IDLE_TEXTURE_GRID = IDLE_SPRITESHEET.get_texture_grid((200, 200), 4, 4)
WALK_TEXTURE_GRID = WALKING_SPRITESHEET.get_texture_grid((200, 200), 5, 5)
TURN_TEXTURE_GRID = TURN_SPRITE
BARK_TEXTURE_GRID = BARKING_SPRITESHEET.get_texture_grid((200, 200), 4, 4)
MELEE_TEXTURE_GRID = MELEE_SPRITESHEET.get_texture_grid((200, 200), 7, 7)
DEATH_TEXTURE_GRID = DEATH_SPRITESHEET.get_texture_grid((220, 240), 10, 10)

IDLE_TEXTURES = [(texture, texture.flip_left_right()) for texture in IDLE_TEXTURE_GRID]
WALK_TEXTURES = [(texture, texture.flip_left_right()) for texture in WALK_TEXTURE_GRID]
TURN_TEXTURE = [(TURN_TEXTURE_GRID, TURN_TEXTURE_GRID.flip_left_right())]
BARK_TEXTURES = [(texture, texture.flip_left_right()) for texture in BARK_TEXTURE_GRID]
MELEE_TEXTURES = [(texture, texture.flip_left_right()) for texture in MELEE_TEXTURE_GRID]
DEATH_TEXTURES = [(texture, texture.flip_left_right()) for texture in DEATH_TEXTURE_GRID]

TEXTURE_DICT = {
    "idle": IDLE_TEXTURES,
    "walk": WALK_TEXTURES,
    "turn": TURN_TEXTURE,
    "bark": BARK_TEXTURES,
    "melee": MELEE_TEXTURES,
    "dead": DEATH_TEXTURES
}