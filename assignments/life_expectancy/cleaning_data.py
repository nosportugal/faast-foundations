"""Modulo de Limpeza de Ficheiro"""
import os
from pathlib import Path
import argparse as ag
import pandas as pd
import numpy as np

#variaveris auxiliares
AUX_NAME_INFILE = "eu_life_expectancy_raw.tsv"
AUX_NAME_OUTPUT= "pt_life_expectancy.csv"
AUX_DATA_PATH = Path(__file__).parent / 'data'

#funcao load_data

def load_data(
    file_input=AUX_NAME_INFILE,
    file_path=AUX_DATA_PATH
    ):

    """Funcao:load_data para leitura de ficheiro"""

    print(f"LOAD_DATA:Abre ficheiro: {file_input}")
    life = pd.read_csv(os.path.join(file_path,file_input), delimiter='\t')
    return life

#funcao clean_data

def clean_data(
    life,
    country="PT",
    ):

    """Funcao:clean_data para limpeza de dados"""

    print("CLEAN_DATA: Alteracoes em curso...")
    life[['unit','sex','age','region']] = life['unit,sex,age,geo\\time'].str.split(",",expand=True)
    life.drop(columns='unit,sex,age,geo\\time', inplace=True)
    life = pd.melt(life, id_vars=['unit', 'sex', 'age', 'region'], var_name="year")
    life = life.astype({'year':'int'})
    life.replace(": ", np.nan, inplace= True)
    life = life.dropna(axis=0, how='any',subset='value')
    life['value'] = life['value'].str.split(' ').str[0]
    life = life.astype({'value':float}, errors="raise")
    life = life[life["region"] == country]
    return life

def save_data(
    life,
    file_output=AUX_NAME_OUTPUT,
    file_path=AUX_DATA_PATH
    ):

    """Funcao:save_data para leitura de ficheiro"""

    print(f"SAVE_DATA: Vai gerar o ficheiro: {file_output}")
    life.to_csv(os.path.join(file_path,file_output), index=False, encoding='utf-8')


def main(
    file_input=AUX_NAME_INFILE,
    file_path=AUX_DATA_PATH,
    file_output=AUX_NAME_OUTPUT,
    country="PT",
    ):

    """Funcao:Main para chamar funcoes"""

    life=load_data(file_input,file_path)
    life=clean_data(life,country)
    save_data(life,file_output,file_path)

if __name__ == "__main__" :

    parser = ag.ArgumentParser(description='Indicar o Pais.')
    parser.add_argument("-c",'--country', default="PT", help='Nome do Pais (default: PT)')

    args = parser.parse_args()

    main(country=args.country)
