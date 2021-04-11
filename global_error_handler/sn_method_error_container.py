from dataclasses import dataclass
from typing import List

from global_error_handler.global_error_aggregate import GlobalErrorAggregate


@dataclass
class SnMethodErrorContainer:
    avg_pred_error: float
    avg_sn_method_error: float
    errors_on_iteration: List[GlobalErrorAggregate]
