from model_space.utils.point import Point


class Node:
    def __init__(self, coords: Point, style: dict):
        self.coords = coords
        self.style = style
