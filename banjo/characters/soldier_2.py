from __future__ import annotations

__all__ = ["Soldier2"]

import arcade

# Constants
DEAD_ZONE = 0.001
RIGHT_FACING = 0
LEFT_FACING = 1
DISTANCE_TO_CHANGE_TEXTURE = 1

# Soldier 2 Constants
WALKING_VELOCITY = 800
RUNNING_VELOCITY = 1200
HEALTH_POINTS = 30
ACCURACY = 0.85
VISION_RANGE = 800

# FAMAS Constants
FAMAS_DAMAGE = 10
FAMAS_MAG = 20
BULLET_MOVE_FORCE = 4500
BULLET_MASS = 0.1
BULLET_GRAVITY = 300

SHOOTING_SOUND = arcade.load_sound("sounds/snd_shooting.wav")
SHELL_SOUND = arcade.load_sound("sounds/snd_bullet_shell.wav")

PATH_CONSTANT = "sprites/soldier_2/"
SOLDIER_2_IDLE = PATH_CONSTANT + "Idle.png"
SOLDIER_2_WALK = PATH_CONSTANT + "Walk.png"
SOLDIER_2_RUN = PATH_CONSTANT + "Run.png"
SOLDIER_2_MELEE = PATH_CONSTANT + "Melee.png"
SOLDIER_2_CROUCH_FIRE = PATH_CONSTANT + "Crouched_shooting.png"
SOLDIER_2_AIM_FIRE = PATH_CONSTANT + "Aimed_down_shooting.png"
SOLDIER_2_HURT = PATH_CONSTANT + "Hurt.png"
SOLDIER_2_DEATH = PATH_CONSTANT + "Death.png"

SOLDIER_2_IDLE_SPRITESHEET = arcade.load_spritesheet(SOLDIER_2_IDLE)
SOLDIER_2_WALK_SPRITESHEET = arcade.load_spritesheet(SOLDIER_2_WALK)
SOLDIER_2_RUN_SPRITESHEET = arcade.load_spritesheet(SOLDIER_2_RUN)
SOLDIER_2_MELEE_SPRITESHEET = arcade.load_spritesheet(SOLDIER_2_MELEE)
SOLDIER_2_CROUCH_FIRE_SPRITESHEET = arcade.load_spritesheet(SOLDIER_2_CROUCH_FIRE)
SOLDIER_2_AIM_FIRE_SPRITESHEET = arcade.load_spritesheet(SOLDIER_2_AIM_FIRE)
SOLDIER_2_HURT_SPRITESHEET = arcade.load_spritesheet(SOLDIER_2_HURT)
SOLDIER_2_DEATH_SPRITESHEET = arcade.load_spritesheet(SOLDIER_2_DEATH)


