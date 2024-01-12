"""Module with data cleaning functions."""
# coding: utf-8


import re
import typing

import pandas as pd

from life_expectancy.defaults import TABLE_KEY_VARS
from life_expectancy.region import Region

__author__ = "Joaquim Leitão"
__email__ = "joaquim.leitao@nos.pt"


def _extract_number_from_row(x: str) -> typing.Optional[str]:
    """
    Extracts an integer or floating point number from one the string representation of one element
    (column in a given row) of a pandas DataFrame
    :param x: The element in the pandas DataFrame
    :return: The integer or floating point number contained in the element, or None othewise
    """
    re_pattern_result = re.search(r"(\d+(\.\d+)?)", x)
    if re_pattern_result is None:
        return None
    return re_pattern_result.group()


def clean_data(df: pd.DataFrame, country_filter: Region) -> pd.DataFrame:
    """
    Performs a variety of operations to the provided pandas DataFrame, in order to clean it for
    further processing:
       - Reshapes the DataFrame to have one row per year (instead of multiple years in the same row)
       - Converts the year and life expectancy value columns to appropriate types (int and float,
         respectively)
       - Removes life expectancy values in a given year that are not defined
       - Filters the DataFrame to only contain rows of a given region, which is given by the
         "country_filter" argument
       - Reset the DataFrame's index
    :param df: The DataFrame to be cleaned
    :param country_filter: The country based on which the DataFrame is going to be filtered
                           (instance of life_expectancy.region.Region)
    :return: The cleaned DataFrame, after the application of the above described operations
    """
    # Deal with NaN values: Mark columns with invalid value (Just ":" and varying number of spaces)
    df = df.replace(re.compile(r"\s*:\s*"), "")

    # Unpivot table, making sure we have the columns specified in _TABLE_KEY_VARS
    df_unpivot = pd.melt(
        df,
        id_vars=TABLE_KEY_VARS,
        value_vars=[col for col in df.columns if col not in TABLE_KEY_VARS],
    )

    # Deal with NaN values - Keep in the string of each column only characters that are digits
    df_unpivot["value"] = df_unpivot["value"].str.strip()
    df_unpivot["value"] = df_unpivot["value"].apply(_extract_number_from_row)

    df_unpivot = df_unpivot.rename(columns={"variable": "year"})
    df_unpivot["year"] = df_unpivot["year"].astype(int)
    df_unpivot["value"] = pd.to_numeric(df_unpivot["value"], errors="coerce")

    df_unpivot = df_unpivot.dropna(subset=["value"])

    # Filter region
    df_unpivot = df_unpivot.loc[
        df_unpivot["region"].str.lower() == country_filter.value.lower()
    ]

    df_unpivot = df_unpivot.reset_index(drop=True)

    return df_unpivot
