from typing import Tuple, List

from config import ModelConfig
from model_space.prediction_model.utils.history_parser import get_line_angle, get_history_angles, \
    get_new_list_with_angle_appended, get_angle_changes, get_angle_change_consistency
from model_space.utils.point import Point


def get_correct_prediction(possible_locations: Tuple[Point, Point], history: List[Point]):
    angle_location1 = get_line_angle(history[-1], possible_locations[0])
    angle_location2 = get_line_angle(history[-1], possible_locations[1])

    angle_history = get_history_angles(history, ModelConfig.mn_history_usage)
    angles_to_location1 = get_new_list_with_angle_appended(angle_history, angle_location1)
    angles_to_location2 = get_new_list_with_angle_appended(angle_history, angle_location2)

    angle_changes_1 = get_angle_changes(angles_to_location1)
    angle_changes_2 = get_angle_changes(angles_to_location2)
    consistency1 = get_angle_change_consistency(angle_changes_1)
    consistency2 = get_angle_change_consistency(angle_changes_2)

    if consistency1 < consistency2:
        return possible_locations[0]
    else:
        return possible_locations[1]
