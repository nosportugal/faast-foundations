"""Tests for the load_data module"""


import os
from unittest.mock import patch

import pandas as pd

from life_expectancy.defaults import DEFAULT_FILE_SEP
from life_expectancy.load_data import load_data
from . import OUTPUT_DIR

__author__ = "Joaquim Leitão"
__email__ = "joaquim.leitao@nos.pt"


def test_load_data(
    eu_life_expectancy_raw_first: pd.DataFrame, eu_life_expectancy_raw: pd.DataFrame
) -> None:
    """
    Test the `load_data` module/function with a mock function
    :param eu_life_expectancy_raw_first: The expected output of the first call to pandas.read_csv in
                                         the `load_data` function
    :param eu_life_expectancy_raw: The expected output of the `load_data` function
    """

    def _read_csv_first_call() -> pd.DataFrame:
        """
        Prints message in load data and returns first fixture
        :return: The first fixture, i.e., the expected output for the first call to pandas.read_csv
                 (subset of the raw EU input with no column name manipulation)
        """
        print("\nIn load_data!")
        return eu_life_expectancy_raw_first

    with patch("pandas.read_csv") as read_csv_mock:
        read_csv_mock.side_effect = [_read_csv_first_call(), eu_life_expectancy_raw]
        load_data(
            os.path.join(OUTPUT_DIR, "eu_life_expectancy_raw.tsv"), DEFAULT_FILE_SEP
        )
        assert read_csv_mock.call_count == 2
