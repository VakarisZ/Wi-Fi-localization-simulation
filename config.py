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

    # Global params
    sim_cnt = 30

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
    mn_history_usage = 5
    mn_history_count = 30
