import random
from random import randrange

from config import ModelConfig


random.seed(ModelConfig.seed)


def get_random_angle_change():
    angle_range = ModelConfig.angle_change_range
    return randrange(angle_range[0], angle_range[1])


def get_random_turn_sharpness():
    turn_sharpness_range = ModelConfig.turn_sharpness_range
    return randrange(turn_sharpness_range[0], turn_sharpness_range[1])


def get_random_avoidance_turn_sharpness():
    avoidance_range = ModelConfig.collision_avoidance_turn_sharpness_range
    return randrange(avoidance_range[0], avoidance_range[1])


def get_random_trajectory():
    return randrange(0, 360)


def get_random_straight_move_iterations():
    return randrange(ModelConfig.straight_move_range[0], ModelConfig.straight_move_range[1])
