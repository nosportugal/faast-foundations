"""Life expectancy package's main module, i.e., execution entry point."""
# coding: utf-8


import argparse
import typing

import pandas as pd

from life_expectancy.defaults import (
    COUNTRY_ARG_STR,
    DEFAULT_REGION_COL_NAME,
    DEFAULT_OUTPUT_COLUMNS,
    INPUT_FILE_PATH_ARG_STR,
    OUTPUT_FILE_PATH_ARG_STR,
    OUTPUT_COLUMNS_ARG_STR,
    REPRESENTATION_STRATEGY_ARG_STR,
    REGION_COL_NAME_ARG_STR,
)
from life_expectancy.cleaning import clean_data
from life_expectancy.load_data import (
    convert_representation_strategy,
    DataRepresentationStrategy,
)
from life_expectancy.region import Region
from life_expectancy.save_data import save_data

__author__ = "Joaquim Leitão"
__email__ = "joaquim.leitao@nos.pt"


def _get_val_for_key(
    args_dict: typing.Dict[str, str], arg_key: str
) -> typing.Optional[typing.Union[str, typing.List[str]]]:
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
    _representation_strategy: typing.Optional[DataRepresentationStrategy],
    _region_col_name: typing.Optional[str],
    _output_path: typing.Optional[str],
    _output_columns: typing.Optional[typing.List[str]],
) -> pd.DataFrame:
    """
    Module's main executing function. Reads the data from the path specified in "input_path"
    to a pandas DataFrame, cleans it (reshapes DataFrame, converts columns to appropriate
    types, removes rows with empty values and retains only records of the country specified in
    "_country"), and saves to a specified local path
    :param _input_path: The local path to the file
    :param _country: The country based on which the DataFrame is going to be filtered
    :param _representation_strategy: The strategy used to load and represent the data in the
                                     provided path
    :param _region_col_name: The desired name for the region/country column of the data
    :param _output_path: The local path where the cleaned DataFrame is going to be saved
    :param _output_columns: The columns to include in the cleaned DataFrame
    :return: The cleaned DataFrame, after the application of the above described operations
    """
    empty_args = []
    if _input_path is None:
        empty_args.append("input_path")
    if _country is None:
        empty_args.append("country")
    if _representation_strategy is None:
        empty_args.append("representation_strategy")
    if _output_path is None:
        empty_args.append("output_path")
    if len(empty_args) > 0:
        raise TypeError(
            f"Not enough arguments specified. Missing arguments: {empty_args}"
        )

    if _region_col_name is None:
        _region_col_name = DEFAULT_REGION_COL_NAME
    if _output_columns is None:
        _output_columns = DEFAULT_OUTPUT_COLUMNS

    df = _representation_strategy.load_data(
        _input_path, _region_col_name, _output_columns
    )
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
    parser.add_argument(
        "-rs",
        "--representation_strategy",
        dest=REPRESENTATION_STRATEGY_ARG_STR,
        help="Representation strategy to be used: (i) 'tsv'/'TSV'/'csv'/'CSV for TSV/CSV file; "
        "(ii) 'json'/'JSON' for JSON file",
    )
    parser.add_argument(
        "-rn",
        "--region_column_name",
        dest=REGION_COL_NAME_ARG_STR,
        help="Desired name for the region/country column",
    )
    parser.add_argument(
        "-oc",
        "--output_columns",
        dest=OUTPUT_COLUMNS_ARG_STR,
        type=lambda arg: arg.split(","),
        help="Desired columns in the saved DataFrame",
    )
    args = vars(parser.parse_args())

    input_path = _get_val_for_key(args, INPUT_FILE_PATH_ARG_STR)
    country_str = _get_val_for_key(args, COUNTRY_ARG_STR)
    output_path = _get_val_for_key(args, OUTPUT_FILE_PATH_ARG_STR)
    representation_strategy_str = _get_val_for_key(
        args, REPRESENTATION_STRATEGY_ARG_STR
    )
    region_col_name = _get_val_for_key(args, REGION_COL_NAME_ARG_STR)
    output_columns = _get_val_for_key(args, OUTPUT_COLUMNS_ARG_STR)

    # Convert country to Region type
    if not isinstance(country_str, str):
        COUNTRY = None
    else:
        COUNTRY = _convert_country_type(country_str)
    if COUNTRY is None:
        raise ValueError(f"Unsupported country: <{country_str}>")

    # Convert representation strategy to the appropriate class
    if not isinstance(representation_strategy_str, str):
        REPRESENTATION_STRATEGY = None
    else:
        REPRESENTATION_STRATEGY = convert_representation_strategy(
            representation_strategy_str
        )
    if REPRESENTATION_STRATEGY is None:
        raise ValueError(
            "Unsupported representation strategy: <representation_strategy_str>"
        )

    if (
        (not isinstance(input_path, str))
        or (not isinstance(region_col_name, str))
        or (not isinstance(output_path, str))
        or (not isinstance(output_columns, list))
    ):
        raise ValueError("Invalid parameters provided to the main function!")

    main(
        input_path,
        COUNTRY,
        REPRESENTATION_STRATEGY,
        region_col_name,
        output_path,
        output_columns,
    )
