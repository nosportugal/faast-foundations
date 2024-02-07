"""Simple script to extract all distinct regions from the entire life_expectancy data"""
# coding: utf-8

from life_expectancy.load_data import TSVRepresentationStrategy
from life_expectancy.defaults import DEFAULT_REGION_COL_NAME

__author__ = "Joaquim Leitão"
__email__ = "joaquim.leitao@nos.pt"


if __name__ == "__main__":
    # Load entire raw data
    raw_df = TSVRepresentationStrategy().load_data(
        "../data/eu_life_expectancy_raw.tsv", "region"
    )

    # Select distinct values from column "region"
    unique_regions_sorted = (
        raw_df[DEFAULT_REGION_COL_NAME].drop_duplicates().sort_values(ascending=True)
    )

    print(unique_regions_sorted)
