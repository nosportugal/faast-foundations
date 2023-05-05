"""Specifica o que este script faz"""
import argparse as ag
from pathlib import Path
import os
import pandas as pd
import numpy as np



FILE_AUX_INPUT = "eu_life_expectancy_raw.tsv"
FILE_AUX_OUTPUT = "pt_life_expectancy.csv"
DATA_PATH = Path(__file__).parent / 'data'


def load_data(fname_input=FILE_AUX_INPUT):

    """Função que importa ficheiro """
    life = pd.read_csv(os.path.join(DATA_PATH, fname_input), delimiter='\t')
    return life

def clean_data(df_input,
    country= "PT"):

    """Função que trabalha dados """
    df_input[['unit','sex','age','region']]=(
        df_input['unit,sex,age,geo\\time'].str.split(",",expand=True)
    )
    df_input.drop(columns='unit,sex,age,geo\\time', inplace=True)
    df_input = pd.melt(df_input, id_vars=['unit', 'sex', 'age', 'region'], var_name="year")
    df_input = df_input.astype({'year':'int'})
    df_input.replace(": ", np.nan, inplace  = True)
    df_input = df_input.dropna(axis=0, how='any', subset="value")
    df_input['value'] = df_input['value'].str.split(' ').str[0]
    df_input = df_input.astype({'value':float}, errors="raise")
    df_input = df_input[df_input["region"] == country]
    return df_input

def save_data(df_input, fname_output=FILE_AUX_OUTPUT):

    """Função que exporta ficheiro"""
    df_input.to_csv(os.path.join(DATA_PATH, fname_output), index=False, encoding='utf-8')

def main(fname_input=FILE_AUX_INPUT,
    country="PT",
    fname_output=FILE_AUX_OUTPUT):

    """Função main que invoca as 3 funções """
    df_load = load_data(fname_input)
    df_load = clean_data(df_load, country)
    save_data(df_load, fname_output)






if __name__ == "__main__":  # pragma: no cover
    parser = ag.ArgumentParser(description='Indicar o Pais.')
    parser.add_argument("-c",'--country', default="PT", help='Nome do Pais (default: PT)')
    args = parser.parse_args()

    #clean_data("eu_life_expectancy_raw.tsv", "pt_life_expectancy_teste.csv",args.country )
    #clean_data(country=args.country )
    main(country=args.country)
