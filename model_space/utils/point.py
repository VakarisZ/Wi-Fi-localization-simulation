from dataclasses import dataclass


@dataclass
class Point:
    x: float
    y: float

    def as_list(self):
        return [self.x, self.y]
