from __future__ import annotations

__all__ = ["Banjo"]

import arcade

# Constants
DEAD_ZONE = 0.01
RIGHT_FACING = 0
LEFT_FACING = 1
DISTANCE_TO_CHANGE_TEXTURE = 3
WALKING_VELOCITY = 1000

PATH_CONSTANT = "sprites/banjo/"
BANJO_IDLE = PATH_CONSTANT + "Banjo_idle.png"
BANJO_WALK = PATH_CONSTANT + "Banjo_walk.png"
BANJO_TURN = PATH_CONSTANT + "Banjo_turn.png"
BANJO_BARK = PATH_CONSTANT + "Banjo_bark.png"
BANJO_MELEE = PATH_CONSTANT + "Banjo_melee.png"
BANJO_DEATH = PATH_CONSTANT + "Banjo_death.png"

BANJO_IDLE_SPRITESHEET = arcade.load_spritesheet(BANJO_IDLE)
BANJO_WALKING_SPRITESHEET = arcade.load_spritesheet(BANJO_WALK)
BANJO_TURN_SPRITE = arcade.load_texture(BANJO_TURN)
BANJO_BARKING_SPRITESHEET = arcade.load_spritesheet(BANJO_BARK)
BANJO_MELEE_SPRITESHEET = arcade.load_spritesheet(BANJO_MELEE)
BANJO_DEATH_SPRITESHEET = arcade.load_spritesheet(BANJO_DEATH)


