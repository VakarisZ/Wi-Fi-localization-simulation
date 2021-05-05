from typing import List

from config import ModelConfig
from global_error_handler.error_list import ErrorList
from prediction_errors.pred_results import PredictionResults


class GlobalErrorContainer:
    def __init__(self):
        self.iteration_cnt = 0
        self.error_lists: List[ErrorList] = []

    def add_error_list(self, error_list: List[PredictionResults]):
        error_list = GlobalErrorContainer.split_errors_according_to_sn_cnt(error_list)
        self.error_lists.extend(error_list)

    @staticmethod
    def split_errors_according_to_sn_cnt(error_list: List[PredictionResults]) -> List[ErrorList]:
        split_errors = []
        while error_list:
            sn_cnt = error_list[0].sn_count
            sublist = GlobalErrorContainer.pop_error_list_according_to_sn(error_list, sn_cnt)
            if ModelConfig.calculate_zone_errors_once and \
                not GlobalErrorContainer.is_error_count_in_list(split_errors, sn_cnt):
                split_errors.append(ErrorList(sublist, sn_cnt))
            elif not ModelConfig.calculate_zone_errors_once:
                split_errors.append(ErrorList(sublist, sn_cnt))
        return split_errors

    @staticmethod
    def is_error_count_in_list(error_list: List, sn_count: int) -> bool:
        return bool([error for error in error_list if error.sn_cnt == sn_count])

    @staticmethod
    def pop_error_list_according_to_sn(error_list: List[PredictionResults], sn_cnt: int) -> List[float]:
        split = []
        for error in error_list:
            if error.sn_count == sn_cnt:
                split.append(error.error)
            if len(split) == len(error_list) or not error.sn_count == sn_cnt:
                del error_list[0:len(split)]
                return split
        return None
