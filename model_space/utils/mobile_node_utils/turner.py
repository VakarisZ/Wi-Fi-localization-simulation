from model_space.utils.mobile_node_utils.random_param_fetcher import get_random_trajectory, get_random_angle_change, \
    get_random_turn_sharpness


class Turner:
    def __init__(self):
        # Where the node is turning towards
        self.angle_change = 0
        # What was the initial angle change. Used to determine if node completed the turn.
        self.initial_angle_change = 0
        # How many degrees a node can turn in one iteration
        self.turn_sharpness = 0

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

    def is_turn_finished(self):
        if self.initial_angle_change > 0 >= self.angle_change:
            return True
        elif self.initial_angle_change < 0 <= self.angle_change:
            return True
        else:
            return False

    def get_next_trajectory(self, trajectory):
        if self.angle_change < 0:
            trajectory -= self.turn_sharpness
            self.angle_change += self.turn_sharpness
        elif self.angle_change > 0:
            trajectory += self.turn_sharpness
            self.angle_change -= self.turn_sharpness
        return trajectory
