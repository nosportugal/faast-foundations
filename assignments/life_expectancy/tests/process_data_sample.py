"""Simple script to generate expected output with subset of the entire life_expectancy data"""
# coding: utf-8

import locale
import os
import typing
import random

import pandas as pd

from life_expectancy.defaults import DEFAULT_OUTPUT_COLUMNS
from life_expectancy.load_data import TSVRepresentationStrategy
import life_expectancy.main
from life_expectancy.region import Region

__author__ = "Joaquim Leitão"
__email__ = "joaquim.leitao@nos.pt"


def _at_least_one_region(rows: typing.List[str], desired_region: Region) -> bool:
    """
    Checks if there is at least one entry for a given region in the extract provided
    :param rows: The extract to be analysed
    :param desired_region: The region of interest
    :return: True if the extract contains at least one entry for the region of interest, or False
             otherwise
    """
    for row in rows:
        if desired_region.value.upper() in row:
            return True
    return False


def generate_data_subset(
    _input_path: str,
    _desired_region: Region,
    _percent_rows_select: float,
    _output_path: str,
) -> None:
    """
    Takes the input data, extracts a subset from it ensuring that it contains at least one entry
    from a desired region, and saves the extract in a specified file. The extract is selected
    randomly until it contains at least one region from the desired region
    :param _input_path: The path to the original input file, containing the entire dataset
    :param _desired_region: The code for the region of interest
    :param _percent_rows_select: Percentage of rows of the original dataset to include in the
                                 extract
    :param _output_path: The path where the extract should be saved
    """
    with open(_input_path, "r", encoding=locale.getpreferredencoding()) as fp:
        rows = fp.readlines()

    first_row = rows[0]
    rows = rows[1:]
    found_desired_region = False
    number_rows_select = int(_percent_rows_select * len(rows))

    while not found_desired_region:
        subset_rows = random.sample(rows, number_rows_select)
        found_desired_region = _at_least_one_region(subset_rows, _desired_region)

    with open(_output_path, "w", encoding=locale.getpreferredencoding()) as fp:
        fp.write(first_row)
        for row in subset_rows:
            fp.write(row)


def _get_fixtures_csv_read(
    _file_path: str, _file_sep: str
) -> typing.Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Takes the path to a csv file and the separator (or separator expression) to use when reading the
    aforementioned csv file, and returns two pandas DataFrames, with the expected outputs of the two
    steps of the data loading component: i) read csv into a pandas DataFrame; ii) if a column
    contains the term 'geo' then it is replaced with 'region'
    :param _file_path: The path to the csv file
    :param _file_sep: The separator (or separator expression) to use when reading the csv file
    :return: Two pandas DataFrames, expected to be obtained in each step of the data loading
             component (as described above)
    """
    df_header = pd.read_csv(_file_path, sep=_file_sep, engine="python")
    new_columns = [col if "geo" not in col else "region" for col in df_header.columns]

    df = pd.read_csv(_file_path, sep=_file_sep, engine="python", skiprows=1)
    df.columns = new_columns

    return df_header, df


def generate_fixtures_csv_read(
    _file_path: str, _file_sep: str, _output_root: str
) -> None:
    """
    Takes the path to a csv file and the separator (or separator expression) to use when reading the
    aforementioned csv file, and returns two pandas DataFrames, with the expected outputs of the two
    steps of the data loading component: i) read csv into a pandas DataFrame; ii) if a column
    contains the term 'geo' then it is replaced with 'region'. Saves the two DataFrames to a local
    specified folder
    :param _file_path: The path to the csv file
    :param _file_sep: The separator (or separator expression) to use when reading the csv file
    :param _output_root: The path to the folder where the pandas DataFrames are going to be saved
    """
    df_no_column_change, df_column_change = _get_fixtures_csv_read(
        _file_path, _file_sep
    )

    _file_name = os.path.basename(_file_path)
    _file_name_no_ext, _ = os.path.splitext(_file_name)

    df_no_column_change.to_csv(
        os.path.join(_output_root, f"{_file_name_no_ext}_first.csv"), index=False
    )
    df_column_change.to_csv(
        os.path.join(_output_root, f"{_file_name_no_ext}_second.csv"), index=False
    )


if __name__ == "__main__":
    generate_data_subset(
        _input_path="../data/eu_life_expectancy_raw.tsv",
        _desired_region=Region.PT,
        _percent_rows_select=0.3,
        _output_path="fixtures/eu_life_expectancy_raw_subset.tsv",
    )

    life_expectancy.main.main(
        _input_path="fixtures/eu_life_expectancy_raw_subset.tsv",
        _country=Region.PT,
        _representation_strategy=TSVRepresentationStrategy(),
        _region_col_name="region",
        _output_path="fixtures/eu_life_expectancy_expected_subset.csv",
        _output_columns=DEFAULT_OUTPUT_COLUMNS,
    )

    # Generate fixture to represent output of the first pandas.read_csv call for the entire EU data:
    generate_fixtures_csv_read(
        _file_path="fixtures/eu_life_expectancy_raw_subset.tsv",
        _file_sep="[\t,]",
        _output_root="fixtures/",
    )
