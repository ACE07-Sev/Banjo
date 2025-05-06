from __future__ import annotations

__all__ = ["Soldier1"]

import arcade
from banjo.characters import Banjo
from banjo.characters.soldier_fsm import SoldierFSM
from banjo.resources.game_constants import (
    GRAVITY,
    RIGHT_FACING,
    LEFT_FACING
)
from banjo.resources.level_maps import PLATFORMS
from banjo.resources.textures import SOLDIER1_TEXTURES
import random

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
    `physics_engine` : arcade.PhysicsEnginePlatformer
        The physics engine managing the soldier's movement and collisions.

    Usage
    -----
    >>> soldier_1 = Soldier1()
    """
    def __init__(self) -> None:
        """ Initialize the Soldier 1 NPC.
        """
        super().__init__(scale=1)

        self.texture_dict = SOLDIER1_TEXTURES

        self.time_since_last_frame = 0.0
        self.time_since_last_coordinate = 0.0
        self.time_since_last_hit = 0.0
        self.animation_fps = {
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

        # Gameplay stats
        self.fsm = SoldierFSM(
            hp=HEALTH_POINTS,
            shooting_range=VISION_RANGE,
            melee_range=100,
            hearing_range=HEARING_RANGE,
            shooting_damage=SCAR_DAMAGE,
            melee_damage=SCAR_MELEE_DAMAGE,
            mag_size=SCAR_MAG
        )
        self.accuracy = ACCURACY

        # Physics variables
        self.walking_velocity = WALKING_VELOCITY
        self.running_velocity = RUNNING_VELOCITY
        self.patrol_pace = 5
        self.time_to_recover = 5

        # Animation variables
        self.is_reloading = False
        self.is_alert = False
        self.is_dying = False
        self.is_dead = False
        self.texture = self.texture_dict[self.current_state][0][0]
        self.character_facing_direction = RIGHT_FACING
        self.current_texture_index = 0
        self.melee_impact_texture_indices = [1]
        self.shoot_impact_texture_indices = [2]

        # Sound variable
        self.sound_amp = 1.0

        # Physics engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self,
            PLATFORMS,
            gravity_constant=GRAVITY
        )

    @property
    def current_state(self) -> str:
        """ Get the current state of the soldier.

        Returns
        -------
        `str`
            The name of the current state of the soldier.
        """
        return self.fsm.current_state.name

    @property
    def hp(self) -> int:
        """ Get the current health points of the soldier.

        Returns
        -------
        `int`
            The current health points of the soldier.
        """
        return self.fsm.hp

    @hp.setter
    def hp(self, value: int) -> None:
        """ Set the health points of the soldier.

        Parameters
        ----------
        `value` : int
            The new health points of the soldier.
        """
        self.fsm.hp = max(0, value)

    @property
    def chase_to(self) -> int | None:
        """ Get the target position of the soldier.

        Returns
        -------
        int | None
            The target position of the soldier.
        """
        return self.fsm.chase_to

    @chase_to.setter
    def chase_to(
            self,
            target_position: int
        ) -> None:
        """ Set the target position of the soldier.

        Parameters
        ----------
        `value` : int
            The new target position of the soldier.
        """
        self.fsm.chase_to = target_position

    def damaged(
            self,
            damage: int
        ) -> None:
        """ Damages the soldier by the given amount.

        Parameters
        ----------
        `damage` : int
            The amount of damage to deal to the soldier.

        Usage
        -----
        >>> soldier_1.damaged(10)
        """
        self.hp -= damage

    def idle(self) -> None:
        """ Play the idle animation.

        Usage
        -----
        >>> soldier_1.idle()
        """
        self.change_x = 0

        current_texture = self.texture_dict[self.current_state]

        if self.current_texture_index > len(current_texture) - 1:
            self.current_texture_index = 0

        self.texture = current_texture[self.current_texture_index][self.character_facing_direction]
        self.current_texture_index += 1

    def at_ease(self) -> None:
        """ Play the at ease animation.

        Usage
        -----
        >>> soldier_1.at_ease()
        """
        self.change_x = 0

        current_texture = self.texture_dict[self.current_state]

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

        current_texture = self.texture_dict[self.current_state]

        if self.current_texture_index > len(current_texture) - 1:
            self.current_texture_index = 0

        self.texture = current_texture[self.current_texture_index][self.character_facing_direction]

        if self.current_texture_index == 2:
            arcade.play_sound(LEFT_STEP, volume=0.5 * self.sound_amp)
        if self.current_texture_index == 5:
            arcade.play_sound(RIGHT_STEP, volume=0.5 * self.sound_amp)

        self.current_texture_index += 1

    def run(self) -> None:
        """ Play the running animation.

        Usage
        -----
        >>> soldier_1.run()
        """
        # Multiply velocity by -1 if looking left, 1 otherwise
        self.change_x = self.running_velocity * (1 - 2 * self.character_facing_direction)

        current_texture = self.texture_dict[self.current_state]

        if self.current_texture_index > len(current_texture) - 1:
            self.current_texture_index = 0

        self.texture = current_texture[self.current_texture_index][self.character_facing_direction]

        if self.current_texture_index == 2:
            arcade.play_sound(LEFT_STEP, volume=0.5 * self.sound_amp)
        if self.current_texture_index == 6:
            arcade.play_sound(RIGHT_STEP, volume=0.5 * self.sound_amp)

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
        self.texture = self.texture_dict["idle"][0][self.character_facing_direction]

    def face_enemy(
            self,
            enemy: Banjo
        ) -> None:
        """ Face the enemy.

        Parameters
        ----------
        `enemy` : banjo.characters.Banjo
            The player character.
        """
        self.character_facing_direction = LEFT_FACING if enemy.center_x < self.center_x else RIGHT_FACING

    def melee(self) -> None:
        """ Play the melee attack animation.

        Usage
        -----
        >>> soldier_1.melee()
        """
        self.change_x = 0

        current_texture = self.texture_dict[self.current_state]

        if self.current_texture_index > len(current_texture) - 1:
            self.current_texture_index = 0

        self.texture = current_texture[self.current_texture_index][self.character_facing_direction]
        self.current_texture_index += 1

    def shoot(self) -> None:
        """ Play the aim fire shooting animation.

        Usage
        -----
        >>> soldier_1.aim_fire()
        """
        self.change_x = 0

        current_texture = self.texture_dict[self.current_state]

        if self.current_texture_index > len(current_texture) - 1:
            self.current_texture_index = 0

        self.texture = current_texture[self.current_texture_index][self.character_facing_direction]

        if self.current_texture_index == 2:
            arcade.play_sound(SHOOTING_SOUND, volume=self.sound_amp)
            self.fsm.current_mag -= 1
        if self.current_texture_index == 4:
            arcade.play_sound(SHELL_SOUND, volume=self.sound_amp)
        if self.current_texture_index == 5:
            arcade.play_sound(SHELL_SOUND, volume=0.8 * self.sound_amp)

        self.current_texture_index += 1

    def reload(self) -> None:
        """ Reload the magazine.

        Usage
        -----
        >>> soldier_1.reload()
        """
        self.change_x = 0

        if not self.is_reloading:
            self.current_texture_index = 0
            self.is_reloading = True

        current_texture = self.texture_dict[self.current_state]

        if self.current_texture_index > len(current_texture) - 1:
            self.current_texture_index = 0
            self.is_reloading = False
            self.fsm.reload_done = True
            return

        self.texture = current_texture[self.current_texture_index][self.character_facing_direction]
        self.current_texture_index += 1

    def alert(self) -> None:
        """ Play the alert animation.

        Usage
        -----
        >>> soldier_1.alert()
        """
        self.change_x = 0

        if not self.is_alert:
            self.current_texture_index = 0
            self.is_alert = True

        current_texture = self.texture_dict[self.current_state]

        if self.current_texture_index > len(current_texture) - 1:
            self.current_texture_index = 0
            self.is_alert = False
            self.fsm.alert_done = True
            return

        self.texture = current_texture[self.current_texture_index][self.character_facing_direction]
        self.current_texture_index += 1

    def hurt(self) -> None:
        """ Play the hurt animation.

        Usage
        -----
        >>> soldier_1.hurt()
        """
        self.change_x = 0

        current_texture = self.texture_dict[self.current_state]

        if self.current_texture_index > len(current_texture) - 1:
            self.current_texture_index = 0

        self.texture = current_texture[self.current_texture_index][self.character_facing_direction]
        self.current_texture_index += 1

    def dead(self) -> None:
        """ Play the death animation.

        Usage
        -----
        >>> soldier_1.death()
        """
        self.change_x = 0

        if not self.is_dying:
            self.current_texture_index = 0
            self.is_dying = True

        current_texture = self.texture_dict[self.current_state]

        if self.current_texture_index > len(current_texture) - 1:
            self.is_dead = True
            self.is_dying = False
            return

        self.texture = current_texture[self.current_texture_index][self.character_facing_direction]
        self.current_texture_index += 1

    def soldier_patrolling(
            self,
            delta_time: float
        ) -> None:
        """ Handle the patrol behavior of the soldiers.

        Parameters
        ----------
        `delta_time` : float
            The time since the last frame.
        """
        # Soldier needs to take a break at each checkpoint
        if self.fsm.take_a_break and self.current_state == "idle":
            if self.time_since_last_coordinate > self.patrol_pace:
                self.fsm.take_a_break = False
                self.time_since_last_coordinate = 0.0
                self.fsm.set_patrol_checkpoints([random.randint(500, 2000)])
            else:
                self.time_since_last_coordinate += delta_time
                return

        if not self.fsm.patrol_checkpoints:
            return

        target_x = self.fsm.patrol_checkpoints[-1]

        if target_x < self.center_x:
            self.character_facing_direction = LEFT_FACING

        elif target_x > self.center_x:
            self.character_facing_direction = RIGHT_FACING

    def soldier_chasing(self) -> None:
        """ Handle the chase behavior of the soldiers.
        """
        if self.chase_to is None or self.current_state != "run":
            return

        target_x = self.chase_to

        if target_x < self.center_x:
            self.character_facing_direction = LEFT_FACING

        elif target_x > self.center_x:
            self.character_facing_direction = RIGHT_FACING

    def calculate_accuracy(
            self,
            distance: int
        ) -> float:
        """ Calculate the accuracy of the soldier based on the distance to the target.
        The `self.accuracy` dictates the chance of hitting the target at maximum range.

        Parameters
        ----------
        `distance` : int
            The distance to the target.

        Returns
        -------
        `float`
            The accuracy of the soldier.
        """
        return 1 - (1 - self.accuracy) * (distance / self.fsm.shooting_range) ** 2

    def shoot_banjo(
            self,
            banjo: Banjo
        ) -> None:
        """ Handle the shooting of Banjo by the soldiers.

        Parameters
        ----------
        `banjo` : banjo.characters.Banjo
            The player character.
        """
        if self.current_state != "shoot":
            return

        # Check if the soldier hit Banjo
        if self.current_texture_index in self.shoot_impact_texture_indices:
            distance = int(abs(banjo.center_x - self.center_x))
            hit_chance = random.random()
            if hit_chance <= self.calculate_accuracy(distance):
                banjo.damaged(self.fsm.shooting_damage)

    def melee_banjo(
            self,
            banjo: Banjo
        ) -> None:
        """ Handle the melee attack of the soldiers.

        Parameters
        ----------
        `banjo` : banjo.characters.Banjo
            The player character.
        """
        if self.current_state != "melee":
            return

        if self.current_texture_index in self.melee_impact_texture_indices:
            banjo.damaged(self.fsm.melee_damage)

    def melee_soldier(
            self,
            delta_time: float,
            banjo: Banjo
        ) -> None:
        """ Handle the melee attack of the soldiers.

        Parameters
        ----------
        `delta_time` : float
            The time since the last frame.
        `banjo` : banjo.characters.Banjo
            The player character.
        """
        if self.current_state != "hurt":
            return

        # If the soldier is not being hit anymore, then they need time to recover
        # before regaining their concsciousness
        if banjo.current_animation != "melee":
            if self.time_since_last_hit > self.time_to_recover:
                self.time_since_last_hit = 0.0
                self.fsm.is_recovered = True
            else:
                self.time_since_last_hit += delta_time

            return

        if banjo.current_texture_index in banjo.melee_impact_texture_indices:
            self.time_since_last_hit = 0.0
            self.damaged(banjo.attack)

    def update_state(
            self,
            enemy: Banjo
        ) -> None:
        """ Update the soldier's state machine based
        on the enemy's state.

        Parameters
        ----------
        `enemy` : banjo.characters.Banjo
            The player character.

        Usage
        -----
        >>> soldier_1.cycle()
        """
        fsm_transition_params = {
            "soldier_coordinate": self.position,
            "soldier_facing_direction": self.character_facing_direction,
            "enemy_coordinate": enemy.position,
            "enemy_direction": enemy.character_facing_direction,
            "enemy_hitting": enemy.current_animation == "melee",
            "enemy_barking": enemy.current_animation == "bark",
            "enemy_hp": enemy.hp
        }

        self.fsm.cycle(**fsm_transition_params)

        if self.current_state in ["shoot", "melee", "reload"]:
            self.face_enemy(enemy)

    def update_animation(
            self,
            delta_time: float=1/60,
            *args, # type: ignore
            **kwargs # type: ignore
        ) -> None:

        if self.is_dead:
            return

        self.time_since_last_frame += delta_time

        if self.time_since_last_frame >= self.animation_fps[self.current_state]:
            getattr(self, self.current_state)()
            self.time_since_last_frame = 0.0

    def update(
            self,
            delta_time: float=1/60,
            *args, # type: ignore
            **kwargs # type: ignore
        ) -> None:

        banjo = kwargs.get("banjo")

        if banjo is None:
            raise ValueError("Banjo object must be passed as a keyword argument.")

        self.sound_amp = max(0.0, 1 - abs(self.center_x - banjo.center_x) / banjo.hearing_range)

        self.physics_engine.update()

        # Soldier will patrol idly, and will engage Banjo
        # if they are in range
        self.update_animation(delta_time, *args, **kwargs)
        self.melee_banjo(banjo)
        self.melee_soldier(delta_time, banjo)
        self.shoot_banjo(banjo)
        self.soldier_patrolling(delta_time)
        self.soldier_chasing()

        self.update_state(banjo)