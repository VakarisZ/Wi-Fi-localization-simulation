from dataclasses import dataclass

from model_space.utils.deg_to_coord_converter import normalize_trajectory_degrees


@dataclass
class DangerWalls:
    top_wall = False
    right_wall = False
    bottom_wall = False
    left_wall = False


def is_colision_avoidance_needed(danger_walls: DangerWalls) -> bool:
    return danger_walls.left_wall or \
           danger_walls.top_wall or \
           danger_walls.right_wall or \
           danger_walls.bottom_wall


def get_direction_by_danger_walls(danger_walls: DangerWalls) -> int:
    if danger_walls.top_wall:
        if danger_walls.right_wall:
            return 225
        elif danger_walls.left_wall:
            return 315
        else:
            return 270

    if danger_walls.bottom_wall:
        if danger_walls.right_wall:
            return 135
        elif danger_walls.left_wall:
            return 45
        else:
            return 90

    if danger_walls.right_wall:
        return 180

    if danger_walls.left_wall:
        return 0


def get_best_angle_change(current_dir, avoidance_dir):
    # Get smallest angle change possible
    angle_change = _get_smallest_angle_change(current_dir, avoidance_dir)
    # Turn counter clockwise
    if normalize_trajectory_degrees(current_dir - angle_change) == avoidance_dir:
        return -1 * angle_change
    # Turn clockwise
    else:
        return angle_change


def _get_smallest_angle_change(current_dir, avoidance_dir):
    angle_one = current_dir - avoidance_dir
    if angle_one < 0:
        angle_one = avoidance_dir - current_dir
    angle_two = 360 - angle_one
    if angle_one > angle_two:
        return angle_two
    else:
        return angle_one


def get_opposite_dir(dir):
    return normalize_trajectory_degrees(dir-180)
