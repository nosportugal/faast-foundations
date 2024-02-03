"""Module with data collection/input functions."""
# coding: utf-8


import typing

import pandas as pd

from life_expectancy.defaults import DEFAULT_FILE_SEP

__author__ = "Joaquim Leitão"
__email__ = "joaquim.leitao@nos.pt"


class DataRepresentationStrategy(typing.Protocol):
    """
    Generic class/protocol to load and hold the representation for the life expectancy data in a
    given format
    """

    def load_data(
        self,
        file_path: str,
        region_col_name: str,
        desired_columns: typing.Optional[typing.List[str]],
    ) -> pd.DataFrame:
        """
        Generic method to load the data from the specified file path, based on the supported
        representation type
        :param file_path: The local path to the file
        :param region_col_name: The name of the column containing the region/country in the
                                provided data
        :param desired_columns: A list of string objects containing the names of the columns to be
                                loaded from the provided data file
        :return: A pandas DataFrame with the file contents
        """

    def __str__(self) -> str:
        """
        Override default string representation
        :return: Class instance string representation
        """
        return self.__class__.__name__


class JSONRepresentationStrategy:
    """Class to load and hold the representation for the life expectancy data in the JSON format"""

    def load_data(
        self,
        file_path: str,
        region_col_name: str,
        desired_columns: typing.Optional[typing.List[str]],
    ) -> pd.DataFrame:
        """
        Reads the contents of the JSON file in the provided path to a pandas DataFrame
        Makes sure that the column containing the region/country is named after the
        region_col_name> parameter
        :param file_path: The local path to the file
        :param region_col_name: The name of the column containing the region/country in the
                                provided data
        :param desired_columns: A list of string objects containing the names of the columns to be
                                loaded from the provided data file
        :return: A pandas DataFrame with the file contents
        """
        df = pd.read_json(file_path)
        df: pd.DataFrame = typing.cast(pd.DataFrame, df)

        # Change "country" to <region_col_name> and "life_expectancy" to "value"
        new_columns = {}
        # pylint: disable=E1101
        for col in df.columns:
            if ("country" in col) and (
                (desired_columns is None) or (region_col_name in desired_columns)
            ):
                new_columns[col] = region_col_name
            elif ("life_expectancy" in col) and (
                (desired_columns is None) or ("value" in desired_columns)
            ):
                new_columns[col] = "value"
            elif (desired_columns is None) or (col in desired_columns):
                new_columns[col] = col
        # Need to select the keys in "new_columns" and change their names to the
        # values in "new_columns"
        df = df.rename(columns=new_columns)[new_columns.values()]
        return df

    def __str__(self) -> str:
        """
        Override default string representation
        :return: Class instance string representation
        """
        return self.__class__.__name__


class TSVRepresentationStrategy:
    """Class to load and hold the representation for the life expectancy data in the TSV format"""

    def load_data(
        self,
        file_path: str,
        region_col_name: str,
        desired_columns: typing.Optional[typing.List[str]],
    ) -> pd.DataFrame:
        """
        Reads the contents of the TSV file in the provided path to a pandas DataFrame
        If the file contains a column with "geo", then it is renamed to the value provided in the
        <region_col_name> parameter
        :param file_path: The local path to the file
        :param region_col_name: The name of the column containing the region/country in the provided
                                data
        :param desired_columns: A list of string objects containing the names of the columns to be
                                loaded from the provided data file
        :return: A pandas DataFrame with the file contents
        """
        file_sep = DEFAULT_FILE_SEP
        # Column separators can be preceded or succedded by optional spaces
        df_header = pd.read_csv(file_path, sep=file_sep, engine="python")
        new_columns = {}
        for col in df_header.columns:
            if ("geo" in col) and (
                (desired_columns is None) or (region_col_name in desired_columns)
            ):
                new_columns[col] = region_col_name
            elif (desired_columns is None) or (col in desired_columns):
                new_columns[col] = col

        df = pd.read_csv(file_path, sep=file_sep, engine="python", skiprows=1)
        # Need to select the keys in "new_columns" and change their names to the
        # values in "new_columns"
        df = df.rename(columns=new_columns)[new_columns.values()]
        return df

    def __str__(self) -> str:
        """
        Override default string representation
        :return: Class instance string representation
        """
        return self.__class__.__name__


REPRESENTATION_STRATEGIES = {
    "csv": TSVRepresentationStrategy,
    "tsv": TSVRepresentationStrategy,
    "json": JSONRepresentationStrategy,
}


def convert_representation_strategy(
    representation_val: typing.Optional[str],
) -> typing.Optional[DataRepresentationStrategy]:
    """
    Checks if the representation strategy, provided as a string, is among the supported
    strategies. If so, it creates and returns the appropriate strategy, otherwise
    return None
    :param representation_val: The string containing the desired representation strategy
    :return: The appropriate instance for the desired representation, if it is supported,
             otherwise None
    """
    if representation_val is not None:
        # Convert representation_val to lower case
        representation_val = representation_val.lower()
        if representation_val in REPRESENTATION_STRATEGIES:
            # Get and instantiate the desired representation strategy
            return REPRESENTATION_STRATEGIES[representation_val]()
    return None
