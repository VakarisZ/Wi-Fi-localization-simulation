import math
from math import acos, cos, sin
from typing import List, Tuple

from config import ModelConfig
from model_space.prediction_model.curve_fitter import fix_prediction_using_curve_fit, \
    get_curve_fit_cofs, curve_fit_to_history
from model_space.prediction_model.prediction_choosers import two_sn_choice, one_sn_choice
from model_space.prediction_model.utils.prediction_dto import MnLocationPrediction
from model_space.utils.point import Point
from model_space.utils.stationary_node import StationaryNode


def get_node_prediction(history: List[MnLocationPrediction],
                        sn_params: List[StationaryNode],
                        mn_speed: float) -> MnLocationPrediction:
    full_history = history
    history = [point.location for point in history]

    if ModelConfig.curve_fitting_history_count < ModelConfig.curve_fitting_points_count:
        ModelConfig.curve_fitting_history_count += 1

    if ModelConfig.do_curve_fitting and ModelConfig.curve_fitting_history_count > 5:
        prediction = get_prediction_with_curve_fit(history, sn_params, mn_speed)
        # Check if more sn's can fix incorrect predictions
        if is_sn_count_bigger(full_history[-1].sn_list, sn_params)\
                and is_prediction_incorrect(prediction, sn_params):
            prediction = get_prediction_from_history(history, sn_params, mn_speed)
            ModelConfig.curve_fitting_history_count = 1
    else:
        prediction = get_prediction_from_history(history, sn_params, mn_speed)

    return MnLocationPrediction(prediction, sn_params)


def get_prediction_from_history(history: List[Point],
                                sn_params: List[StationaryNode],
                                mn_speed: float) -> MnLocationPrediction:
    possible_locations = calculate_possible_locations(history, sn_params, mn_speed)
    if len(sn_params) > 1:
        predicted_location = two_sn_choice.get_correct_prediction(possible_locations,
                                                                  history[-1],
                                                                  mn_speed)
    else:
        predicted_location = one_sn_choice.get_correct_prediction(possible_locations, history)

    return predicted_location


def get_prediction_with_curve_fit(history: List[Point],
                                  sn_params: List[StationaryNode],
                                  mn_speed: float) -> MnLocationPrediction:
    fit_curve = get_curve_fit_cofs(history)
    fit_curve = curve_fit_to_history(fit_curve)

    possible_locations = calculate_possible_locations(fit_curve, sn_params, mn_speed)
    if len(sn_params) > 1:
        predicted_location = two_sn_choice.get_correct_prediction(possible_locations,
                                                                  fit_curve[-1],
                                                                  mn_speed)
    else:
        predicted_location = one_sn_choice.get_correct_prediction(possible_locations, fit_curve)

    return fix_prediction_using_curve_fit(predicted_location, fit_curve)


def calculate_possible_locations(history: List[Point],
                                 sn_params: List[StationaryNode],
                                 mn_speed: float) -> Tuple[Point, Point]:
    # for two stationary nodes, don't use history
    if len(sn_params) > 1:
        pnt1 = sn_params[0].coords
        pnt2 = sn_params[1].coords
        # Sides are marked according to the point they oppose, e.g. d12 is opposite to point 3, d23 to point 1 etc.
        d12 = math.dist(pnt1.as_list(), pnt2.as_list())
        d13 = sn_params[0].distance_to_mn
        d23 = sn_params[1].distance_to_mn
    else:
        # We need to do the calculations with the same sn
        pnt1 = history[-1]
        pnt2 = sn_params[0].coords
        d12 = math.dist(pnt1.as_list(), pnt2.as_list())  # Distance 12
        d13 = float(mn_speed)  # Distance 13
        d23 = sn_params[0].distance_to_mn  # Distance 23

    return get_third_point_locations(pnt1, pnt2, d12, d13, d23)


def get_third_point_locations(pnt1: Point,
                              pnt2: Point,
                              d12: float,
                              d13: float,
                              d23: float):
    x1 = pnt1.x
    y1 = pnt1.y
    x2 = pnt2.x
    y2 = pnt2.y

    u = x2 - x1
    v = y2 - y1

    cos_ther_result = (d12 ** 2 + d13 ** 2 - d23 ** 2) / (2 * d12 * d13)
    a1 = acos_error_compliant(cos_ther_result)  # Angle 1

    RHS1 = x1 * u + y1 * v + d13 * d12 * cos(a1)
    RHS2 = y2 * u - x2 * v + d13 * d12 * sin(a1)
    x3 = (1 / d12 ** 2) * (u * RHS1 - v * RHS2)
    y3 = (1 / d12 ** 2) * (v * RHS1 + u * RHS2)

    RHS2_alt = y2 * u - x2 * v - d13 * d12 * sin(a1)
    x3_alt = (1 / d12 ** 2) * (u * RHS1 - v * RHS2_alt)
    y3_alt = (1 / d12 ** 2) * (v * RHS1 + u * RHS2_alt)

    p1 = Point(x3, y3)
    p2 = Point(x3_alt, y3_alt)

    return p1, p2


# TODO move this method
def get_sn_from_list(node_id: str, node_list: List[StationaryNode]) -> StationaryNode:
    node = [sn for sn in node_list if sn.id == node_id]
    if not node:
        return node_list[0]
    return node[0]


def acos_error_compliant(value: float):
    if value > 1:
        return acos(1)
    elif value < -1:
        return acos(-1)
    else:
        return acos(value)


def is_sn_count_bigger(last_sn_list: List, current_sn_list: List):
    return len(last_sn_list) < len(current_sn_list) and len(last_sn_list) == 1


# Check if prediction is obviously incorrect based on sn_params
def is_prediction_incorrect(prediction: Point, sn_params: List[StationaryNode]):
    diff1 = abs(math.dist([prediction.x, prediction.y],
                          [sn_params[0].coords.x, sn_params[0].coords.y])
                - sn_params[0].distance_to_mn)
    diff2 = abs(math.dist([prediction.x, prediction.y],
                          [sn_params[1].coords.x, sn_params[1].coords.y])
                - sn_params[1].distance_to_mn)
    return diff1 > 10 or diff2 > 10
