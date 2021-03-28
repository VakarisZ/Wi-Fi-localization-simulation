from dataclasses import dataclass
from typing import List


@dataclass
class ErrorList:
    errors: List[float]
    sn_cnt: int
