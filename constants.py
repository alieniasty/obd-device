from enum import Enum

class PidTypes(Enum):
    SPEED = 1
    FUEL_LEVEL = 2
    RPM = 3
    MAF = 4
    RUN_TIME = 5

class Units(Enum):
    kmh = 1
    percent = 2
    rpm = 3
    grams_per_second = 4
    seconds = 5