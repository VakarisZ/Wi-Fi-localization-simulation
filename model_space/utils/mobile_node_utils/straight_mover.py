from model_space.utils.mobile_node_utils.random_param_fetcher import get_random_straight_move_iterations


class StraightMover:
    def __init__(self):
        # How many iterations to move straight
        self.iterations_remaining = 0

    def setup_new_move(self):
        self.iterations_remaining = get_random_straight_move_iterations()

    def get_next_trajectory(self, trajectory) -> float:
        self.iterations_remaining -= 1
        return trajectory

    def is_moving_straight_finished(self) -> bool:
        return bool(self.iterations_remaining)
