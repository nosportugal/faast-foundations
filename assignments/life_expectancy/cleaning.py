"""Module with data cleaning functions."""
# coding: utf-8

import argparse
import re
import typing

import pandas as pd


__author__ = "Joaquim Leitão"
__email__ = "joaquim.leitao@nos.pt"


_COUNTRY_ARG_STR = "country"
_INPUT_FILE_PATH_ARG_STR = "input_path"
_OUTPUT_FILE_PATH_ARG_STR = "output_path"
_TABLE_KEY_VARS = ["unit", "sex", "age", "region"]
_DEFAULT_FILE_SEP = "[\t,]"


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


def load_data(file_path: str, file_sep: typing.Optional[str] = None) -> pd.DataFrame:
    """
    Reads the contents of the file in the provided path to a pandas DataFrame
    If the file contains a column with "geo", then it is renamed to "region"
    :param file_path: The local path to the file
    :param file_sep: Optional parameter. Character or regex pattern to treat as the delimiter
    :return: A pandas DataFrame with the file contents
    """
    if file_sep is None:
        file_sep = _DEFAULT_FILE_SEP

    # Column separators can be preceded or succedded by optional spaces
    df_header = pd.read_csv(file_path, sep=file_sep, engine="python")
    new_columns = [col if "geo" not in col else "region" for col in df_header.columns]

    df = pd.read_csv(file_path, sep=file_sep, engine="python", skiprows=1)
    df.columns = new_columns

    return df


def clean_data(df: pd.DataFrame, country_filter: str) -> pd.DataFrame:
    """
    Performs a variety of operations to the provided pandas DataFrame, in order to clean it for
    further processing:
       - Reshapes the DataFrame to have one row per year (instead of multiple years in the same row)
       - Converts the year and life expectancy value columns to appropriate types (int and float,
         respectively)
       - Removes life expectancy values in a given year that are not defined
       - Filters the DataFrame to only contain rows of a given region, which is given by the
         "country_filter" argument
    :param df: The DataFrame to be cleaned
    :param country_filter: The country based on which the DataFrame is going to be filtered
    :return: The cleaned DataFrame, after the application of the above described operations
    """
    # Deal with NaN values: Mark columns with invalid value (Just ":" and varying number of spaces)
    df = df.replace(re.compile(r"\s*:\s*"), "")

    # Unpivot table, making sure we have the columns specified in _TABLE_KEY_VARS
    df_unpivot = pd.melt(
        df,
        id_vars=_TABLE_KEY_VARS,
        value_vars=[col for col in df.columns if col not in _TABLE_KEY_VARS],
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
        df_unpivot["region"].str.lower() == country_filter.lower()
    ]
    return df_unpivot


def save_data(df: pd.DataFrame, save_file_path: str):
    """
    Saves the contents of the provided DataFrame in a specified local path
    :param df: The DataFrame to be saved
    :param save_file_path: The local path where the DataFrame is going to be saved
    """
    df.to_csv(save_file_path, index=False)


def main(
    _input_path: typing.Optional[str],
    _country: typing.Optional[str],
    _output_path: typing.Optional[str],
):
    """
    Module's main executing function. Reads the data from the path specified in "input_path" to a
    pandas DataFrame, cleans it (reshapes DataFrame, converts columns to appropriate types, removes
    rows with empty values and retains only records of the country specified in "_country"),
    and saves to a specified local path
    :param _input_path: The local path to the file
    :param _country: The country based on which the DataFrame is going to be filtered
    :param _output_path: The local path where the cleaned DataFrame is going to be saved
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--country", dest=_COUNTRY_ARG_STR, help="Filter country")
    parser.add_argument(
        "-ip",
        "--input_path",
        dest=_INPUT_FILE_PATH_ARG_STR,
        help="Local path to life expectancy input data file",
    )
    parser.add_argument(
        "-sp",
        "--output_path",
        dest=_OUTPUT_FILE_PATH_ARG_STR,
        help="Local path where cleaned life expectancy file is saved",
    )
    args = vars(parser.parse_args())

    input_path = _get_val_for_key(args, _INPUT_FILE_PATH_ARG_STR)
    country = _get_val_for_key(args, _COUNTRY_ARG_STR)
    output_path = _get_val_for_key(args, _OUTPUT_FILE_PATH_ARG_STR)

    main(input_path, country, output_path)
