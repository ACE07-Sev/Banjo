from __future__ import annotations

__all__ = ["Soldier1"]

import arcade

# Constants
DEAD_ZONE = 0.001
RIGHT_FACING = 0
LEFT_FACING = 1
DISTANCE_TO_CHANGE_TEXTURE = 0.5

# Soldier 1 Constants
WALKING_VELOCITY = 1100
RUNNING_VELOCITY = 1800
HEALTH_POINTS = 30
ACCURACY = 0.7
GRENADE_DAMAGE = 80
VISION_RANGE = 500

# SCAR Constants
SCAR_DAMAGE = 10
SCAR_MAG = 20
BULLET_MOVE_FORCE = 4500
BULLET_MASS = 0.1
BULLET_GRAVITY = 300

SHOOTING_SOUND = arcade.load_sound("sounds/snd_shooting.wav")
SHELL_SOUND = arcade.load_sound("sounds/snd_bullet_shell.wav")

PATH_CONSTANT = "sprites/soldier_1/"
SOLDIER_1_IDLE = PATH_CONSTANT + "Idle.png"
SOLDIER_1_WALK = PATH_CONSTANT + "Walk.png"
SOLDIER_1_RUN = PATH_CONSTANT + "Run.png"
SOLDIER_1_MELEE = PATH_CONSTANT + "Melee.png"
SOLDIER_1_HIP_FIRE = PATH_CONSTANT + "Hip_shooting.png"
SOLDIER_1_AIM_FIRE = PATH_CONSTANT + "Aimed_down_shooting.png"
SOLDIER_1_GRENADE = PATH_CONSTANT + "Grenade.png"
SOLDIER_1_HURT = PATH_CONSTANT + "Hurt.png"
SOLDIER_1_DEATH = PATH_CONSTANT + "Death.png"

SOLDIER_1_IDLE_SPRITESHEET = arcade.load_spritesheet(SOLDIER_1_IDLE)
SOLDIER_1_WALK_SPRITESHEET = arcade.load_spritesheet(SOLDIER_1_WALK)
SOLDIER_1_RUN_SPRITESHEET = arcade.load_spritesheet(SOLDIER_1_RUN)
SOLDIER_1_MELEE_SPRITESHEET = arcade.load_spritesheet(SOLDIER_1_MELEE)
SOLDIER_1_HIP_FIRE_SPRITESHEET = arcade.load_spritesheet(SOLDIER_1_HIP_FIRE)
SOLDIER_1_AIM_FIRE_SPRITESHEET = arcade.load_spritesheet(SOLDIER_1_AIM_FIRE)
SOLDIER_1_GRENADE_SPRITESHEET = arcade.load_spritesheet(SOLDIER_1_GRENADE)
SOLDIER_1_HURT_SPRITESHEET = arcade.load_spritesheet(SOLDIER_1_HURT)
SOLDIER_1_DEATH_SPRITESHEET = arcade.load_spritesheet(SOLDIER_1_DEATH)


