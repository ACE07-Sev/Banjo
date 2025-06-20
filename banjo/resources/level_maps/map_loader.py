from __future__ import annotations

__all__ = [
    "TILE_SCALE",
    "LAYER_OPTIONS",
    "TILE_MAP",
    "SCENE",
    "PLATFORMS",
    "load_tilemap",
    "load_scene",
    "load_platforms"
]

import arcade


# Pre-loaded map constants
LAYER_OPTIONS = {
    "Concrete ground - Platform": {"use_spatial_hash": True},
    "Sewer ground - Platform": {"use_spatial_hash": True},
    "River ground - Platform": {"use_spatial_hash": True}
}

TILE_SCALE = 1.5
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

# Loaders for re-creating the constants
# This is useful for when we need to re-create the map
def load_tilemap() -> arcade.TileMap:
    return arcade.load_tilemap(
        "./tiled/map.tmx",
        scaling=TILE_SCALE,
        layer_options=LAYER_OPTIONS
    )

def load_scene(tile_map: arcade.TileMap) -> arcade.Scene:
    return arcade.Scene.from_tilemap(tile_map)

def load_platforms(scene: arcade.Scene) -> list[arcade.SpriteList]:
    return [
        scene["Concrete ground - Platform"],
        scene["Sewer ground - Platform"],
        scene["River ground - Platform"]
    ]