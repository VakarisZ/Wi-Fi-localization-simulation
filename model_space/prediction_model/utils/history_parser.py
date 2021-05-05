import math
from copy import deepcopy
from math import atan2
from typing import List

from model_space.prediction_model.utils.prediction_dto import MnLocationPrediction
from model_space.utils.point import Point


def get_angle_changes(angle_list: List[float]) -> List[float]:
    angle_changes = []

    for i in range(0, len(angle_list) - 1):
        angle_changes.append(angle_list[i] - angle_list[i + 1])

    return angle_changes


def get_new_list_with_angle_appended(angle_list: List[float], angle: float):
    new_list = deepcopy(angle_list)
    new_list.append(angle)
    return new_list


def get_history_angles(history: List[Point], count: int) -> List[float]:
    line_angles = []
    for i in range(-count, 1):
        point_1 = history[i]
        point_2 = history[i + 1]
        line_angles.append(get_line_angle(point_1, point_2))
    return line_angles


def get_line_angle(point_1: Point, point_2: Point):
    angle = atan2(point_2.x - point_1.x, point_2.y - point_1.y)

    if angle < 0:
        angle += (math.pi * 2)

    return math.degrees(angle)


# TODO unused
def get_angle_prediction(angle_history: List[float]):
    prediction = 0
    prediction += angle_history[-1] / 100 * 70
    prediction += angle_history[-2] / 100 * 20
    prediction += angle_history[-3] / 100 * 10
    return prediction


def compare_angle_change_consistency(angle_changes1: List[float], angle_changes2: List[float]):
    consistency1 = get_angle_change_consistency(angle_changes1)
    consistency2 = get_angle_change_consistency(angle_changes2)
    if consistency1 < consistency2:
        return angle_changes1
    else:
        return angle_changes2


# TODO improve this method
def get_angle_change_consistency(angle_changes: List[float]):
    overflow = abs(angle_changes[-2] - angle_changes[-1] + 360)
    underflow = abs(angle_changes[-2] - angle_changes[-1] - 360)
    no_overflow = abs(angle_changes[-2] - angle_changes[-1])
    return min([no_overflow, overflow, underflow])


def get_angle_diff(angle_one: float, angle_two: float) -> float:
    temp_angle = abs(angle_one-angle_two) % 360
    return 360 - temp_angle if temp_angle > 180 else temp_angle


def get_correct_angle(angle_choice: List[float], target: float) -> float:
    diff1 = abs(angle_choice[0] - target)
    diff2 = abs(angle_choice[1] - target)
    if diff1 < diff2:
        return angle_choice[0]
    else:
        return angle_choice[1]


def get_average_distance_between_measurements(history: List[Point]):
    distance_sum = 0
    for i in range(len(history)-1):
        distance_sum += math.dist([history[i].x, history[i].y],
                                  [history[i+1].x, history[i+1].y])

