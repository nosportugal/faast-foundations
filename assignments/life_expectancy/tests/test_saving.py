"""Tests for the save_data module"""


from unittest.mock import patch

import pandas as pd

from life_expectancy.save_data import save_data
from . import OUTPUT_DIR


def test_save_data(eu_life_expectancy_expected: pd.DataFrame) -> None:
    """Test the 'save_data' module/function with a mock function"""
    with patch("pandas.DataFrame.to_csv") as to_csv_mock:
        to_csv_mock.side_effect = print("\nIn save_data!")
        save_data(
            eu_life_expectancy_expected, OUTPUT_DIR / "pt_life_expectancy_obtained.csv"
        )
        to_csv_mock.assert_called_once()
