"""Tests for the usage of the Region class (life_expectancy.region.Region)"""
# condig:utf-8

import typing

from life_expectancy.region import Region


__author__ = "Joaquim Leitão"
__email__ = "joaquim.leitao@nos.pt"


def test_expected_countries(expected_regions: typing.List[str]) -> None:
    """
    Test the `list_all_countries` classmethod in the life_expectancy.region.Region
    :param expected_regions: A list of the expected regions that should be supported in
                             life_expectancy.region.Region
    """
    region_list = Region.list_all_countries()

    # Check if both lists of regions have the same number of elements
    assert len(region_list) == len(expected_regions)

    # Make sure every region in "region_list" is present in the expected output
    for region in region_list:
        if region not in expected_regions:
            assert False

    # Make sure every region in the expected output is present in "region_list"
    for region in expected_regions:
        if region not in region_list:
            assert False
