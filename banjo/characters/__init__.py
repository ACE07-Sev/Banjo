__all__ = [
    "Banjo",
    "Soldier",
    "Soldier1",
    "Soldier2",
    "Soldier3",
    "Platoon",
    "SOLDIER_TYPE"
]

from banjo.characters.banjo_player import Banjo
from banjo.characters.soldier_interface import Soldier
from banjo.characters.soldier_1 import Soldier1
from banjo.characters.soldier_2 import Soldier2
from banjo.characters.soldier_3 import Soldier3
from banjo.characters.platoon import Platoon

SOLDIER_TYPE = Soldier1 | Soldier2 | Soldier3