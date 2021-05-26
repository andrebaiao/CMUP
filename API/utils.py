from enum import Enum

SUCCESS = 200
CREATED = 201
ERROR = 500
FORBIDDEN = 403


class Day(Enum):
    MON = 1
    TUE = 2
    WED = 3
    THU = 4
    FRI = 5
    SAT = 6
    SUN = 7


class PartOfDay(Enum):
    BRK = 1
    LUN = 2
    DIN = 3
    NIG = 4
