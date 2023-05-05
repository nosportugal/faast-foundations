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
AUX="JOAO"
#funcao clifeandata

def clean_data(
    country="PT",
    file_input=AUX_NAME_INFILE,
    file_output=AUX_NAME_OUTPUT,
    file_path=AUX_DATA_PATH
    ):

    """Funcao:clifean_data para limpeza de ficheiro"""

    print(f"Abre ficheiro: {file_input}")
    print(f"Arg:{country}")
    life = pd.read_csv(os.path.join(file_path,file_input), delimiter='\t')
    print("Alteracoes em curso...")
    life[['unit','sex','age','region']] = life['unit,sex,age,geo\\time'].str.split(",",expand=True)
    life.drop(columns='unit,sex,age,geo\\time', inplace=True)
    life = pd.melt(life, id_vars=['unit', 'sex', 'age', 'region'], var_name="year")
    life = life.astype({'year':'int'})
    life.replace(": ", np.nan, inplace= True)
    life = life.dropna(axis=0, how='any',subset='value')
    life['value'] = life['value'].str.split(' ').str[0]
    life = life.astype({'value':float}, errors="raise")
    life_pt = life[life["region"] == country]
    print(f"Vai gerar o ficheiro: {file_output}")
    life_pt.to_csv(os.path.join(file_path,file_output), index=False, encoding='utf-8')

if __name__ == "__main__" :

    parser = ag.ArgumentParser(description='Indicar o Pais.')
    parser.add_argument("-c",'--country', default="PT", help='Nome do Pais (default: PT)')

    args = parser.parse_args()
    clean_data(country=args.country)
