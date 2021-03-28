from typing import List, Tuple

from config import ModelConfig
from global_error_handler.error_list import ErrorList
from global_error_handler.global_error_aggregate import GlobalErrorAggregate


def group_errors_to_method_and_iteration(error_lists: List[ErrorList]) -> Tuple[List[GlobalErrorAggregate],
                                                                                List[GlobalErrorAggregate],
                                                                                List[GlobalErrorAggregate]]:
    three_sn_errors = [None] * ModelConfig.iteration_count
    two_sn_errors = [None] * ModelConfig.iteration_count
    one_sn_errors = [None] * ModelConfig.iteration_count

    for error_list in error_lists:
        if error_list.sn_cnt == 3:
            target_list = three_sn_errors
        elif error_list.sn_cnt == 2:
            target_list = two_sn_errors
        else:
            target_list = one_sn_errors

        for i in range(len(error_list.errors)):
            if not target_list[i]:
                target_list[i] = GlobalErrorAggregate(error_list.sn_cnt, i, [error_list.errors[i]])
            else:
                target_list[i].errors.append(error_list.errors[i])

    return three_sn_errors, two_sn_errors, one_sn_errors
