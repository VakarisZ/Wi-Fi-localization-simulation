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


@dataclass
class AreaParams:
    x_min: float
    x_max: float
    y_min: float
    y_max: float


@dataclass
class ModelConfig:
    # Global params
    random_seed = 'test6'
    area = AreaParams(x_min=-50, x_max=50, y_min=-50, y_max=50)
    mobile_node_params = MobileNodeParams(start_coords=Point(x=0, y=0), speed=1)
    stationary_node_param_list = [StationaryNodeParams(location_coords=Point(-90, 50), range=110),
                                  StationaryNodeParams(location_coords=Point(0, -70), range=110),
                                  StationaryNodeParams(location_coords=Point(90, 75), range=110)]

    # Mobile node params
    turn_sharpness_range = (1, 10)  # Percent per iteration
    collision_avoidance_turn_sharpness_range = (8, 12)  # We want sharper turns to avoid collision
    angle_change_range = (-180, 180)  # Angles to turn
    danger_range = 17  # Percentage of danger in the map zone, where node should turn away in order not to hit the wall.
