from typing import List, Tuple

from config import ModelConfig
from global_error_handler.error_list import ErrorList
from global_error_handler.global_error_aggregate import GlobalErrorAggregate
from global_error_handler.sn_method_error_container import SnMethodErrorContainer


def group_errors_to_method_and_iteration(error_lists: List[ErrorList],
                                         average_error: float) -> Tuple[SnMethodErrorContainer,
                                                                        SnMethodErrorContainer,
                                                                        SnMethodErrorContainer]:
    three_sn_aggregates = [None] * ModelConfig.iteration_count
    two_sn_aggregates = [None] * ModelConfig.iteration_count
    one_sn_aggregates = [None] * ModelConfig.iteration_count

    three_sn_errors = []
    two_sn_errors = []
    one_sn_errors = []

    for error_list in error_lists:
        if error_list.sn_cnt == 3:
            three_sn_errors.extend(error_list.errors)
            target_list = three_sn_aggregates
        elif error_list.sn_cnt == 2:
            two_sn_errors.extend(error_list.errors)
            target_list = two_sn_aggregates
        else:
            one_sn_errors.extend(error_list.errors)
            target_list = one_sn_aggregates

        for i in range(len(error_list.errors)):
            if not target_list[i]:
                target_list[i] = GlobalErrorAggregate(error_list.sn_cnt, i, [error_list.errors[i]])
            else:
                target_list[i].errors.append(error_list.errors[i])

    three_sn_aggregates = trim_error_list(three_sn_aggregates)
    two_sn_aggregates = trim_error_list(two_sn_aggregates)
    one_sn_aggregates = trim_error_list(one_sn_aggregates)

    three_sn_average = sum(three_sn_errors) / len(three_sn_errors)
    three_sn_container = SnMethodErrorContainer(avg_pred_error=average_error,
                                                avg_sn_method_error=three_sn_average,
                                                errors_on_iteration=three_sn_aggregates)

    two_sn_average = sum(two_sn_errors) / len(two_sn_errors)
    two_sn_container = SnMethodErrorContainer(avg_pred_error=average_error,
                                              avg_sn_method_error=two_sn_average,
                                              errors_on_iteration=two_sn_aggregates)

    one_sn_average = sum(one_sn_errors) / len(one_sn_errors)
    one_sn_container = SnMethodErrorContainer(avg_pred_error=average_error,
                                              avg_sn_method_error=one_sn_average,
                                              errors_on_iteration=one_sn_aggregates)

    return three_sn_container, two_sn_container, one_sn_container


def trim_error_list(error_list: List[GlobalErrorAggregate]) -> List[GlobalErrorAggregate]:
    return [error for error in error_list if error]
