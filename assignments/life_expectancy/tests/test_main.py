"""Tests for the entire cleaning module"""
from unittest.mock import patch

import pandas as pd

from life_expectancy.cleaning import main
from . import OUTPUT_DIR


def test_main(
    pt_life_expectancy_raw_first: pd.DataFrame,
    pt_life_expectancy_raw: pd.DataFrame,
    pt_life_expectancy_expected: pd.DataFrame,
) -> None:
    """
    Run the `clean_data` function and compare the output to the expected output
    :param pt_life_expectancy_raw_first: Expected output of the first call to pandas.read_csv in the
                                         `clean_data` function
    :param pt_life_expectancy_raw: Expected output of the data loading part
    :param pt_life_expectancy_expected: Expected output of the `clean_data` function
    """
    pt_life_expectancy_actual = pd.read_csv(OUTPUT_DIR / "pt_life_expectancy.csv")

    with patch("pandas.DataFrame.to_csv") as to_csv_mock:
        to_csv_mock.side_effect = print("\nIn save_data!")
        with patch("pandas.read_csv") as read_csv_mock:
            read_csv_mock.side_effect = [
                pt_life_expectancy_raw_first,
                pt_life_expectancy_raw,
            ]

            pt_life_expectancy_obtained = main(
                _input_path="assignments/life_expectancy/data/eu_life_expectancy_raw.tsv",
                _country="PT",
                _output_path="assignments/life_expectancy/data/pt_life_expectancy.csv",
            )

            pd.testing.assert_frame_equal(
                pt_life_expectancy_actual, pt_life_expectancy_expected
            )

            pd.testing.assert_frame_equal(
                pt_life_expectancy_obtained, pt_life_expectancy_expected
            )

            assert to_csv_mock.call_count == 1
            to_csv_mock.assert_called_once()

            assert read_csv_mock.call_count == 2
