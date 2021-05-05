from dataclasses import dataclass

from model_space.utils.point import Point


@dataclass
class MobileNodeParams:
    start_coords: Point
    speed: float


@dataclass
class StationaryNodeParams:
    location_coords: Point
    range: float
    id: str


@dataclass
class AreaParams:
    x_min: float
    x_max: float
    y_min: float
    y_max: float


@dataclass
class ModelConfig:
    # UI:
    show_simulation_plots = False
    show_error_plots = False
    show_only_big_error_plots = False
    show_global_error_plot = True
    wall_color = 'red'
    draw_margin = 5
    show_mn_history = True
    calculate_zone_errors_once = True  # Will not calculate errors for a second entry to the zone.
    # For example if client traveled to 2 brocker zone then to 1 brocker zone, then back to 2,
    # the error calculations is dropped as soon as client re-enters zone with 2 brockers

    # Global params
    sim_cnt = 2000

    seed = 'test'
    iteration_count = 200
    area = AreaParams(x_min=-100, x_max=100, y_min=-100, y_max=100)
    mobile_node_params = MobileNodeParams(start_coords=Point(x=0, y=0), speed=1)
    stationary_node_param_list = [StationaryNodeParams(location_coords=Point(-90, 50), range=110, id=" 1"),
                                  StationaryNodeParams(location_coords=Point(0, -70), range=110, id=" 2"),
                                  StationaryNodeParams(location_coords=Point(90, 75), range=140, id=" 3")]

    # Mobile node params
    turn_sharpness_range = (1, 6)  # Percent per iteration
    collision_avoidance_turn_sharpness_range = (8, 12)  # We want sharper turns to avoid collision
    angle_change_range = (-180, 180)  # Angles to turn
    danger_range = 17  # Percentage of danger in the map zone, where node should turn away in order not to hit the wall.
    move_straight = True
    straight_move_range = (10, 30)  # How many iterations to move straight after a turn

    # Shadow prediction params
    mn_history_usage = 5  # How many history points to use to determine trajectory
    mn_history_count = 200  # How many measurements to keep in history

    # Error ranges (absolute). If 0.1 is specified, the error will be somewhere between -0.1 and 0.1
    sn_distance_error_range = 0.1
    mn_speed_error_range = 0

    # Plots
    prediction_plot = None
    simulation_plot = None

    # Curve fitting assistance
    do_curve_fitting = True
    curve_fitting_min_angle = 50  # How big the angle error needs to be, to trigger fixing of prediction
    angle_adjustment = 20  # How many degrees we need to change from curve fit angle into calculated
    curve_fitting_points_count = 7  # How many points from history to take while implementing curve fitting (fitted curve length)
    curve_fitting_history_count = 10  # Used to track how many history points can be used in curve fitting
    curve_to_history_scale = 4  # How many points are drawn for one history point in fit curve. Depends on speed.
    curve_fitting_k = 2  # Power of function used for fitting
    curve_fitting_s = 2  # Coefficient of smoothing
