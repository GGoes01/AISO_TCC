import pandas as pd
from Celula import Celula
from Fitness import Fitness
import random


def calcular_afinidade(populacao):

    for index, row in populacao.iterrows():
        populacao.loc[index, 'afinidade'] = round((populacao['fitness'].max() - row['fitness']) / populacao['fitness'].min(), 2)

    return populacao


class Populacao:

    def __init__(self, num_celulas, validade, cidades, geracao):
        self.__num_celulas = num_celulas
        self.__cidades = cidades
        self.__geracao = geracao
        self.__validade = validade

    def get_num_celulas(self):
        return self.__num_celulas

    def set_num_celulas(self, num_celulas):
        self.__num_celulas = num_celulas

    def get_cidades(self):
        return self.__cidades

    def set_num_celulas(self, cidades):
        self.__cidades = cidades

    def gerar_populacao(self):
        populacao = []

        for i in range(self.__num_celulas):
            rota = [cidade for cidade in range(len(self.__cidades))]
            random.shuffle(rota)
            fitness = Fitness(rota, self.__cidades)
            id = str(self.__geracao) + '_x' + '_' + str(i)

            celula = Celula(id, fitness.calcular(), 0, 0, rota)
            populacao.append(celula.get_celula())

        populacao = pd.DataFrame(populacao)

        populacao = calcular_afinidade(populacao)

        return populacao


