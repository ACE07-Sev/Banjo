from __future__ import annotations

__all__ = ["SCENE", "PLATFORMS"]

import arcade

TILE_SCALE = 1.5


LAYER_OPTIONS = {
    "Concrete ground - Platform": {"use_spatial_hash": True},
    "Sewer ground - Platform": {"use_spatial_hash": True},
    "River ground - Platform": {"use_spatial_hash": True}
}

TILE_MAP = arcade.load_tilemap(
    "./tiled/map.tmx",
    scaling=TILE_SCALE,
    layer_options=LAYER_OPTIONS
)
SCENE = arcade.Scene.from_tilemap(TILE_MAP)

PLATFORMS = [
    SCENE["Concrete ground - Platform"],
    SCENE["Sewer ground - Platform"],
    SCENE["River ground - Platform"]
]