class Banjo(arcade.Sprite):
    """ `banjo.Banjo` is the class that represents the player
    controlled character in the game. It is a subclass of
    `arcade.Sprite` and has additional functionality to handle
    walking, barking, and melee attacks.

    Notes
    -----
    Mutated from the factory runoff, Banjo is a vicious amphibian
    that only knows how to kill. Banjo was originally a peaceful
    Banjo-frog that lived in the swamp. Being the social creatures
    that they are, Banjo-frogs would often gather in large groups
    down by the river. Whilst Banjo was mutated, he still retains
    the urge to move downstream.

    Banjo is approximately 800 KG, 3 meters tall, and has razor
    sharp teeth and claws. Banjo is a carnivore and will eat
    anything that moves. Banjo moves through the sewers and only
    surfaces to feed. Due to his size and mutation, he must frequently
    feed to keep up with his metabolism. Banjo also needs to keep
    his skin moist, so he must stay near water.

    Banjo is a formidable opponent, however, he is not invincible.
    Banjo has 100 health points and can deal 10 damage with each
    attack. He cannot withstand gunfire consistently and will die
    if he is shot enough times. Banjo is also susceptible to
    explosions and will die if he is caught in one.

    Attributes
    ----------
    `idle_textures` : list[tuple[arcade.Texture, arcade.Texture]]
        A list of tuples where each tuple contains a texture facing
        left and a texture facing right. These textures are used
        for the idle animation.
    `walk_textures` : list[tuple[arcade.Texture, arcade.Texture]]
        A list of tuples where each tuple contains a texture facing
        left and a texture facing right. These textures are used
        for the walking animation.
    `turn_texture` : tuple[arcade.Texture, arcade.Texture]
        A tuple containing a texture facing left and a texture facing
        right. These textures are used for the turning animation.
    `bark_textures` : list[tuple[arcade.Texture, arcade.Texture]]
        A list of tuples where each tuple contains a texture facing
        left and a texture facing right. These textures are used
        for the barking animation.
    `melee_textures` : list[tuple[arcade.Texture, arcade.Texture]]
        A list of tuples where each tuple contains a texture facing
        left and a texture facing right. These textures are used
        for the melee attack animation.
    `death_textures` : list[tuple[arcade.Texture, arcade.Texture]]
        A list of tuples where each tuple contains a texture facing
        left and a texture facing right. These textures are used
        for the death animation.
    `not_idle` : bool
        A boolean representing whether the player is idle or not.
    `hp` : int
        The player's health points.
    `attack` : int
        The player's attack power.
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

        idle_textures = BANJO_IDLE_SPRITESHEET.get_texture_grid((200, 200), 4, 4)
        walk_textures = BANJO_WALKING_SPRITESHEET.get_texture_grid((200, 200), 5, 5)
        turn_texture = BANJO_TURN_SPRITE
        bark_textures = BANJO_BARKING_SPRITESHEET.get_texture_grid((200, 200), 5, 5)
        melee_textures = BANJO_MELEE_SPRITESHEET.get_texture_grid((200, 200), 7, 7)
        death_textures = BANJO_DEATH_SPRITESHEET.get_texture_grid((220, 240), 10, 10)

        self.idle_textures = [(texture, texture.flip_left_right()) for texture in idle_textures]
        self.walk_textures = [(texture, texture.flip_left_right()) for texture in walk_textures]
        self.turn_texture = (turn_texture, turn_texture.flip_left_right())
        self.bark_textures = [(texture, texture.flip_left_right()) for texture in bark_textures]
        self.melee_textures = [(texture, texture.flip_left_right()) for texture in melee_textures]
        self.death_textures = [(texture, texture.flip_left_right()) for texture in death_textures]

        self.not_idle = False
        self.hp = 100
        self.attack = 10
        self.texture = self.walk_textures[0][0]
        self.character_face_direction = RIGHT_FACING
        self.current_texture = 0
        self.x_odometer = 0

    def idle(self) -> None:
        """ Play the idle animation.

        Usage
        -----
        >>> player.idle()
        """
        if self.current_texture > 3:
            self.current_texture = 0
        self.texture = self.idle_textures[self.current_texture][self.character_face_direction]
        self.current_texture += 1

    def walk(self) -> None:
        """ Play the walking animation.

        Usage
        -----
        >>> player.walk()
        """
        if self.current_texture > 4:
            self.current_texture = 0
        self.texture = self.walk_textures[self.current_texture][self.character_face_direction]
        self.current_texture += 1

    def turn(
            self,
            direction: int
        ) -> None:
        """ Play the turning animation.

        Parameters
        ----------
        `direction` : int
            The direction the player is turning. 0 for right, 1 for left.

        Usage
        -----
        >>> player.turn(0)
        """
        self.character_face_direction = direction
        self.texture = self.turn_texture[abs(direction - 1)]

    def bark(self) -> None:
        """ Play the barking animation.

        Usage
        -----
        >>> player.bark()
        """
        self.not_idle = True
        if self.current_texture > 4:
            self.current_texture = 0
        self.texture = self.bark_textures[self.current_texture][self.character_face_direction]
        self.current_texture += 1

    def melee(self) -> None:
        """ Play the melee attack animation.

        Usage
        -----
        >>> player.melee()
        """
        self.not_idle = True
        if self.current_texture > 6:
            self.current_texture = 0
        self.texture = self.melee_textures[self.current_texture][self.character_face_direction]
        self.current_texture += 1

    def death(self) -> None:
        """ Play the death animation.

        Usage
        -----
        >>> player.death()
        """
        self.hp = 0
        self.not_idle = True
        if self.current_texture > 9:
            return
        self.texture = self.death_textures[self.current_texture][self.character_face_direction]
        self.current_texture += 1

    def pymunk_moved(
            self,
            physics_engine: arcade.PymunkPhysicsEngine,
            dx: float,
            dy: float,
            d_angle: float
        ) -> None:

        if self.hp == 0:
            return

        if abs(dx) <= DEAD_ZONE and not self.not_idle:
            self.idle()
            return

        if dx < -DEAD_ZONE and self.character_face_direction == RIGHT_FACING:
            self.turn(LEFT_FACING)
            return
        elif dx > DEAD_ZONE and self.character_face_direction == LEFT_FACING:
            self.turn(RIGHT_FACING)
            return

        self.x_odometer += dx

        if abs(self.x_odometer) > DISTANCE_TO_CHANGE_TEXTURE:
            self.x_odometer = 0
            self.walk()