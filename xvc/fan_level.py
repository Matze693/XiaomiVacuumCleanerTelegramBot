from enum import Enum


class FanLevel(Enum):
    """
    Enum for distinct fan levels.
    """
    Quiet = 38
    Balanced = 60
    Turbo = 75
    Max = 100
    Mob = 105