class Soldier2(arcade.Sprite):
    """ `banjo.Soldier2` is the class that represents the Soldier 2 NPC
    character in the game. It is a subclass of `arcade.Sprite` and has
    additional functionality to handle walking, running, melee attacks,
    shooting, grenade throwing, taking damage, and dying.

    Soldier 2 is the tactical mid-range soldier NPC in the game. They
    are equipped with a 5.56mm FAMAS F1 with a 25 round magazine. They
    are trained to take cover and shoot from a distance. They will keep
    their distance from Banjo and shoot at him from a distance. Due to
    crouching and aiming down sights, they are more accurate than the
    other NPCs.

    Notes
    -----
    Lt. Riley is a seasoned soldier who has been in the field for a
    while. He's a calm and collected soldier who knows how to handle
    himself in a firefight. He's a bit of a perfectionist and likes to
    take his time to line up his shots.

    Lt. Riley has 30 health points and deals 10 damage with each round
    he hits Banjo with. He rocks a 5.56mm FAMAS F1 with a 25 round magazine.
    He only carries a smoke grenade which he can throw at Banjo to obscure
    his vision.

    Lt. Riley is part of TF141 and is a member of the Bravo Team.
    Due to how cold and calculated he is, he is also known as "Ghost".

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
    `run_textures` : list[tuple[arcade.Texture, arcade.Texture]]
        A list of tuples where each tuple contains a texture facing
        left and a texture facing right. These textures are used
        for the running animation.
    `melee_textures` : list[tuple[arcade.Texture, arcade.Texture]]
        A list of tuples where each tuple contains a texture facing
        left and a texture facing right. These textures are used
        for the melee attack animation.
    `crouch_fire_textures` : list[tuple[arcade.Texture, arcade.Texture]]
        A list of tuples where each tuple contains a texture facing
        left and a texture facing right. These textures are used
        for the crouch fire shooting animation.
    `aim_fire_textures` : list[tuple[arcade.Texture, arcade.Texture]]
        A list of tuples where each tuple contains a texture facing
        left and a texture facing right. These textures are used
        for the aim fire shooting animation.
    `hurt_textures` : list[tuple[arcade.Texture, arcade.Texture]]
        A list of tuples where each tuple contains a texture facing
        left and a texture facing right. These textures are used
        for the hurt animation.
    `death_textures` : list[tuple[arcade.Texture, arcade.Texture]]
        A list of tuples where each tuple contains a texture facing
        left and a texture facing right. These textures are used
        for the death animation.
    `texture` : arcade.Texture
        The current texture being displayed.
    `is_idle` : bool
        A boolean representing whether the NPC is idle.
    `hp` : int
        The amount of health points the NPC has.
    `attack` : int
        The amount of damage the NPC deals.
    `accuracy` : float
        The accuracy of the NPC's attacks.
    `magazine` : int
        The number of rounds the NPC has left in their magazine.
    `range` : int
        The range of the NPC's vision.
    `running` : bool
        A boolean representing whether the NPC is running.
    `character_face_direction` : int
        An integer representing which direction the NPC is facing.
        0 for right, 1 for left.
    `current_texture` : int
        The index of the current texture being displayed.
    `x_odometer` : float
        How far the NPC has moved horizontally since the last texture change.

    Usage
    -----
    >>> soldier_2 = Soldier2()
    """
    def __init__(self) -> None:
        """ Initialize the Soldier 2 NPC.
        """
        super().__init__(scale=1)

        idle_textures = SOLDIER_2_IDLE_SPRITESHEET.get_texture_grid((128, 128), 9, 9)
        walk_textures = SOLDIER_2_WALK_SPRITESHEET.get_texture_grid((128, 128), 8, 8)
        run_textures = SOLDIER_2_RUN_SPRITESHEET.get_texture_grid((128, 128), 8, 8)
        melee_textures = SOLDIER_2_MELEE_SPRITESHEET.get_texture_grid((128, 128), 4, 4)
        crouch_fire_textures = SOLDIER_2_CROUCH_FIRE_SPRITESHEET.get_texture_grid((128, 128), 7, 7)
        aim_fire_textures = SOLDIER_2_AIM_FIRE_SPRITESHEET.get_texture_grid((128, 128), 7, 7)
        hurt_textures = SOLDIER_2_HURT_SPRITESHEET.get_texture_grid((128, 128), 3, 3)
        death_textures = SOLDIER_2_DEATH_SPRITESHEET.get_texture_grid((256, 128), 9, 9)

        self.idle_textures = [(texture, texture.flip_left_right()) for texture in idle_textures]
        self.walk_textures = [(texture, texture.flip_left_right()) for texture in walk_textures]
        self.run_textures = [(texture, texture.flip_left_right()) for texture in run_textures]
        self.melee_textures = [(texture, texture.flip_left_right()) for texture in melee_textures]
        self.crouch_fire_textures = [(texture, texture.flip_left_right()) for texture in crouch_fire_textures]
        self.aim_fire_textures = [(texture, texture.flip_left_right()) for texture in aim_fire_textures]
        self.hurt_textures = [(texture, texture.flip_left_right()) for texture in hurt_textures]
        self.death_textures = [(texture, texture.flip_left_right()) for texture in death_textures]

        self.is_idle = True
        self.hp = HEALTH_POINTS
        self.attack = FAMAS_DAMAGE
        self.magazine = FAMAS_MAG
        self.accuracy = ACCURACY
        self.range = VISION_RANGE

        self.running = False
        self.texture = self.walk_textures[0][0]
        self.character_face_direction = RIGHT_FACING
        self.current_texture = 0
        self.x_odometer = 0

    def idle(self) -> None:
        """ Play the idle animation.

        Usage
        -----
        >>> soldier_2.idle()
        """
        if self.current_texture > 8:
            self.current_texture = 0
        self.texture = self.idle_textures[self.current_texture][self.character_face_direction]
        self.current_texture += 1

    def walk(self) -> None:
        """ Play the walking animation.

        Usage
        -----
        >>> soldier_2.walk()
        """
        if self.current_texture > 7:
            self.current_texture = 0
        self.texture = self.walk_textures[self.current_texture][self.character_face_direction]
        self.current_texture += 1

    def run(self) -> None:
        """ Play the running animation.

        Usage
        -----
        >>> soldier_2.run()
        """
        if self.current_texture > 7:
            self.current_texture = 0
        self.texture = self.run_textures[self.current_texture][self.character_face_direction]
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
        self.texture = self.idle_textures[0][self.character_face_direction]

    def melee(self) -> None:
        """ Play the melee attack animation.

        Usage
        -----
        >>> soldier_2.melee()
        """
        self.is_idle = False
        if self.current_texture > 2:
            self.current_texture = 0
        self.texture = self.melee_textures[self.current_texture][self.character_face_direction]
        self.current_texture += 1

    def crouch_fire(self) -> None:
        """ Play the crouch fire shooting animation.

        Usage
        -----
        >>> soldier_2.crouch_fire()
        """
        self.is_idle = False
        if self.current_texture > 5:
            self.current_texture = 0
        self.texture = self.crouch_fire_textures[self.current_texture][self.character_face_direction]
        if self.current_texture == 3:
            arcade.play_sound(SHOOTING_SOUND)
        if self.current_texture == 5:
            arcade.play_sound(SHELL_SOUND)
        self.current_texture += 1

    def aim_fire(self) -> None:
        """ Play the aim fire shooting animation.

        Usage
        -----
        >>> soldier_2.aim_fire()
        """
        self.is_idle = False
        if self.current_texture > 5:
            self.current_texture = 0
        self.texture = self.aim_fire_textures[self.current_texture][self.character_face_direction]
        if self.current_texture == 3:
            arcade.play_sound(SHOOTING_SOUND)
        if self.current_texture == 5:
            arcade.play_sound(SHELL_SOUND)
        self.current_texture += 1

    def hurt(self) -> None:
        """ Play the hurt animation.

        Usage
        -----
        >>> soldier_2.hurt()
        """
        self.is_idle = False
        if self.current_texture > 2:
            self.current_texture = 0
        self.texture = self.hurt_textures[self.current_texture][self.character_face_direction]
        self.current_texture += 1

    def death(self) -> None:
        """ Play the death animation.

        Usage
        -----
        >>> soldier_2.death()
        """
        self.is_idle = False
        if self.current_texture > 8:
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

        if abs(dx) <= DEAD_ZONE and self.is_idle:
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
            if self.running:
                self.run()
            else:
                self.walk()