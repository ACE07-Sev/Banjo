from __future__ import annotations

__all__ = ["Banjo"]

import arcade

# Constants
DEAD_ZONE = 0.1

RIGHT_FACING = 0
LEFT_FACING = 1

DISTANCE_TO_CHANGE_TEXTURE = 3

PLAYER_MOVE_FORCE_ON_GROUND = 8000

BANJO_WALK = "sprites/Banjo_walk.png"
BANJO_BARK = "sprites/Banjo_bark.png"
BANJO_MELEE = "sprites/Banjo_melee.png"

BANJO_WALKING_SPRITESHEET = arcade.load_spritesheet(BANJO_WALK)
BANJO_BARKING_SPRITESHEET = arcade.load_spritesheet(BANJO_BARK)
BANJO_MELEE_SPRITESHEET = arcade.load_spritesheet(BANJO_MELEE)


class Banjo(arcade.Sprite):
    """ `banjo.Banjo` is the class that represents the player
    controlled character in the game. It is a subclass of
    `arcade.Sprite` and has additional functionality to handle
    walking, barking, and melee attacks.

    Attributes
    ----------
    `walk_textures` : List[Tuple[arcade.Texture, arcade.Texture]]
        A list of tuples where each tuple contains a texture facing
        left and a texture facing right. These textures are used
        for the walking animation.
    `bark_textures` : List[Tuple[arcade.Texture, arcade.Texture]]
        A list of tuples where each tuple contains a texture facing
        left and a texture facing right. These textures are used
        for the barking animation.
    `melee_textures` : List[Tuple[arcade.Texture, arcade.Texture]]
        A list of tuples where each tuple contains a texture facing
        left and a texture facing right. These textures are used
        for the melee attack animation.
    `texture` : arcade.Texture
        The current texture being displayed for the player.
    `character_face_direction` : int
        An integer representing which direction the player is facing.
        0 for right, 1 for left.
    `current_texture` : int
        The index of the current texture being displayed.
    `x_odometer` : float
        How far the player has moved horizontally since the last texture change.

    Usage
    -----
    >>> player = Banjo()
    """
    def __init__(self) -> None:
        """ Initialize the player character.
        """
        super().__init__(scale=1)

        walk_textures = BANJO_WALKING_SPRITESHEET.get_texture_grid((200, 200), 5, 5)
        bark_textures = BANJO_BARKING_SPRITESHEET.get_texture_grid((200, 200), 5, 5)
        melee_textures = BANJO_MELEE_SPRITESHEET.get_texture_grid((200, 200), 7, 7)

        self.walk_textures = [(texture, texture.flip_left_right()) for texture in walk_textures]
        self.bark_textures = [(texture, texture.flip_left_right()) for texture in bark_textures]
        self.melee_textures = [(texture, texture.flip_left_right()) for texture in melee_textures]

        self.texture = self.walk_textures[0][0]
        self.character_face_direction = RIGHT_FACING
        self.current_texture = 0
        self.x_odometer = 0

    def pymunk_moved(
            self,
            physics_engine: arcade.PymunkPhysicsEngine,
            dx: float,
            dy: float,
            d_angle: float
        ) -> None:

        # Figure out if we need to face left or right
        if dx < -DEAD_ZONE and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif dx > DEAD_ZONE and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        # Add to the odometer how far we've moved
        self.x_odometer += dx

        # Have we moved far enough to change the texture?
        if abs(self.x_odometer) > DISTANCE_TO_CHANGE_TEXTURE:
            self.x_odometer = 0

            # Advance the walking animation
            self.current_texture += 1
            if self.current_texture > 4:
                self.current_texture = 0
            self.texture = self.walk_textures[self.current_texture][self.character_face_direction]