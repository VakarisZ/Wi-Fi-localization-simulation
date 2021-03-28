from config import ModelConfig, MobileNodeParams
from model_space.utils.colision_avoidance import get_direction_by_danger_walls, is_colision_avoidance_needed, \
    DangerWalls, get_best_angle_change
from model_space.utils.deg_to_coord_converter import CoordsChange, normalize_trajectory_degrees
from model_space.utils.mobile_node_utils.random_param_fetcher import get_random_angle_change, get_random_turn_sharpness, \
    get_random_avoidance_turn_sharpness, get_random_trajectory
from model_space.utils.mobile_node_utils.straight_mover import StraightMover
from model_space.utils.mobile_node_utils.turner import Turner
from model_space.utils.node import Node


TURNING = 'turning'
MOVING_STRAIGHT = 'moving_straight'


class MobileNode(Node):

    def __init__(self, mobile_node_params: MobileNodeParams):
        super().__init__(mobile_node_params.start_coords, {'color': 'red', 'marker': 'o', 'markersize': 5})
        # How much distance node covers in an iteration
        self.speed = mobile_node_params.speed
        # Trajectory of the next step. If it's 90 it will move straight up an amount of speed
        self.current_trajectory = get_random_trajectory()
        # What type of movement mn is doing
        self.movement_type = MOVING_STRAIGHT
        # Handles turns
        self.turner = Turner()
        # Handles moving straight
        self.straight_mover = StraightMover()
        self.straight_mover.setup_new_move()
        # Which walls node was close to
        self.danger_walls = DangerWalls()

    def move(self):
        new_trajectory = self.current_trajectory
        if self._avoid_clashing_into_wall():
            pass
        if self.movement_type == TURNING:
            if not self.turner.is_turn_finished():
                new_trajectory = self.turner.get_next_trajectory(self.current_trajectory)
            else:
                self.straight_mover.setup_new_move()
                self.movement_type = MOVING_STRAIGHT
                new_trajectory = self.straight_mover.get_next_trajectory(self.current_trajectory)
        elif self.movement_type == MOVING_STRAIGHT:
            if self.straight_mover.is_moving_straight_finished():
                new_trajectory = self.straight_mover.get_next_trajectory(self.current_trajectory)
            else:
                self.turner.setup_new_turn()
                self.movement_type = TURNING
                new_trajectory = self.turner.get_next_trajectory(self.current_trajectory)

        self.current_trajectory = normalize_trajectory_degrees(new_trajectory)
        self._move_in_dir(self.current_trajectory)

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
        self.movement_type = TURNING
        self.turner.setup_new_turn(angle_change=angle_change, turn_sharpness=turn_sharpness)

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
