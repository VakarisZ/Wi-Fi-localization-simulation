from dataclasses import dataclass


@dataclass
class GlobalError:
    # Which iteration of error
    iteration: int
    # How many ranges available/algorith
    sn_cnt: int
    # Error
    error: float
