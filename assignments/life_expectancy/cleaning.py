"""It cleans a dataset and exports it"""

import pandas as pd

def clean_data(
    path_input='life_expectancy/data/eu_life_expectancy_raw.tsv',
    path_output='life_expectancy/data/pt_life_expectancy.csv') -> pd.DataFrame:
    """Imports data and make some transformations

    Args:
        path_input (str): Path to file
        path_output (str): Path to export resulting df

    Returns:
        pandas DataFrame: cleaned data
    """

    life_expectancy = pd.read_csv(path_input,sep='\t')

    # Splitting a conjugated column in multiple column
    life_expectancy[['unit', 'sex', 'age', 'region']] = \
        life_expectancy['unit,sex,age,geo\\time'].str.split(',', expand=True)

    # Dropping the conjugated column
    life_expectancy.drop('unit,sex,age,geo\\time', axis=1, inplace=True)

    # From wide to long
    life_expectancy = pd.melt(
        life_expectancy,
        id_vars=['unit', 'sex', 'age', 'region'],
        var_name="year"
    )

    # Cleaning values that were supposed to be null and values with strings attached
    life_expectancy['value'].replace(': ', None, inplace=True)
    life_expectancy['value'] = life_expectancy['value'].str.split(' ', expand=True)[0]

    # Changing column types
    life_expectancy['year'] = life_expectancy['year'].astype(int)
    life_expectancy['value'] = life_expectancy['value'].astype(float)

    # Dropping rows that contain null values
    life_expectancy = life_expectancy.dropna()

    # Filtering only observations about PT
    life_expectancy = life_expectancy[life_expectancy["region"] == "PT"]

    life_expectancy.to_csv(path_output, index=False)

    return life_expectancy

if __name__ == "__main__":  # pragma: no cover
    clean_data()
