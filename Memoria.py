import pandas as pd
from datetime import datetime


class Memoria:

    def __init__(self, memoria):
        self.__memoria = pd.DataFrame(memoria)

    def set_memoria(self, memoria):
        self.__memoria = memoria

    def get_memoria(self):
        return self.__memoria

    def ordenar_memoria(self):
        self.__memoria.sort_values(by='fitness', inplace=True)

    def exportar_memoria(self, mapa):
        now = datetime.now()
        info = str(mapa) + "_" + str(self.__memoria.shape[0]) + "_" + str(now.date()) + "_" + str(now.time()).replace(":", "-")[:8] + '.csv'

        self.__memoria.to_csv(info, sep=';', index=False)

    def importar_memoria(self, arquivo):
        self.__memoria = pd.read_csv(arquivo, sep=';')

