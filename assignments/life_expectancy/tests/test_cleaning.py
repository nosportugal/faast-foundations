"""Tests for the cleaning module"""
import pandas as pd

from life_expectancy.cleaning import main
from . import OUTPUT_DIR


def test_clean_data(pt_life_expectancy_expected):
    """Run the `clean_data` function and compare the output to the expected output"""

    main(
        _input_path="assignments/life_expectancy/data/eu_life_expectancy_raw.tsv",
        _country="PT",
        _output_path="assignments/life_expectancy/data/pt_life_expectancy.csv",
    )

    pt_life_expectancy_actual = pd.read_csv(OUTPUT_DIR / "pt_life_expectancy.csv")
    pd.testing.assert_frame_equal(
        pt_life_expectancy_actual, pt_life_expectancy_expected
    )
