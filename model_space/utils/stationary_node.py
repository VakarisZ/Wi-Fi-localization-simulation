from model_space.utils.node import Node
from model_space.utils.point import Point


class StationaryNode(Node):
    def __init__(self, coords: Point, range):
        super().__init__(coords=coords,
                         style={'color': 'blue', 'marker': 'o', 'markersize': 5})
        self.range = range
