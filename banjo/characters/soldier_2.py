from __future__ import annotations

__all__ = ["Soldier2"]

import arcade
from banjo.characters import Soldier
from banjo.resources.textures import SOLDIER2_TEXTURES

# Soldier 2 Constants
WALKING_VELOCITY = 100
RUNNING_VELOCITY = 200
HEALTH_POINTS = 30
ACCURACY = 0.7
VISION_RANGE = 800
HEARING_RANGE = 300

# FAMAS Constants
FAMAS_DAMAGE = 10
FAMAS_MAG = 20
FAMAS_MELEE_DAMAGE = 1
BULLET_MOVE_FORCE = 4500
BULLET_MASS = 0.1
BULLET_GRAVITY = 300

# Sounds
SHOOTING_SOUND = arcade.load_sound("sounds/shooting.wav")
SHELL_SOUND = arcade.load_sound("sounds/bullet_shell.wav")
LEFT_STEP = arcade.load_sound("sounds/footstep_left.wav")
RIGHT_STEP = arcade.load_sound("sounds/footstep_right.wav")

ANIMATION_FPS = {
    "idle": 1/6,
    "walk": 1/8,
    "run": 1/12,
    "turn": 1/2,
    "melee": 1/6,
    "shoot": 1/16,
    "reload": 1/3,
    "hurt": 1/4,
    "death": 1/9
}


class Soldier2(Soldier):
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
    >>> soldier_2 = Soldier2()
    """
    def __init__(self) -> None:
        """ Initialize the Soldier 2 NPC.
        """
        super().__init__(
            texture_dict=SOLDIER2_TEXTURES,
            animation_fps=ANIMATION_FPS,
            hp=HEALTH_POINTS,
            shooting_range=VISION_RANGE,
            melee_range=100,
            hearing_range=HEARING_RANGE,
            accuracy=ACCURACY,
            shooting_damage=FAMAS_DAMAGE,
            mag_size=FAMAS_MAG,
            melee_damage=FAMAS_MELEE_DAMAGE,
            walking_velocity=WALKING_VELOCITY,
            running_velocity=RUNNING_VELOCITY,
            patrol_pace=3,
            time_to_recover=4,
            melee_impact_texture_indices=[1],
            shoot_impact_texture_indices=[2]
        )

    def walk(self) -> None:
        """ Play the walking animation.

        Usage
        -----
        >>> soldier_2.walk()
        """
        super().walk()

        if self.current_texture_index == 3:
            arcade.play_sound(LEFT_STEP, volume=0.5 * self.sound_amp, pan=self.pan)
        if self.current_texture_index == 7:
            arcade.play_sound(RIGHT_STEP, volume=0.5 * self.sound_amp, pan=self.pan)

    def run(self) -> None:
        """ Play the running animation.

        Usage
        -----
        >>> soldier_2.run()
        """
        super().run()

        if self.current_texture_index == 4:
            arcade.play_sound(LEFT_STEP, volume=0.5 * self.sound_amp, pan=self.pan)
        if self.current_texture_index == 8:
            arcade.play_sound(RIGHT_STEP, volume=0.5 * self.sound_amp, pan=self.pan)

    def shoot(self) -> None:
        """ Play the aim fire shooting animation.

        Usage
        -----
        >>> soldier_2.shoot()
        """
        super().shoot()

        if self.current_texture_index == 3:
            arcade.play_sound(SHOOTING_SOUND, volume=self.sound_amp, pan=self.pan)
            self.fsm.current_mag -= 1
        if self.current_texture_index == 5:
            arcade.play_sound(SHELL_SOUND, volume=self.sound_amp, pan=self.pan)
        if self.current_texture_index == 6:
            arcade.play_sound(SHELL_SOUND, volume=0.8 * self.sound_amp, pan=self.pan)