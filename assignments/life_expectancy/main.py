"""Life expectancy package's main module, i.e., execution entry point."""
# coding: utf-8


import argparse
import typing

import pandas as pd

from life_expectancy.defaults import (
    COUNTRY_ARG_STR,
    INPUT_FILE_PATH_ARG_STR,
    OUTPUT_FILE_PATH_ARG_STR,
)
from life_expectancy.cleaning import clean_data
from life_expectancy.load_data import load_data
from life_expectancy.region import Region
from life_expectancy.save_data import save_data

__author__ = "Joaquim Leitão"
__email__ = "joaquim.leitao@nos.pt"


def _get_val_for_key(
    args_dict: typing.Dict[str, str], arg_key: str
) -> typing.Optional[str]:
    """
    Retrieves the value of a given key in a dictionary/hash table. If the key is not available, then
    a null/None value is returned
    :param args_dict: The dictionary/hash table
    :param arg_key: The key for which the corresponding value is intended to be retrieved
    :return: The value of the desired key, if it exists in the dictionary/hash table; otherwsie
             returns null/None
    """
    try:
        arg_val = args_dict[arg_key]
    except KeyError:
        arg_val = None
    return arg_val


def _convert_country_type(country_val: typing.Optional[str]) -> typing.Optional[Region]:
    """
    Checks if a given country, represented as a string, is contained within the list of supported
    countries, i.e. life_expectancy.region.Region. If affirmative, then returns the appropriate
    instance of the Enum class, otherwise returns None
    :param country_val: The string representation of the country of interest
    :return: The appropriate instance of the life_expectancy.region.Region if the country is
             supported, otherwise None
    """
    if (country_val is not None) and (Region.has_member_key(country_val)):
        return Region(country_val.upper())
    return None


def main(
    _input_path: typing.Optional[str],
    _country: typing.Optional[Region],
    _output_path: typing.Optional[str],
) -> pd.DataFrame:
    """
    Module's main executing function. Reads the data from the path specified in "input_path"~
    to a pandas DataFrame, cleans it (reshapes DataFrame, converts columns to appropriate
    types, removes rows with empty values and retains only records of the country specified in
    "_country"), and saves to a specified local path
    :param _input_path: The local path to the file
    :param _country: The country based on which the DataFrame is going to be filtered
    :param _output_path: The local path where the cleaned DataFrame is going to be saved
    :return: The cleaned DataFrame, after the application of the above described operations
    """
    empty_args = []
    if _input_path is None:
        empty_args.append("input_path")
    if _country is None:
        empty_args.append("country")
    if _output_path is None:
        empty_args.append("output_path")
    if len(empty_args) > 0:
        raise TypeError(
            f"Not enough arguments specified. Missing arguments: {empty_args}"
        )

    df = load_data(_input_path)
    df = clean_data(df, _country)
    save_data(df, _output_path)

    return df


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--country", dest=COUNTRY_ARG_STR, help="Filter country")
    parser.add_argument(
        "-ip",
        "--input_path",
        dest=INPUT_FILE_PATH_ARG_STR,
        help="Local path to life expectancy input data file",
    )
    parser.add_argument(
        "-sp",
        "--output_path",
        dest=OUTPUT_FILE_PATH_ARG_STR,
        help="Local path where cleaned life expectancy file is saved",
    )
    args = vars(parser.parse_args())

    input_path = _get_val_for_key(args, INPUT_FILE_PATH_ARG_STR)
    country_str = _get_val_for_key(args, COUNTRY_ARG_STR)
    output_path = _get_val_for_key(args, OUTPUT_FILE_PATH_ARG_STR)

    # Convert country to Region type
    country = _convert_country_type(country_str)

    if country is None:
        raise ValueError(f"Unsupported country: <{country_str}>")

    main(input_path, country, output_path)
