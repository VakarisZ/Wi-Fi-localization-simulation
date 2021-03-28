from dataclasses import dataclass
from typing import List


@dataclass
class GlobalErrorAggregate:
    sn_cnt: int
    iteration: int
    errors: List[float]

    def get_avg_error(self) -> float:
        return sum(self.errors) / len(self.errors)
