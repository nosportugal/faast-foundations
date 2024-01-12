"""Module with data collection/input functions."""
# coding: utf-8


import typing

import pandas as pd

from life_expectancy.defaults import DEFAULT_FILE_SEP

__author__ = "Joaquim Leitão"
__email__ = "joaquim.leitao@nos.pt"


def load_data(file_path: str, file_sep: typing.Optional[str] = None) -> pd.DataFrame:
    """
    Reads the contents of the file in the provided path to a pandas DataFrame
    If the file contains a column with "geo", then it is renamed to "region"
    :param file_path: The local path to the file
    :param file_sep: Optional parameter. Character or regex pattern to treat as the delimiter
    :return: A pandas DataFrame with the file contents
    """
    if file_sep is None:
        file_sep = DEFAULT_FILE_SEP

    # Column separators can be preceded or succedded by optional spaces
    df_header = pd.read_csv(file_path, sep=file_sep, engine="python")
    new_columns = [col if "geo" not in col else "region" for col in df_header.columns]

    df = pd.read_csv(file_path, sep=file_sep, engine="python", skiprows=1)
    df.columns = new_columns

    return df
