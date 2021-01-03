from model_space.utils.node import Node
from model_space.utils.point import Point


class MobileNode(Node):

    def __init__(self, coords: Point):
        super().__init__(coords, {'color': 'red', 'marker': 'o', 'markersize': 5})
