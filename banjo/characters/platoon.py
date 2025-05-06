from __future__ import annotations

__all__ = ["Platoon"]

import arcade
from banjo.characters import Soldier1
import random


class Platoon(arcade.SpriteList):
    """ `banjo.characters.Platoon` is the class that manages the group behavior
    of soldiers in the game.

    Parameters
    ----------
    `soldiers` : list[banjo.characters.Soldier1]
        The list of soldiers that are part of the platoon.

    Attributes
    ----------
    `soldiers` : list[banjo.characters.Soldier1]
        The list of soldiers that are part of the platoon.

    Usage
    -----
    >>> platoon = Platoon(soldiers)
    """
    def __init__(
            self,
            soldiers: list[Soldier1]
        ) -> None:
        """ Initializes the platoon with a list of soldiers.
        """
        super().__init__(use_spatial_hash=True)
        self.soldiers = soldiers

        for soldier in soldiers:
            self.append(soldier)

    def converge(
            self,
            target_position: int
        ) -> None:
        """ Sets all platoon members to converge on the target position.

        Parameters
        ----------
        `target_position` : int
            The target position for the soldiers to converge on.

        Usage
        -----
        >>> platoon.converge(100)
        """
        # Add a random offset to the target position for each soldier
        # to avoid soldiers standing in the same spot
        for soldier in self.soldiers:
            soldier.fsm.chase_to = target_position + random.randint(-300, 300)

    def shots_fired(self) -> None:
        """ Sets all platoon members to converge on where the
        shot came from.

        Usage
        -----
        >>> platoon.shots_fired()
        """
        for soldier in self.soldiers:
            if soldier.current_state == "shoot":
                # When shooting, `soldier.chase_to` will
                # never be None, so we use type: ignore to
                # silence pylance
                self.converge(soldier.chase_to) # type: ignore

    def update(
            self,
            delta_time: float=1/60,
            *args, # type: ignore
            **kwargs # type: ignore
        ) -> None:

        banjo = kwargs.get("banjo")

        if banjo is None:
            raise ValueError("Banjo object must be passed as a keyword argument.")

        for soldier in self.soldiers:
            soldier.update(delta_time, banjo=banjo)

        self.shots_fired()