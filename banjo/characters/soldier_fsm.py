from __future__ import annotations

__all__ = ["SoldierFSM"]

from statemachine import StateMachine, State
from banjo.resources.game_constants import RIGHT_FACING


class SoldierFSM(StateMachine):
    """ `banjo.characters.SoldierFSM` is a state machine that defines the
    different states and transitions of a soldier character in a game.

    The soldier can be in one of the following states:
    - Idle: The soldier is not doing anything. We start in this state.
    - Walking: The soldier is walking.
    - Running: The soldier is running.
    - Shooting: The soldier is shooting at an enemy.
    - Reloading: The soldier is reloading their weapon.
    - Melee: The soldier is attacking an enemy with a melee weapon.
    - Hurting: The soldier is being hit by an enemy.
    - Dying: The soldier is dying. We cannot exit this state.

    The soldier can transition between these states based on certain conditions.
    The transitions are defined in the `cycle` variable, which is a combination
    of the different states and their conditions.

    Different conditions will define the behavior of the soldier in the game,
    such as whether they would prioritize certain actions over others.

    Parameters
    ----------
    `hp` : int, optional, default=30
        The soldier's health points.
    `shooting_range` : int, optional, default=800
        The range of the soldier's shooting.
    `melee_range` : int, optional, default=100
        The range of the soldier's melee attack.
    `shooting_damage` : int, optional, default=10
        The damage dealt by the soldier's shooting.
    `melee_damage` : int, optional, default=20
        The damage dealt by the soldier's melee attack.
    `shooting_accuracy` : float, optional, default=0.6
        The accuracy of the soldier's shooting.
    `mag_size` : int, optional, default=20
        The size of the soldier's magazine.

    Attributes
    ----------
    `hp` : int
        The soldier's health points.
    `shooting_range` : int
        The range of the soldier's shooting.
    `melee_range` : int
        The range of the soldier's melee attack.
    `hearing_range` : int
        The range within which the soldier can hear the enemy.
    `mag_size` : int
        The size of the soldier's magazine.
    `current_mag` : int
        The current number of bullets in the soldier's magazine.
    `patrol_checkpoints` : list[int]
        The list of patrol checkpoints for the soldier.
    `chase_to` : int or None
        The x-coordinate of the enemy the soldier is chasing, or None if not chasing.
    `take_a_break` : bool
        Whether the soldier is taking a break during patrol.
    `reload_done` : bool
        Whether the soldier has finished reloading.
    `alert_done` : bool
        Whether the soldier has finished alerting.
    `is_recovered` : bool
        Whether the soldier has recovered from being hit.

    Usage
    -----
    >>> soldier = SoldierFSM()
    >>> soldier.cycle(**kwargs)
    """
    idle = State("idle", initial=True)
    walk = State("walk")
    run = State("run")
    shoot = State("shoot")
    reload = State("reload")
    melee = State("melee")
    alert = State("alert")
    hurt = State("hurt")
    dead = State("dead")
    at_ease = State("at_ease")

    # Transitions are evaluated in the order which
    # they are defined
    # Use the order to define precedence
    cycle = \
        idle.to(at_ease, cond="enemy_dead") | \
        idle.to(hurt, cond="is_being_hit") | \
        idle.to(melee, cond="can_melee") | \
        idle.to(reload, cond="mag_empty") | \
        idle.to(shoot, cond="can_shoot") | \
        idle.to(alert, cond="can_hear") | \
        idle.to(run, cond="can_chase") | \
        idle.to(walk, cond="can_patrol") | \
        idle.to(idle) | \
        walk.to(at_ease, cond="enemy_dead") | \
        walk.to(hurt, cond="is_being_hit") | \
        walk.to(melee, cond="can_melee") | \
        walk.to(reload, cond="mag_empty") | \
        walk.to(shoot, cond="can_shoot") | \
        walk.to(alert, cond="can_hear") | \
        walk.to(run, cond="can_chase") | \
        walk.to(walk, cond="can_patrol") | \
        walk.to(idle, cond="can_take_a_break") | \
        walk.to(at_ease) | \
        run.to(at_ease, cond="enemy_dead") | \
        run.to(hurt, cond="is_being_hit") | \
        run.to(melee, cond="can_melee") | \
        run.to(reload, cond="mag_empty") | \
        run.to(shoot, cond="can_shoot") | \
        run.to(alert, cond="can_hear") | \
        run.to(run, cond="can_chase") | \
        run.to(walk, cond="can_patrol") | \
        run.to(idle) | \
        shoot.to(at_ease, cond="enemy_dead") | \
        shoot.to(hurt, cond="is_being_hit") | \
        shoot.to(melee, cond="can_melee") | \
        shoot.to(reload, cond="mag_empty") | \
        shoot.to(shoot, cond="can_shoot") | \
        shoot.to(run, cond="can_chase") | \
        shoot.to(idle) | \
        melee.to(at_ease, cond="enemy_dead") | \
        melee.to(hurt, cond="is_being_hit") | \
        melee.to(melee, cond="can_melee") | \
        melee.to(reload, cond=["mag_empty", "can_shoot"]) | \
        melee.to(shoot, cond="can_shoot") | \
        melee.to(run, cond="can_chase") | \
        melee.to(idle) | \
        reload.to(at_ease, cond="enemy_dead") | \
        reload.to(hurt, cond="is_being_hit") | \
        reload.to(melee, cond="can_melee") | \
        reload.to(idle, cond="finish_reloading") | \
        reload.to(reload, cond="mag_empty") | \
        reload.to(shoot, cond="can_shoot") | \
        reload.to(alert, cond="can_hear") | \
        reload.to(run, cond="can_chase") | \
        reload.to(idle) | \
        hurt.to(at_ease, cond="enemy_dead") | \
        hurt.to(dead, cond="is_dying") | \
        hurt.to(hurt, cond="(is_being_hit and can_melee) or !has_recovered") | \
        hurt.to(idle) | \
        alert.to(at_ease, cond="enemy_dead") | \
        alert.to(hurt, cond="is_being_hit") | \
        alert.to(melee, cond="can_melee") | \
        alert.to(reload, cond="mag_empty") | \
        alert.to(shoot, cond="can_shoot") | \
        alert.to(idle, cond="finish_alert") | \
        alert.to(alert, cond="can_hear") | \
        alert.to(run, cond="can_chase") | \
        alert.to(walk, cond="can_patrol") | \
        alert.to(idle) | \
        at_ease.to(at_ease) | \
        dead.to(dead)

    def __init__(
            self,
            hp: int = 30,
            shooting_range: int = 800,
            melee_range: int = 100,
            hearing_range: int = 1000,
            mag_size: int = 20
        ) -> None:
        """ Initialize a `banjo.characters.SoldierFSM` instance.
        """
        # Soldier specific attributes
        self.hp = hp
        self.shooting_range = shooting_range
        self.melee_range = melee_range
        self.hearing_range = hearing_range
        self.mag_size = mag_size

        # General attributes
        self.current_mag = self.mag_size
        self.patrol_checkpoints: list[int] = []
        self.chase_to = None
        self.take_a_break = False

        # Environment specific attributes
        self.reload_done = False
        self.alert_done = False
        self.is_recovered = True

        super().__init__()

    def set_patrol_checkpoints(
            self,
            patrol_checkpoints: list[int]
        ) -> None:
        """ Set the patrol checkpoints for the soldier.

        Parameters
        ----------
        `patrol_checkpoints` : list[int]
            The list of patrol checkpoints for the soldier.
        """
        self.patrol_checkpoints = patrol_checkpoints

    def can_hear(
            self,
            soldier_coordinate: tuple[int, int],
            enemy_coordinate: tuple[int, int],
            enemy_barking: bool
        ) -> bool:
        """ Check if the soldier can hear an enemy.

        Parameters
        ----------
        `soldier_coordinate` : tuple[int, int]
            The coordinate of the soldier.
        `enemy_coordinate` : tuple[int, int]
            The coordinate of the enemy.
        `enemy_barking` : bool
            True if the enemy is barking, False otherwise.

        Returns
        -------
        bool
            True if the soldier can hear the enemy, False otherwise.
        """
        can_hear = abs(soldier_coordinate[0] - enemy_coordinate[0]) <= self.hearing_range and enemy_barking

        if can_hear:
            self.chase_to = enemy_coordinate[0]

        return can_hear

    def finish_alert(self) -> bool:
        """ Check if the soldier has finished alerting.

        Returns
        -------
        bool
            True if the soldier has finished alerting, False otherwise.
        """
        alert_done = self.alert_done

        if alert_done:
            self.alert_done = False

        return alert_done

    def can_take_a_break(self) -> bool:
        """ Check if the soldier can take a break.

        Returns
        -------
        bool
            True if the soldier can take a break, False otherwise.
        """
        return self.take_a_break

    def can_patrol(
            self,
            soldier_coordinate: tuple[int, int]
        ) -> bool:
        """ Check if the soldier can patrol.

        Parameters
        ----------
        `soldier_coordinate` : tuple[int, int]
            The coordinate of the soldier.

        Returns
        -------
        bool
            True if the soldier can patrol, False otherwise.
        """
        if not self.patrol_checkpoints:
            return False

        if abs(soldier_coordinate[0] - self.patrol_checkpoints[-1]) > 10:
            return True

        self.take_a_break = True

        return False

    def can_chase(
            self,
            soldier_coordinate: tuple[int, int]
        ) -> bool:
        """ Check if the soldier can chase an enemy.

        Parameters
        ----------
        `soldier_coordinate` : tuple[int, int]
            The coordinate of the soldier.

        Returns
        -------
        bool
            True if the soldier can chase an enemy, False otherwise.
        """
        if self.chase_to is not None:
            if abs(soldier_coordinate[0] - self.chase_to) > 10:
                return True

            # Reset when nothing is being chased
            self.chase_to = None

        return False

    def can_shoot(
            self,
            soldier_coordinate: tuple[int, int],
            soldier_facing_direction: int,
            enemy_coordinate: tuple[int, int],
        ) -> bool:
        """ Check if the soldier can shoot an enemy.

        Parameters
        ----------
        `soldier_coordinate` : tuple[int, int]
            The coordinate of the soldier.
        `soldier_facing_direction` : int
            The direction the soldier is facing (0 for right, 1 for left).
        `enemy_coordinate` : tuple[int, int]
            The coordinate of the enemy.

        Returns
        -------
        `can_shoot` : bool
            True if the soldier can shoot the enemy, False otherwise.
        """
        can_shoot = False

        if abs(enemy_coordinate[1] - soldier_coordinate[1]) > 50:
            return can_shoot

        if soldier_facing_direction == RIGHT_FACING:
            if (
                enemy_coordinate[0] > soldier_coordinate[0]
                and abs(enemy_coordinate[0] - soldier_coordinate[0]) < self.shooting_range
            ):
                can_shoot = True

        else:
            if (
                enemy_coordinate[0] < soldier_coordinate[0]
                and abs(enemy_coordinate[0] - soldier_coordinate[0]) < self.shooting_range
            ):
                can_shoot = True

        if can_shoot:
            self.chase_to = enemy_coordinate[0]

        return can_shoot

    def can_melee(
            self,
            soldier_coordinate: tuple[int, int],
            enemy_coordinate: tuple[int, int]
        ) -> bool:
        """ Check if the soldier can melee an enemy.

        Parameters
        ----------
        `soldier_coordinate` : tuple[int, int]
            The coordinate of the soldier.
        `enemy_coordinate` : tuple[int, int]
            The coordinate of the enemy.

        Returns
        -------
        `can_melee` : bool
            True if the soldier can melee the enemy, False otherwise.
        """
        can_melee = False

        if abs(enemy_coordinate[1] - soldier_coordinate[1]) > 50:
            return can_melee

        if abs(enemy_coordinate[0] - soldier_coordinate[0]) < self.melee_range:
            can_melee = True

        if can_melee:
            self.chase_to = enemy_coordinate[0]

        return can_melee

    def mag_empty(self) -> bool:
        """ Check if the soldier's magazine is empty.

        Returns
        -------
        bool
            True if the soldier's magazine is empty, False otherwise.
        """
        return self.current_mag == 0

    def finish_reloading(self) -> bool:
        """ Check if the soldier has finished reloading.

        Returns
        -------
        bool
            True if the soldier has finished reloading, False otherwise.
        """
        reload_done = self.reload_done

        if reload_done:
            self.current_mag = self.mag_size
            self.reload_done = False

        return reload_done

    def is_being_hit(
            self,
            soldier_coordinate: tuple[int, int],
            enemy_hitting: bool,
            enemy_coordinate: tuple[int, int]
        ) -> bool:
        """ Check if the soldier is being hit by an enemy.

        Parameters
        ----------
        `soldier_coordinate` : tuple[int, int]
            The coordinate of the soldier.
        `enemy_hitting` : bool
            True if the soldier is being hit, False otherwise.
        `enemy_coordinate` : tuple[int, int]
            The coordinate of the enemy.

        Returns
        -------
        bool
            True if the soldier is being hit, False otherwise.
        """
        if enemy_hitting:
            if abs(enemy_coordinate[1] - soldier_coordinate[1]) > 50:
                return False

            if abs(enemy_coordinate[0] - soldier_coordinate[0]) < self.melee_range:
                self.is_recovered = False
                return True

        return enemy_hitting

    def has_recovered(self) -> bool:
        """ Check if the soldier has recovered from being hit.

        Returns
        -------
        bool
            True if the soldier has recovered, False otherwise.
        """
        return self.is_recovered

    def is_dying(self) -> bool:
        """ Check if the soldier is dying.

        Returns
        -------
        bool
            True if the soldier is dying, False otherwise.
        """
        return self.hp <= 0

    def enemy_dead(
            self,
            enemy_hp: int
        ) -> bool:
        """ Check if the enemy is dead.

        Parameters
        ----------
        `enemy_hp` : int
            The health points of the enemy.

        Returns
        -------
        bool
            True if the enemy is dead, False otherwise.
        """
        return enemy_hp <= 0