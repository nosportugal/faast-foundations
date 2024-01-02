"""Tests for the load_data module"""


from unittest.mock import patch

from life_expectancy.defaults import DEFAULT_FILE_SEP
from life_expectancy.load_data import load_data
from . import OUTPUT_DIR


def test_load_data() -> None:
    """Test the 'load_data' module/function with a mock function"""
    with patch("pandas.read_csv") as read_csv_mock:
        read_csv_mock.side_effect = print("\nIn load_data!")
        load_data(OUTPUT_DIR / "eu_life_expectancy_raw.tsv", DEFAULT_FILE_SEP)
        assert read_csv_mock.call_count == 2
