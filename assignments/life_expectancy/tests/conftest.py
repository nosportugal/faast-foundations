"""Pytest configuration file"""
import pandas as pd
import pytest

from . import FIXTURES_DIR


@pytest.fixture(scope="session")
def pt_life_expectancy_expected() -> pd.DataFrame:
    """
    Fixture to load the expected output of the cleaning script, when the EU data is provided and
    filtered for the PT region
    """
    return pd.read_csv(FIXTURES_DIR / "pt_life_expectancy_expected.csv")


@pytest.fixture(scope="session", name="pt_life_expectancy_raw_first")
def pt_life_expectancy_raw_first_setup() -> pd.DataFrame:
    """
    Fixture to load the expected output of the first call to the pandas.read_csv in the cleaning
    script, when the EU data is provided and filtered for the PT region
    """
    return pd.read_csv(
        "assignments/life_expectancy/data/eu_life_expectancy_raw.tsv",
        sep="[\t,]",
        engine="python",
    )


@pytest.fixture(scope="session")
def pt_life_expectancy_raw(pt_life_expectancy_raw_first: pd.DataFrame) -> pd.DataFrame:
    """
    Fixture to load the expected output of the data loading part of the cleaning script, when the EU
    data is provided and filtered for the PT region
    """
    new_columns = [
        col if "geo" not in col else "region"
        for col in pt_life_expectancy_raw_first.columns
    ]

    df = pd.read_csv(
        "assignments/life_expectancy/data/eu_life_expectancy_raw.tsv",
        sep="[\t,]",
        engine="python",
        skiprows=1,
    )
    df.columns = new_columns
    return df


@pytest.fixture(scope="session")
def eu_life_expectancy_raw_first() -> pd.DataFrame:
    """
    Fixture to load a subset of the raw EU input to the cleaning script, with no column name
    manipulation
    """
    file_path = FIXTURES_DIR / "eu_life_expectancy_raw_subset_first.csv"
    return pd.read_csv(file_path, sep=",", engine="python")


@pytest.fixture(scope="session")
def eu_life_expectancy_raw() -> pd.DataFrame:
    """
    Fixture to load the raw EU input to the cleaning script, replacing 'geo' in column with 'region'
    """
    file_path = FIXTURES_DIR / "eu_life_expectancy_raw_subset_second.csv"
    return pd.read_csv(file_path, sep=",", engine="python")


@pytest.fixture(scope="session")
def eu_life_expectancy_expected() -> pd.DataFrame:
    """Fixture to load the expected EU output of the cleaning script"""
    return pd.read_csv(FIXTURES_DIR / "eu_life_expectancy_expected_subset.csv")
