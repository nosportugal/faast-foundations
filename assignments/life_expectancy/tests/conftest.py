"""Pytest configuration file"""
import pandas as pd
import pytest

from . import FIXTURES_DIR


@pytest.fixture(scope="session")
def pt_life_expectancy_expected() -> pd.DataFrame:
    """Fixture to load the expected output of the cleaning script"""
    return pd.read_csv(FIXTURES_DIR / "pt_life_expectancy_expected.csv")


@pytest.fixture(scope="session")
def eu_life_expectancy_raw() -> pd.DataFrame:
    """Fixture to load the raw EU input to the cleaning script"""

    file_path = FIXTURES_DIR / "eu_life_expectancy_raw_subset.tsv"
    df_header = pd.read_csv(file_path, sep="[\t,]", engine="python")
    new_columns = [col if "geo" not in col else "region" for col in df_header.columns]

    df = pd.read_csv(file_path, sep="[\t,]", engine="python", skiprows=1)
    df.columns = new_columns

    return df


@pytest.fixture(scope="session")
def eu_life_expectancy_expected() -> pd.DataFrame:
    """Fixture to load the expected EU output of the cleaning script"""
    return pd.read_csv(FIXTURES_DIR / "eu_life_expectancy_expected_subset.csv")
