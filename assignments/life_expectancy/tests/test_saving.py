"""Tests for the save_data module"""


import os
from unittest.mock import patch

import pandas as pd

from life_expectancy.save_data import save_data
from . import OUTPUT_DIR

__author__ = "Joaquim Leitão"
__email__ = "joaquim.leitao@nos.pt"


def test_save_data(eu_life_expectancy_expected: pd.DataFrame) -> None:
    """
    Test the 'save_data' module/function with a mock function
    :param eu_life_expectancy_expected: Pandas DataFrame to be saved
    """
    with patch("pandas.DataFrame.to_csv") as to_csv_mock:
        to_csv_mock.side_effect = print("\nIn save_data!")
        save_data(
            eu_life_expectancy_expected,
            os.path.join(OUTPUT_DIR, "pt_life_expectancy_obtained.csv"),
        )
        to_csv_mock.assert_called_once()
