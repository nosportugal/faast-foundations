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

    for region in region_list:
        if region not in expected_regions:
            assert False

    assert expected_regions == region_list

    # assert all(a == b for a, b in zip(region_list, expected_regions))
