"""Tests for the load_data module"""


import os
from unittest.mock import patch

import pandas as pd

from life_expectancy.load_data import (
    JSONRepresentationStrategy,
    TSVRepresentationStrategy,
)
from . import OUTPUT_DIR

__author__ = "Joaquim Leitão"
__email__ = "joaquim.leitao@nos.pt"


def test_load_data_json(eu_life_expectancy_raw_json: pd.DataFrame) -> None:
    """
    Test the life_expectancy.load_data.JSONRepresentationStrategy class with a mock function
    :param eu_life_expectancy_raw_json: The expected output of the
                                   life_expectancy.load_data.JSONRepresentationStrategy.load_data
                                   method
    """
    with patch("pandas.read_json") as read_json_mock:
        read_json_mock.side_effect = [eu_life_expectancy_raw_json]
        JSONRepresentationStrategy().load_data(
            os.path.join(OUTPUT_DIR, "eurostat_life_expect.json"),
            "region",
        )
        read_json_mock.assert_called_once()


def test_load_data_csv(
    eu_life_expectancy_raw_first: pd.DataFrame, eu_life_expectancy_raw: pd.DataFrame
) -> None:
    """
    Test the life_expectancy.load_data.TSVRepresentationStrategy class with a mock function
    :param eu_life_expectancy_raw_first: The expected output of the first call to pandas.read_csv in
                                         the load_data method of the
                                         life_expectancy.load_data.TSVRepresentationStrategy class
    :param eu_life_expectancy_raw: The expected output of the load_data method of the
                                   life_expectancy.load_data.TSVRepresentationStrategy class
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
        TSVRepresentationStrategy().load_data(
            os.path.join(OUTPUT_DIR, "eu_life_expectancy_raw.tsv"),
            "region",
        )
        assert read_csv_mock.call_count == 2
