"""Module with data cleaning functions."""
# coding: utf-8

import argparse
import os
import re

import pandas as pd


"""
Module for data cleaning operations
"""

__author__ = "Joaquim Leitão"
__email__ = "joaquim.leitao@nos.pt"


_COUNTRY_ARG_STR = "country"


def clean_data(country_filter: str = None):
    """
    Read tsv file located in "life_expectancy/data/eu_life_expectancy_raw.tsv" and filters
    contents based on country
    :param country_filter: The country based on which the contents of the tsv file are going
                           to be filtered 
    """
    file_path = "life_expectancy/data/eu_life_expectancy_raw.tsv"
    table_key_vars = ["unit", "sex", "age", "region"]

    if country_filter is None:
        country_filter = "PT"

    # Column separators: ",", "\t", "\\" or ":" . Each can be preceded or succedded by optional
    # spaces
    # df = pd.read_table(file_path, engine="python", sep="[\t,:]+|")
    df_header = pd.read_csv(file_path, sep="[\t,]", na_values=[":"], engine="python")
    new_columns = [col if "geo" not in col else "region" for col in df_header.columns]

    df = pd.read_csv(file_path, sep="[\t,]", engine="python", skiprows=1)
    df.columns = new_columns

    # Deal with NaN values
    df = df.replace(re.compile(r"\s*:\s*"), "")

    # Unpivot table, making sure we have the columns "unit", "sex", "age", "region", "year" and
    # "value"
    df_unpivot = pd.melt(
        df,
        id_vars=table_key_vars,
        value_vars=[col for col in df.columns if col not in table_key_vars]
    )
    # Deal with NaN values - Not digit
    df_unpivot["value"] = df_unpivot["value"].str.replace(r"[^\d\.]", "")

    df_unpivot = df_unpivot.rename(columns={"variable": "year"})
    df_unpivot["year"] = pd.to_numeric(df_unpivot["year"], errors="coerce")
    df_unpivot["value"] = pd.to_numeric(df_unpivot["value"], errors="coerce")
    df_unpivot = df_unpivot.dropna(subset=["value"])

    # Filter region
    df_unpivot_pt = df_unpivot.loc[df_unpivot["region"] == country_filter]

    file_path_root = os.path.dirname(file_path)
    df_unpivot_pt.to_csv(
        os.path.join(file_path_root, f"{country_filter.lower()}_life_expectancy.csv"),
        index=False
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--country", dest=_COUNTRY_ARG_STR, help="Filter country")
    args = vars(parser.parse_args())

    try:
        COUNTRY = args[_COUNTRY_ARG_STR]
    except KeyError:
        COUNTRY = None

    clean_data(COUNTRY)
    
