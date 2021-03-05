from enum import IntEnum


class ShipCondition(IntEnum):
    """ Used to render the correct ship sprites """
    HEALTHY = 0
    DAMAGED = 1
    VERY_DAMAGED = 2
    SUNK = 3
