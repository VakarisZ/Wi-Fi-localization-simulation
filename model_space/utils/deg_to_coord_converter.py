import math
from dataclasses import dataclass

FIRST_QUADRANT = 1  # 1st quadrant = +x/+y
SECOND_QUADRANT = 2  # 2nd = -x/+y
THIRD_QUADRANT = 3  # 3rd = -x/-y
FOURTH_QUADRANT = 4  # 4th = +x/-y


@dataclass
class CoordsChange:
    x_change: float
    y_change: float

    def __init__(self, degrees, speed):
        quadrant_values = get_quadrant_values_from_degrees(degrees)
        self.x_change = calc_x_change(speed, quadrant_values)
        self.y_change = calc_y_change(speed, quadrant_values)


@dataclass
class QuadrantValues:
    x_positivity: int
    y_positivity: int
    degrees: float

    def __init__(self, degrees, quadrant):
        if quadrant == FIRST_QUADRANT:
            self.x_positivity = +1
            self.y_positivity = +1
            self.degrees = degrees
        elif quadrant == SECOND_QUADRANT:
            self.x_positivity = -1
            self.y_positivity = +1
            self.degrees = 180 - degrees
        elif quadrant == THIRD_QUADRANT:
            self.x_positivity = -1
            self.y_positivity = -1
            self.degrees = degrees - 180
        elif quadrant == FOURTH_QUADRANT:
            self.x_positivity = +1
            self.y_positivity = -1
            self.degrees = 360 - degrees
        else:
            raise Exception("Unknown quadrant")


def calc_x_change(speed, quadrant_values):
    x_change = calc_sine_theorem(calc_last_corner(quadrant_values.degrees), speed)
    x_change *= quadrant_values.x_positivity
    return x_change


def calc_y_change(speed, quadrant_values):
    y_change = calc_sine_theorem(quadrant_values.degrees, speed)
    y_change *= quadrant_values.y_positivity
    return y_change


def get_quadrant_values_from_degrees(degrees) -> QuadrantValues:
    degrees = normalize_trajectory_degrees(degrees)
    quadrant = get_quadrant_from_degrees(degrees)
    return QuadrantValues(degrees, quadrant)


def normalize_trajectory_degrees(degrees):
    # Convert negative degrees to positive
    if degrees < 0:
        return 360 + degrees
    elif degrees >= 360:
        return degrees - 360
    else:
        return degrees


def get_quadrant_from_degrees(degrees):
    if 0 <= degrees <= 90:
        return FIRST_QUADRANT
    elif 90 < degrees <= 180:
        return SECOND_QUADRANT
    elif 180 < degrees <= 270:
        return THIRD_QUADRANT
    elif 270 < degrees <= 360:
        return FOURTH_QUADRANT


def calc_sine_theorem(degrees, speed):
    return abs(speed * math.sin(math.radians(degrees)) / math.sin(math.radians(90)))


def calc_last_corner(degrees):
    return 180 - 90 - degrees
