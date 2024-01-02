"""Simple script to generate expected output with subset of the entire life_expectancy data"""
# coding: utf-8

import locale
import typing
import random

import life_expectancy.cleaning


def _at_least_one_region(rows: typing.List[str], desired_region: str) -> bool:
    """ "
    Checks if there is at least one entry for a given region in the extract provided
    :param rows: The extract to be analysed
    :param desired_region: The region of interest
    :return: True if the extract contains at least one entry for the region of interest, or False
             otherwise
    """
    for row in rows:
        if desired_region in row:
            return True
    return False


def generate_data_subset(
    _input_path: str,
    _desired_region: str,
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


if __name__ == "__main__":
    generate_data_subset(
        _input_path="../data/eu_life_expectancy_raw.tsv",
        _desired_region="PT",
        _percent_rows_select=0.3,
        _output_path="fixtures/eu_life_expectancy_raw_subset.tsv",
    )

    life_expectancy.cleaning.main(
        _input_path="fixtures/eu_life_expectancy_raw_subset.tsv",
        _country="PT",
        _output_path="fixtures/eu_life_expectancy_expected_subset.csv",
    )
