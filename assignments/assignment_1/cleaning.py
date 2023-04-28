"""Specifica o que este script faz"""
import pandas as pd
import numpy as np
import argparse as ag

def clean_data(fname_input, fname_output, country):
    """Função que importa ficheiro e trabalha dados e exporta novamente"""
    life = pd.read_csv("../life_expectancy/data/" + fname_input, delimiter='\t')
    life[['unit','sex','age','region']]=life['unit,sex,age,geo\\time'].str.split(",",expand=True)
    life.drop(columns='unit,sex,age,geo\\time', inplace=True)
    life = pd.melt(life, id_vars=['unit', 'sex', 'age', 'region'], var_name="year")
    life = life.astype({'year':'int'})
    life.replace(": ", np.nan, inplace  = True)
    life['value'] = life['value'].str.split(' ').str[0]
    life = life.astype({'value':float}, errors="raise")
    life_pt = life[life["region"] == country]
    life_pt.to_csv("../life_expectancy/data/" + fname_output, index=False, encoding='utf-8')

if __name__ == "__main__":  # pragma: no cover
    parser = ag.ArgumentParser(description='Indicar o Pais.')
    parser.add_argument("-c",'--country', default="PT", help='Nome do Pais (default: PT)')
    args = parser.parse_args()
    clean_data("eu_life_expectancy_raw.tsv", "pt_life_expectancy_teste.csv",args.country )