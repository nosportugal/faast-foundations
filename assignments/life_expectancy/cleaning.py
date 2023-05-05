"""Specifica o que este script faz"""
import argparse as ag
from pathlib import Path
import os
import pandas as pd
import numpy as np



FILE_AUX_INPUT = "eu_life_expectancy_raw.tsv"
FILE_AUX_OUTPUT = "pt_life_expectancy.csv"
DATA_PATH = Path(__file__).parent / 'data'

def clean_data(
    fname_input=FILE_AUX_INPUT,
    fname_output=FILE_AUX_OUTPUT,
    country= "PT"):

    """Função que importa ficheiro e trabalha dados e exporta novamente"""
    life = pd.read_csv(os.path.join(DATA_PATH, fname_input), delimiter='\t')
    life[['unit','sex','age','region']]=life['unit,sex,age,geo\\time'].str.split(",",expand=True)
    life.drop(columns='unit,sex,age,geo\\time', inplace=True)
    life = pd.melt(life, id_vars=['unit', 'sex', 'age', 'region'], var_name="year")
    life = life.astype({'year':'int'})
    life.replace(": ", np.nan, inplace  = True)
    life = life.dropna(axis=0, how='any', subset="value")
    life['value'] = life['value'].str.split(' ').str[0]
    life = life.astype({'value':float}, errors="raise")
    life_pt = life[life["region"] == country]
    life_pt.to_csv(os.path.join(DATA_PATH, fname_output), index=False, encoding='utf-8')

if __name__ == "__main__":  # pragma: no cover
    parser = ag.ArgumentParser(description='Indicar o Pais.')
    parser.add_argument("-c",'--country', default="PT", help='Nome do Pais (default: PT)')
    args = parser.parse_args()

    #clean_data("eu_life_expectancy_raw.tsv", "pt_life_expectancy_teste.csv",args.country )
    clean_data(country=args.country )