class Soldier1(arcade.Sprite):
    """ `banjo.Soldier1` is the class that represents the Soldier 1 NPC
    character in the game. It is a subclass of `arcade.Sprite` and has
    additional functionality to handle walking, running, melee attacks,
    shooting, grenade throwing, taking damage, and dying.

    Soldier 1 is the aggressive close combat type of NPC. They are
    equipped with a powerful assault rifle and a grenade. They are
    always on the move and will attack Banjo on sight. They are
    not very accurate but they make up for it with their numbers and
    aggressiveness.

    Notes
    -----
    Sgt. McTavish is a competitive FNG. He's a bit of a loose cannon
    which is why he runs towards the enemy instead of away from them.
    He's a bit of a show off and likes to show off his skills by
    throwing grenades and shooting from the hip.

    Sgt. McTavish has 30 health points and deals 10 damage with each
    round he hits Banjo with. He rocks a 7.62mm FN SCAR-H 17 with a
    20 round magazine. He also carries an M67 fragmentation grenade
    which he can throw at Banjo.

    Sgt. McTavish is part of TF141 and is a member of the Bravo Team.
    Due to how slippery he is sometimes, he's also known as "Soap".

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
    `hip_fire_textures` : list[tuple[arcade.Texture, arcade.Texture]]
        A list of tuples where each tuple contains a texture facing
        left and a texture facing right. These textures are used
        for the hip fire shooting animation.
    `aim_fire_textures` : list[tuple[arcade.Texture, arcade.Texture]]
        A list of tuples where each tuple contains a texture facing
        left and a texture facing right. These textures are used
        for the aim fire shooting animation.
    `grenade_textures` : list[tuple[arcade.Texture, arcade.Texture]]
        A list of tuples where each tuple contains a texture facing
        left and a texture facing right. These textures are used
        for the grenade throwing animation.
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
    >>> soldier_1 = Soldier1()
    """
    def __init__(self) -> None:
        """ Initialize the Soldier 1 NPC.
        """
        super().__init__(scale=1.5)

        idle_textures = SOLDIER_1_IDLE_SPRITESHEET.get_texture_grid((128, 128), 7, 7)
        walk_textures = SOLDIER_1_WALK_SPRITESHEET.get_texture_grid((128, 128), 7, 7)
        run_textures = SOLDIER_1_RUN_SPRITESHEET.get_texture_grid((128, 128), 8, 8)
        melee_textures = SOLDIER_1_MELEE_SPRITESHEET.get_texture_grid((128, 128), 3, 3)
        hip_fire_textures = SOLDIER_1_HIP_FIRE_SPRITESHEET.get_texture_grid((128, 128), 6, 6)
        aim_fire_textures = SOLDIER_1_AIM_FIRE_SPRITESHEET.get_texture_grid((128, 128), 6, 6)
        grenade_textures = SOLDIER_1_GRENADE_SPRITESHEET.get_texture_grid((128, 128), 9, 9)
        hurt_textures = SOLDIER_1_HURT_SPRITESHEET.get_texture_grid((128, 128), 3, 3)
        death_textures = SOLDIER_1_DEATH_SPRITESHEET.get_texture_grid((256, 128), 10, 10)

        self.idle_textures = [(texture, texture.flip_left_right()) for texture in idle_textures]
        self.walk_textures = [(texture, texture.flip_left_right()) for texture in walk_textures]
        self.run_textures = [(texture, texture.flip_left_right()) for texture in run_textures]
        self.melee_textures = [(texture, texture.flip_left_right()) for texture in melee_textures]
        self.hip_fire_textures = [(texture, texture.flip_left_right()) for texture in hip_fire_textures]
        self.aim_fire_textures = [(texture, texture.flip_left_right()) for texture in aim_fire_textures]
        self.grenade_textures = [(texture, texture.flip_left_right()) for texture in grenade_textures]
        self.hurt_textures = [(texture, texture.flip_left_right()) for texture in hurt_textures]
        self.death_textures = [(texture, texture.flip_left_right()) for texture in death_textures]

        self.is_idle = True
        self.hp = HEALTH_POINTS
        self.attack = SCAR_DAMAGE
        self.accuracy = ACCURACY
        self.magazine = SCAR_MAG
        self.range = VISION_RANGE

        self.running = False
        self.texture = self.walk_textures[0][0]
        self.character_face_direction = RIGHT_FACING
        self.current_texture = 0
        self.x_odometer = 0

        # FPS control variables
        # self.time_since_last_frame = 0
        # self.animation_frame_rate = {
        #     "idle": 1/1000
        # }
        # self.current_animation = "idle"

    def idle(self) -> None:
        """ Play the idle animation.

        Usage
        -----
        >>> soldier_1.idle()
        """
        # if self.time_since_last_frame < self.animation_frame_rate["idle"]:
        #     return

        if self.current_texture > 6:
            self.current_texture = 0
        self.texture = self.idle_textures[self.current_texture][self.character_face_direction]
        self.current_texture += 1

    def walk(self) -> None:
        """ Play the walking animation.

        Usage
        -----
        >>> soldier_1.walk()
        """
        if self.current_texture > 6:
            self.current_texture = 0
        self.texture = self.walk_textures[self.current_texture][self.character_face_direction]
        self.current_texture += 1

    def run(self) -> None:
        """ Play the running animation.

        Usage
        -----
        >>> soldier_1.run()
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
        >>> soldier_1.melee()
        """
        self.is_idle = False
        if self.current_texture > 2:
            self.current_texture = 0
        self.texture = self.melee_textures[self.current_texture][self.character_face_direction]
        self.current_texture += 1

    def hip_fire(self) -> None:
        """ Play the hip fire shooting animation.

        Usage
        -----
        >>> soldier_1.hip_fire()
        """
        self.is_idle = False
        if self.current_texture > 5:
            self.current_texture = 0
        self.texture = self.hip_fire_textures[self.current_texture][self.character_face_direction]
        if self.current_texture == 2:
            arcade.play_sound(SHOOTING_SOUND)
        if self.current_texture == 4:
            arcade.play_sound(SHELL_SOUND)
        self.current_texture += 1

    def aim_fire(self) -> None:
        """ Play the aim fire shooting animation.

        Usage
        -----
        >>> soldier_1.aim_fire()
        """
        self.is_idle = False
        if self.current_texture > 5:
            self.current_texture = 0
        self.texture = self.aim_fire_textures[self.current_texture][self.character_face_direction]
        if self.current_texture == 2:
            arcade.play_sound(SHOOTING_SOUND)
        if self.current_texture == 4:
            arcade.play_sound(SHELL_SOUND)
        self.current_texture += 1

    def grenade(self) -> None:
        """ Play the grenade throwing animation.

        Usage
        -----
        >>> soldier_1.grenade()
        """
        self.is_idle = False
        if self.current_texture > 8:
            self.current_texture = 0
        self.texture = self.grenade_textures[self.current_texture][self.character_face_direction]
        self.current_texture += 1

    def hurt(self) -> None:
        """ Play the hurt animation.

        Usage
        -----
        >>> soldier_1.hurt()
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
        >>> soldier_1.death()
        """
        self.hp = 0
        self.is_idle = False
        if self.current_texture > 9:
            return
        self.texture = self.death_textures[self.current_texture][self.character_face_direction]
        self.current_texture += 1

    # def update_animation(
    #         self,
    #         delta_time: float
    #     ) -> None:

    #     self.time_since_last_frame += delta_time
    #     getattr(self, self.current_animation)()
    #     self.time_since_last_frame = 0

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
            # self.current_animation = "idle"
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