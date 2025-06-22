from __future__ import annotations

__all__ = ["Soldier1"]

import arcade
from banjo.characters import Soldier
from banjo.resources.textures import SOLDIER1_TEXTURES

# Soldier 1 Constants
WALKING_VELOCITY = 1.8
RUNNING_VELOCITY = 2.5
HEALTH_POINTS = 30
ACCURACY = 0.5
GRENADE_DAMAGE = 80
VISION_RANGE = 500
HEARING_RANGE = 1000

# SCAR Constants
SCAR_DAMAGE = 5
SCAR_MAG = 20
SCAR_MELEE_DAMAGE = 4

# Sounds
SHOOTING_SOUND = arcade.load_sound("sounds/shooting.wav")
SHELL_SOUND = arcade.load_sound("sounds/bullet_shell.wav")
LEFT_STEP = arcade.load_sound("sounds/footstep_left.wav")
RIGHT_STEP = arcade.load_sound("sounds/footstep_right.wav")

ANIMATION_FPS = {
    "idle": 1/6,
    "walk": 1/8,
    "run": 1/12,
    "melee": 1/6,
    "shoot": 1/16,
    "reload": 1/7,
    "alert": 1/8,
    "hurt": 1/4,
    "dead": 1/9,
    "at_ease": 1/6,
}


class Soldier1(Soldier):
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

    Sgt. McTavish has 30 health points and deals 5 damage with each
    round he hits Banjo with. He rocks a 7.62mm FN SCAR-H 17 with a
    20 round magazine. He also carries an M67 fragmentation grenade
    which he can throw at Banjo.

    Sgt. McTavish is part of TF141 and is a member of the Bravo Team.
    Due to how slippery he is sometimes, he's also known as "Soap".

    Attributes
    ----------
    `texture_dict` : dict[str, list[tuple[arcade.Texture, arcade.Texture]]]
        A dictionary containing the texture grids for each animation
        state of the soldier.
    `time_since_last_frame` : float
        The time since the last frame was updated.
    `time_since_last_coordinate` : float
        Time since last break at a checkpoint.
    `time_since_last_hit` : float
        Time since last hit by Banjo.
    `animation_fps` : dict[str, float]
        A dictionary containing the frames per second for each
        animation state of the soldier.
    `fsm` : banjo.characters.SoldierFSM
        The finite-state machine for the soldier, containing the
        transition logic and state management.
    `shooting_damage` : int
        The damage dealt by the soldier when shooting.
    `mag_size` : int
        The size of the soldier's magazine.
    `melee_damage` : int
        The damage dealt by the soldier when melee attacking.
    `accuracy` : float
        The accuracy of the soldier when shooting.
    `walking_velocity` : float
        The walking velocity of the soldier.
    `running_velocity` : float
        The running velocity of the soldier.
    `patrol_pace` : int
        The time the soldier takes to rest after reaching a checkpoint.
    `time_to_recover` : int
        The time the soldier takes to recover after being hit by Banjo.
    `is_reloading` : bool
        Whether the soldier is currently reloading or not.
    `is_alert` : bool
        Whether the soldier is currently alert or not.
    `is_dying` : bool
        Whether the soldier is currently dying or not.
    `is_dead` : bool
        Whether the soldier is currently dead or not.
    `texture` : arcade.Texture
        The current texture of the soldier.
    `character_facing_direction` : int
        The direction the soldier is facing (0 for right, 1 for left).
    `current_texture_index` : int
        The index of the current texture in the animation sequence.
    `melee_impact_texture_indices` : list[int]
        The texture indices where melee impact occurs.
    `shoot_impact_texture_indices` : list[int]
        The texture indices where shooting impact occurs.
    `sound_amp` : float
        The sound volume multiplier to reflect the distance to Banjo.
    `pan` : float
        The sound pan to reflect the position which the soldier is in
        with respect to Banjo. This mimics directional audio.
    `physics_engine` : arcade.PhysicsEnginePlatformer
        The physics engine managing the soldier's movement and collisions.

    Usage
    -----
    >>> soldier_1 = Soldier1()
    """
    def __init__(self) -> None:
        """ Initialize the Soldier 1 NPC.
        """
        super().__init__(
            texture_dict=SOLDIER1_TEXTURES,
            animation_fps=ANIMATION_FPS,
            hp=HEALTH_POINTS,
            shooting_range=VISION_RANGE,
            melee_range=100,
            hearing_range=HEARING_RANGE,
            accuracy=ACCURACY,
            shooting_damage=SCAR_DAMAGE,
            mag_size=SCAR_MAG,
            melee_damage=SCAR_MELEE_DAMAGE,
            walking_velocity=WALKING_VELOCITY,
            running_velocity=RUNNING_VELOCITY,
            patrol_pace=5,
            time_to_recover=5,
            melee_impact_texture_indices=[1],
            shoot_impact_texture_indices=[2]
        )

    def walk(self) -> None:
        """ Play the walking animation.

        Usage
        -----
        >>> soldier_1.walk()
        """
        super().walk()

        # Since we increment the current texture index in the walk method,
        # we need to add 1 to these indices to get the correct sound effect
        if self.current_texture_index == 3:
            arcade.play_sound(LEFT_STEP, volume=0.5 * self.sound_amp, pan=self.pan)
        if self.current_texture_index == 6:
            arcade.play_sound(RIGHT_STEP, volume=0.5 * self.sound_amp, pan=self.pan)

    def run(self) -> None:
        """ Play the running animation.

        Usage
        -----
        >>> soldier_1.run()
        """
        super().run()

        # Since we increment the current texture index in the run method,
        # we need to add 1 to these indices to get the correct sound effect
        if self.current_texture_index == 3:
            arcade.play_sound(LEFT_STEP, volume=0.5 * self.sound_amp, pan=self.pan)
        if self.current_texture_index == 7:
            arcade.play_sound(RIGHT_STEP, volume=0.5 * self.sound_amp, pan=self.pan)

    def shoot(self) -> None:
        """ Play the aim fire shooting animation.

        Usage
        -----
        >>> soldier_1.shoot()
        """
        super().shoot()

        # Since we increment the current texture index in the shoot method,
        # we need to add 1 to these indices to get the correct sound effect
        if self.current_texture_index == 3:
            arcade.play_sound(SHOOTING_SOUND, volume=self.sound_amp, pan=self.pan)
            self.fsm.current_mag -= 1
        if self.current_texture_index == 5:
            arcade.play_sound(SHELL_SOUND, volume=self.sound_amp, pan=self.pan)
        if self.current_texture_index == 6:
            arcade.play_sound(SHELL_SOUND, volume=0.8 * self.sound_amp, pan=self.pan)