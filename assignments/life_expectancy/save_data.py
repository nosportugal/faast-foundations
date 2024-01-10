"""Module with data storage/saving functions."""
# coding: utf-8


import pandas as pd


def save_data(df: pd.DataFrame, save_file_path: str) -> None:
    """
    Saves the contents of the provided DataFrame in a specified local path
    :param df: The DataFrame to be saved
    :param save_file_path: The local path where the DataFrame is going to be saved
    """
    df.to_csv(save_file_path, index=False)
