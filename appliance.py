from enum import Enum


class Priority(Enum):
    LOW = 1
    HIGH = 2
    CRITICAL = 3


class Appliance:
    def __init__(self, name: str, power_draw: float, priority: Priority):
        self.name = name
        self.power_draw = power_draw
        self.priority = priority
        self.is_on = False

    def turn_on(self):
        self.is_on = True

    def turn_off(self):
        self.is_on = False
