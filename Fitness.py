import math


def calc_dist(cidade1, cidade2):
    __x1 = cidade1[0]
    __y1 = cidade1[1]
    __x2 = cidade2[0]
    __y2 = cidade2[1]

    dist = math.sqrt((__x1 - __x2)**2 + (__y1 - __y2)**2)

    return dist


class Fitness:

    def __init__(self, rota, cidades):
        self.__rota = list(rota)
        self.__cidades = list(cidades)

    def calcular(self):

        distancia = 0.0

        for pos in self.__rota:  # Para cada ciade na rota
            if pos == self.__rota[-1]:  # Se for a última cidade
                distancia += calc_dist(self.__cidades[pos], self.__cidades[0])  # Calcula a distância até a primeira

            else:
                indice = self.__rota.index(pos) + 1  # Armazena o índice da cidade seguinte
                pos_b = self.__rota[indice]  # Define a cidade seguinte
                distancia += calc_dist(self.__cidades[pos], self.__cidades[pos_b])  # Calcula a distância entre as
                # cidades

        return distancia
