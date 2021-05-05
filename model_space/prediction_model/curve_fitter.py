import math
from typing import List

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline

from config import ModelConfig
from model_space.prediction_model.utils.history_parser import get_line_angle, get_angle_diff
from model_space.utils.point import Point


def get_curve_fit_cofs(history: List[Point]) -> List[Point]:

    if ModelConfig.prediction_plot:
        ModelConfig.prediction_plot.clean_history()
        ModelConfig.prediction_plot.clean_curve_fit()

    trimmed_history = history[-ModelConfig.curve_fitting_history_count+1:]

    xdata = [point.x for point in trimmed_history]
    ydata = [point.y for point in trimmed_history]

    points = np.array([xdata,
                       ydata]).T

    distance = np.cumsum(np.sqrt(np.sum(np.diff(points, axis=0) ** 2, axis=1)))
    distance = np.insert(distance, 0, 0) / distance[-1]

    # Build a list of the spline function, one for each dimension:
    splines = [UnivariateSpline(distance,
                                coords,
                                k=ModelConfig.curve_fitting_k,
                                s=ModelConfig.curve_fitting_s) for coords in points.T]

    # Computed the spline for the asked distances:
    alpha = np.linspace(0, 1, 75).data
    points_fitted = np.vstack([spl(alpha) for spl in splines]).T

    if ModelConfig.prediction_plot:
        # ModelConfig.prediction_plot.draw_history(xdata, ydata)
        ModelConfig.prediction_plot.draw_curve_fit_line(*points_fitted.T)
    return [Point(point[0], point[1]) for point in points_fitted]


def curve_fit_to_history(curve_points: List[Point]) -> List[Point]:
    history = []
    start_index = -1
    stop_index = -1 * (ModelConfig.mn_history_usage*ModelConfig.curve_to_history_scale)
    if abs(stop_index) > len(curve_points):
        stop_index = -1 * len(curve_points)
    step = -1 * ModelConfig.curve_to_history_scale
    for i in range(start_index, stop_index, step):
        history.append(curve_points[i])
    history.reverse()
    return history


def fix_prediction_using_curve_fit(predicted_location: Point, interpolated_points: List[Point]) -> Point:
    fixed_prediction = predicted_location
    curve_fit_angle = get_line_angle(interpolated_points[-2], interpolated_points[-1])
    predicted_angle = get_line_angle(interpolated_points[-1], predicted_location)
    angle_diff = get_angle_diff(curve_fit_angle, predicted_angle)
    if angle_diff > ModelConfig.curve_fitting_min_angle:
        angle = get_fixed_prediction_angle(predicted_angle, curve_fit_angle, angle_diff)
        distance = math.dist([predicted_location.x, predicted_location.y],
                             [interpolated_points[-1].x, interpolated_points[-1].y])
        # We should take the average distance from history, but for performance just use 1 instead
        distance = 1
        fixed_prediction = get_new_point_at_angle(interpolated_points[-1], angle, distance)
    return fixed_prediction


# Fix prediction angle to conform to fitted curve
def get_fixed_prediction_angle(predicted_angle: float, curve_fit_angle: float, angle_diff: float):
    diff1 = abs(((curve_fit_angle + angle_diff) % 360) - predicted_angle)
    diff2 = abs(((curve_fit_angle - angle_diff) % 360) - predicted_angle)
    if diff1 < diff2:
        return (curve_fit_angle + ModelConfig.angle_adjustment) % 360
    else:
        return (curve_fit_angle - ModelConfig.angle_adjustment) % 360


def get_new_point_at_angle(point: Point, angle: float, distance: float):
    angle_in_rad = math.pi / 2 - math.radians(angle)
    new_x = point.x + distance * math.cos(angle_in_rad)
    new_y = point.y + distance * math.sin(angle_in_rad)
    return Point(new_x, new_y)


def test_curve_fit_examples():
    theta = np.linspace(-3, 2, 40)
    points = np.vstack((np.cos(theta), np.sin(theta))).T

    # add some noise:
    points = points + 0.05 * np.random.randn(*points.shape)

    # Linear length along the line:
    distance = np.cumsum(np.sqrt(np.sum(np.diff(points, axis=0) ** 2, axis=1)))
    distance = np.insert(distance, 0, 0) / distance[-1]

    # Build a list of the spline function, one for each dimension:
    splines = [UnivariateSpline(distance, coords, k=3, s=.2) for coords in points.T]

    # Computed the spline for the asked distances:
    alpha = np.linspace(0, 1, 75)
    points_fitted = np.vstack(spl(alpha) for spl in splines).T

    # Graph:
    plt.plot(*points.T, 'ok', label='original points')
    plt.plot(*points_fitted.T, '-r', label='fitted spline k=3, s=.2')
    plt.axis('equal')
    plt.legend()
    plt.xlabel('x')
    plt.ylabel('y')


if __name__ == "__main__":
    test_curve_fit_examples()
