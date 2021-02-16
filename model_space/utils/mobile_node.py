from initial_config import ModelConfig, MobileNodeParams
from model_space.utils.colision_avoidance import get_direction_by_danger_walls, is_colision_avoidance_needed, \
    DangerWalls, get_best_angle_change
from model_space.utils.deg_to_coord_converter import CoordsChange, normalize_trajectory_degrees
from model_space.utils.mobile_node_utils.random_param_fetcher import get_random_angle_change, get_random_turn_sharpness, \
    get_random_avoidance_turn_sharpness, get_random_trajectory
from model_space.utils.node import Node


class MobileNode(Node):

    def __init__(self, mobile_node_params: MobileNodeParams):
        super().__init__(mobile_node_params.start_coords, {'color': 'red', 'marker': 'o', 'markersize': 5})
        # How much distance node covers in an iteration
        self.speed = mobile_node_params.speed
        # Trajectory of the next step. If it's 90 it will move straight up an amount of speed
        self.current_trajectory = get_random_trajectory()
        # Where the node is turning towards
        self.angle_change = 0
        # What was the initial angle change. Used to determine if node completed the turn.
        self.initial_angle_change = 0
        # How many degrees a node can turn in one iteration
        self.turn_sharpness = 0
        # Which walls node was close to
        self.danger_walls = DangerWalls()

        self.setup_new_turn()

    def setup_new_turn(self, angle_change=None, turn_sharpness=None):
        if not angle_change:
            self.angle_change = get_random_angle_change()
        else:
            self.angle_change = angle_change
        self.initial_angle_change = self.angle_change
        if not turn_sharpness:
            self.turn_sharpness = get_random_turn_sharpness()
        else:
            self.turn_sharpness = turn_sharpness

    def move(self):
        if self._avoid_clashing_into_wall():
            pass
        elif self._is_angle_change_finished():
            self.setup_new_turn()
        if self.angle_change < 0:
            self.current_trajectory -= self.turn_sharpness
            self.angle_change += self.turn_sharpness
        elif self.angle_change > 0:
            self.current_trajectory += self.turn_sharpness
            self.angle_change -= self.turn_sharpness

        self.current_trajectory = normalize_trajectory_degrees(self.current_trajectory)
        self._move_in_dir(self.current_trajectory)

    def _is_angle_change_finished(self):
        if self.initial_angle_change > 0 >= self.angle_change:
            return True
        elif self.initial_angle_change < 0 <= self.angle_change:
            return True
        else:
            return False

    def _move_in_dir(self, degrees: float):
        if -360 > degrees > 360:
            raise Exception("Simplify the degrees of the angle!")
        coord_change = CoordsChange(degrees, self.speed)
        self.coords.x += coord_change.x_change
        self.coords.y += coord_change.y_change

    def _avoid_clashing_into_wall(self):
        danger_walls = self._get_close_walls()
        # We need to see if it's needed to re-evaluate collision avoidance
        if not danger_walls.__dict__ == self.danger_walls.__dict__:
            self.danger_walls = danger_walls
            if is_colision_avoidance_needed(danger_walls):
                self._change_direction_to_avoid_clash(danger_walls)
                return True
        return False

    def _change_direction_to_avoid_clash(self, danger_walls):
        new_direction = get_direction_by_danger_walls(danger_walls)
        angle_change = get_best_angle_change(self.current_trajectory, new_direction)
        turn_sharpness = get_random_avoidance_turn_sharpness()
        self.setup_new_turn(angle_change=angle_change, turn_sharpness=turn_sharpness)

    def _get_close_walls(self):
        danger_walls = DangerWalls()
        area = ModelConfig().area
        danger_zone = ModelConfig.danger_range
        if self.coords.x < self._get_min_danger_border(area.x_min, danger_zone):
            danger_walls.left_wall = True
        if self.coords.x > self._get_max_danger_border(area.x_max, danger_zone):
            danger_walls.right_wall = True
        if self.coords.y < self._get_min_danger_border(area.y_min, danger_zone):
            danger_walls.bottom_wall = True
        if self.coords.y > self._get_max_danger_border(area.y_max, danger_zone):
            danger_walls.top_wall = True
        return danger_walls

    def _get_min_danger_border(self, map_border, danger_zone_percent):
        return map_border + abs(map_border / 100 * danger_zone_percent)

    def _get_max_danger_border(self, map_border, danger_zone_percent):
        return map_border - map_border / 100 * danger_zone_percent
