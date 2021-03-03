import math


def calc_dist(coord1, coord2):
    __x1 = coord1[0]
    __y1 = coord1[1]
    __x2 = coord2[0]
    __y2 = coord2[1]

    dist = math.sqrt((__x1 - __x2)**2 + (__y1 - __y2)**2)

    return dist


class Fitness:

    def __init__(self, rota, matriz_dist):
        self.__rota = list(rota)
        self.__matriz_dist = list(matriz_dist)

    def calcular(self):

        distancia = 0.0

        for pos in self.__rota:
            if pos == self.__rota[-1]:
                distancia += self.__matriz_dist[pos][self.__rota[0]]

            else:
                indice = self.__rota.index(pos) + 1
                pos_b = self.__rota[indice]
                distancia += self.__matriz_dist[pos][pos_b]

        return distancia

