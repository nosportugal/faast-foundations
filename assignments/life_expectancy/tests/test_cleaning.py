"""Tests for the cleaning module"""


import pandas as pd

from life_expectancy.cleaning import clean_data


def test_clean_data(
    eu_life_expectancy_raw: pd.DataFrame, eu_life_expectancy_expected: pd.DataFrame
) -> None:
    """Run the `clean_data` function and compare the output to the expected output"""
    eu_life_expectancy_obtained = clean_data(
        df=eu_life_expectancy_raw, country_filter="PT"
    )
    pd.testing.assert_frame_equal(
        eu_life_expectancy_obtained, eu_life_expectancy_expected
    )
