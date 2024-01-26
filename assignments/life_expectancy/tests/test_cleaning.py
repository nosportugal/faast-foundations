"""Tests for the cleaning module"""


import pandas as pd

from life_expectancy.cleaning import clean_data
from life_expectancy.region import Region

__author__ = "Joaquim Leitão"
__email__ = "joaquim.leitao@nos.pt"


def test_clean_data(
    eu_life_expectancy_raw: pd.DataFrame, eu_life_expectancy_expected: pd.DataFrame
) -> None:
    """
    Run the `clean_data` function and compare the output to the expected output
    :param eu_life_expectancy_raw: Pandas DataFrame with the input to the `clean_data` function
    :param eu_life_expectancy_expected: Pandas DataFrame with the expected output of the
                                        `clean_data` function
    """
    eu_life_expectancy_obtained = clean_data(
        df=eu_life_expectancy_raw, country_filter=Region.PT
    )
    pd.testing.assert_frame_equal(
        eu_life_expectancy_obtained, eu_life_expectancy_expected
    )
