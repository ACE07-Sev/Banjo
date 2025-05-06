from __future__ import annotations

__all__ = ["Banjo"]

import arcade
from banjo.resources.game_constants import GRAVITY, RIGHT_FACING
from banjo.resources.level_maps import PLATFORMS
from banjo.resources.textures import BANJO_TEXTURES

# Sounds
BANJO_BARK_SOUND = "sounds/banjo_bark.wav"

# Banjo Constant
HP = 100
ATTACK = 1
HUNGER_RATE = 0.1
DRYING_RATE = 0.1
WALKING_VELOCITY = 5
HEARING_RANGE = 500


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
    `texture_dict` : dict[str, list[tuple[arcade.Texture, arcade.Texture]]]
        The dictionary that contains the textures for the player
        character. The keys are the names of the animations and
        the values are lists of tuples containing the texture and
        its flipped version.
    `hp` : int
        The health points of the player character. The player
        character starts with 100 health points.
    `attack` : int
        The attack points of the player character. The player
        character starts with 10 attack points.
    `hunger_rate` : float
        The rate at which the player character gets hungry.
        The player character starts with 0 hunger points.
    `current_hunger` : int
        The current hunger points of the player character.
        The player character starts with 0 hunger points.
    `max_hunger` : int
        The maximum hunger points of the player character.
        The player character starts with 3 hunger points.
    `drying_rate` : float
        The rate at which the player character gets dry.
        The player character starts with 0 dryness points.
    `current_dryness` : int
        The current dryness points of the player character.
        The player character starts with 0 dryness points.
    `max_dryness` : int
        The maximum dryness points of the player character.
        The player character starts with 3 dryness points.
    `walking_velocity` : int
        The walking velocity of the player character.
        The player character starts with a velocity of 200.
    `friction` : float
        The friction of the player character.
    `mass` : float
        The mass of the player character.
    `is_dying` : bool
        Whether the player character is dying or not.
        The player character starts with False.
    `is_dead` : bool
        Whether the player character is dead or not.
        The player character starts with False.
    `hearing_range` : int
        The maximum distance at which Banjo can clearly
        hear sounds.
    `texture` : arcade.Texture
        The texture of the player character. The player
        character starts with the walking texture.
    `character_facing_direction` : int
        The direction the player character is facing.
        The player character starts facing right.
    `current_animation` : str
        The current animation of the player character.
        The player character starts with the idle animation.
    `current_texture_index` : int
        The current texture index of the player character.
        The player character starts with the first texture
        in the idle animation.
    `time_since_last_frame` : float
        The time since the last frame was drawn. This is
        used to control the FPS of the animation.
    `animation_fps` : dict[str, float]
        The FPS of the animations. The keys are the names
        of the animations and the values are the FPS of
        the animations.
    `physics_engine` : arcade.PhysicsEnginePlatformer
        The physics engine used to control the player
        velocity and collision with the platforms.

    Usage
    -----
    >>> player = Banjo()
    """
    def __init__(self) -> None:
        """ Initialize the player character.
        """
        super().__init__(scale=1)

        self.texture_dict = BANJO_TEXTURES

        # Banjo gameplay stats
        self.hp = HP
        self.attack = ATTACK
        self.hunger_rate = HUNGER_RATE
        self.current_hunger = 0
        self.max_hunger = 3
        self.time_since_last_eaten = 0.0
        self.drying_rate = DRYING_RATE
        self.current_dryness = 0
        self.max_dryness = 3
        self.time_since_last_hydrated = 0.0
        self.walking_velocity = WALKING_VELOCITY
        self.friction = 1.5
        self.mass = 2.0
        self.is_dead = False
        self.hearing_range = HEARING_RANGE

        # Banjo animation variables
        self.is_dying = False
        self.texture = self.texture_dict["walk"][0][0]
        self.character_facing_direction = RIGHT_FACING
        self.current_animation = "idle"
        self.current_texture_index = 0
        self.melee_impact_texture_indices = [3, 6]

        # FPS control variables
        self.time_since_last_frame = 0.0
        self.animation_fps = {
            "idle": 1/6,
            "walk": 1/8,
            "turn": 1/2,
            "bark": 1/5,
            "melee": 1/8,
            "dead": 1/8
        }

        # Physics engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            player_sprite=self,
            platforms=PLATFORMS,
            gravity_constant=GRAVITY
        )

    def eat(self) -> None:
        """ Eat food to restore hunger.

        Usage
        -----
        >>> player.eat()
        """
        self.current_hunger = 0
        self.time_since_last_eaten = 0.0

        if self.hp + 20 >= 100:
            self.hp = 100
        else:
            self.hp += 20

    # UNUSED FEATURE
    def hunger(self) -> None:
        """ Hunger to restore fullness.

        Usage
        -----
        >>> player.hunger()
        """
        ...

    # UNUSED FEATURE
    def hydrate(self) -> None:
        """ Hydrate to restore dryness.

        Usage
        -----
        >>> player.hydrate()
        """
        self.current_dryness = 0
        self.time_since_last_hydrated = 0.0

    # UNUSED FEATURE
    def dehydrate(self) -> None:
        """ Dehydrate to restore dryness.

        Usage
        -----
        >>> player.dehydrate()
        """
        ...

    def damaged(
            self,
            damage: int
        ) -> None:
        """ Take damage from an attack.

        Parameters
        ----------
        `damage` : int
            The amount of damage to take.

        Usage
        -----
        >>> player.damaged(10)
        """
        self.hp -= damage

    def idle(self) -> None:
        """ Play the idle animation.

        Usage
        -----
        >>> soldier_1.idle()
        """
        self.change_x = 0

        current_texture = self.texture_dict[self.current_animation]

        if self.current_texture_index > len(current_texture) - 1:
            self.current_texture_index = 0

        self.texture = current_texture[self.current_texture_index][self.character_facing_direction]
        self.current_texture_index += 1

    def walk(self) -> None:
        """ Play the walking animation.

        Usage
        -----
        >>> soldier_1.walk()
        """
        # Multiply velocity by -1 if looking left, 1 otherwise
        self.change_x = self.walking_velocity * (1 - 2 * self.character_facing_direction)

        current_texture = self.texture_dict[self.current_animation]

        if self.current_texture_index > len(current_texture) - 1:
            self.current_texture_index = 0

        self.texture = current_texture[self.current_texture_index][self.character_facing_direction]
        self.current_texture_index += 1

    def turn(self) -> None:
        """ Play the turning animation.

        Parameters
        ----------
        `direction` : int
            The direction the player is turning. 0 for right, 1 for left.

        Usage
        -----
        >>> player.turn(0)
        """
        self.character_facing_direction = abs(self.character_facing_direction - 1)
        self.texture = self.texture_dict[self.current_animation][0][self.character_facing_direction]

    def bark(self) -> None:
        """ Play the barking animation.

        Usage
        -----
        >>> player.bark()
        """
        self.change_x = 0

        current_texture = self.texture_dict[self.current_animation]

        if self.current_texture_index > len(current_texture) - 1:
            self.current_texture_index = 0

        self.texture = current_texture[self.current_texture_index][self.character_facing_direction]

        if self.current_texture_index == 2:
            arcade.play_sound(arcade.load_sound(BANJO_BARK_SOUND))

        self.current_texture_index += 1

    def melee(self) -> None:
        """ Play the melee attack animation.

        Usage
        -----
        >>> player.melee()
        """
        self.change_x = 0

        current_texture = self.texture_dict[self.current_animation]

        if self.current_texture_index > len(current_texture) - 1:
            self.current_texture_index = 0

        self.texture = current_texture[self.current_texture_index][self.character_facing_direction]
        self.current_texture_index += 1

    def dead(self) -> None:
        """ Play the death animation.

        Usage
        -----
        >>> player.death()
        """
        self.change_x = 0

        if not self.is_dying:
            self.current_texture_index = 0
            self.is_dying = True

        current_texture = self.texture_dict[self.current_animation]

        if self.current_texture_index > len(current_texture) - 1:
            self.is_dead = True
            return

        self.texture = current_texture[self.current_texture_index][self.character_facing_direction]
        self.current_texture_index += 1

    def update_animation(
            self,
            delta_time: float=1/60,
            *args, # type: ignore
            **kwargs # type: ignore
        ) -> None:

        if self.is_dead:
            return

        self.time_since_last_frame += delta_time

        if self.time_since_last_frame >= self.animation_fps[self.current_animation]:
            # Clamp the current animation to death if death is triggered
            if self.is_dying or self.hp <= 0:
                self.current_animation = "dead"

            getattr(self, self.current_animation)()
            self.time_since_last_frame = 0.0

    def update(
            self,
            delta_time: float=1/60,
            *args, # type: ignore
            **kwargs # type: ignore
        ) -> None:
        """ Update the player character.

        Parameters
        ----------
        `delta_time` : float
            The time since the last frame was drawn.

        Usage
        -----
        >>> player.update(1/60)
        """
        self.physics_engine.update()
        self.update_animation(delta_time, *args, **kwargs)