from __future__ import annotations

__all__ = ["Soldier"]

import arcade
from banjo.characters import Banjo
from banjo.characters.soldier_fsm import SoldierFSM
from banjo.resources.game_constants import (
    GRAVITY,
    RIGHT_FACING,
    LEFT_FACING
)
from banjo.resources.level_maps import PLATFORMS
import random


class Soldier(arcade.Sprite):
    """ `banjo.Soldier` is the parent class for all soldier NPCs in the game.
    It inherits from `arcade.Sprite` and implements the soldier's common behavior
    and animations. In case of deviation from the common behavior, the child classes
    will override the methods.

    Additionally, if you want to add sounds you can do so by overriding the methods
    using `super().method_name()` and then adding conditions to play the sounds.

    Parameters
    ----------
    `texture_dict` : dict[str, list[tuple[arcade.Texture, arcade.Texture]]]
        A dictionary containing the texture grids for each animation
        state of the soldier.
    `animation_fps` : dict[str, float]
        A dictionary containing the frames per second for each
        animation state of the soldier.
    `hp` : int
        The health points of the soldier.
    `shooting_range` : int
        The range of the soldier's shooting attack.
    `melee_range` : int
        The range of the soldier's melee attack.
    `hearing_range` : int
        The range of the soldier's hearing.
    `accuracy` : float
        The accuracy of the soldier when shooting.
    `shooting_damage` : int
        The damage dealt by the soldier when shooting.
    `melee_damage` : int
        The damage dealt by the soldier when melee attacking.
    `walking_velocity` : float
        The walking velocity of the soldier.
    `running_velocity` : float
        The running velocity of the soldier.
    `patrol_pace` : int
        The time the soldier takes to rest after reaching a checkpoint.
    `time_to_recover` : int
        The time the soldier takes to recover after being hit by Banjo.
    `melee_impact_texture_indices` : list[int]
        The texture indices where melee impact occurs.
    `shoot_impact_texture_indices` : list[int]
        The texture indices where shooting impact occurs.

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
    def __init__(
            self,
            texture_dict: dict[str, list[tuple[arcade.Texture, arcade.Texture]]],
            animation_fps: dict[str, float],
            hp: int,
            shooting_range: int,
            melee_range: int,
            hearing_range: int,
            accuracy: float,
            shooting_damage: int,
            mag_size: int,
            melee_damage: int,
            walking_velocity: float,
            running_velocity: float,
            patrol_pace: int,
            time_to_recover: int,
            melee_impact_texture_indices: list[int],
            shoot_impact_texture_indices: list[int]
        ) -> None:
        """ Initialize the Soldier 1 NPC.
        """
        super().__init__(scale=1)

        self.texture_dict = texture_dict

        self.time_since_last_frame = 0.0
        self.time_since_last_coordinate = 0.0
        self.time_since_last_hit = 0.0
        self.animation_fps = animation_fps

        # Gameplay stats
        self.fsm = SoldierFSM(
            hp=hp,
            shooting_range=shooting_range,
            melee_range=melee_range,
            hearing_range=hearing_range,
            mag_size=mag_size
        )
        self.accuracy = accuracy
        self.shooting_damage = shooting_damage
        self.mag_size = mag_size
        self.melee_damage = melee_damage

        # Physics variables
        self.walking_velocity = walking_velocity
        self.running_velocity = running_velocity
        self.patrol_pace = patrol_pace
        self.time_to_recover = time_to_recover

        # Animation variables
        self.is_reloading = False
        self.is_alert = False
        self.is_dying = False
        self.is_dead = False
        self.texture = self.texture_dict[self.current_state][0][0]
        self.character_facing_direction = RIGHT_FACING
        self.current_texture_index = 0
        self.melee_impact_texture_indices = melee_impact_texture_indices
        self.shoot_impact_texture_indices = shoot_impact_texture_indices

        # Sound variable
        self.sound_amp = 1.0
        self.pan = 0.0

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

        self.current_texture_index += 1

    def turn(self) -> None:
        """ Play the turning animation.

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
        >>> soldier_1.shoot()
        """
        self.change_x = 0

        current_texture = self.texture_dict[self.current_state]

        if self.current_texture_index > len(current_texture) - 1:
            self.current_texture_index = 0

        self.texture = current_texture[self.current_texture_index][self.character_facing_direction]

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
                banjo.damaged(self.shooting_damage)

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
            banjo.damaged(self.melee_damage)

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

        # Most left is -1, most right is 1
        self.pan = (self.center_x - banjo.center_x) / banjo.hearing_range
        self.pan = max(-1.0, min(1.0, self.pan))

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