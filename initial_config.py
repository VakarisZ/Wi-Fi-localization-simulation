from dataclasses import dataclass

from model_space.utils.mobile_node import MobileNode
from model_space.utils.point import Point
from model_space.utils.stationary_node import StationaryNode


@dataclass
class ModelConfig:
    area = {'xmin': -100, 'xmax': 100, 'ymin': -100, 'ymax': 100}
    mobile_node = MobileNode(Point(x=0, y=0))
    stationary_nodes = [StationaryNode(Point(-90, 50), 110),
                        StationaryNode(Point(0, -70), 110),
                        StationaryNode(Point(90, 75), 110)]
