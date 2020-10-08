import pandas as pd
from Mapa import Mapa
from Memoria import Memoria
from Populacao import Populacao, calcular_afinidade
from Fitness import Fitness
import random


def mutacionar(rota_celula_mae):
    nova_rota = list(rota_celula_mae)
    num_trocas = random.randint(1, int(len(rota_celula_mae) * 0.05))
    selecao = random.choices(rota_celula_mae, k=(2 * num_trocas))
    for contador in range(0, len(selecao), 2):
        aux = nova_rota[selecao[contador]]
        nova_rota[selecao[contador]] = nova_rota[selecao[contador + 1]]
        nova_rota[selecao[contador + 1]] = aux

    return nova_rota


def clonar(populacao, num_clones, geracao, validade, cidades):
    for index, celula_mae in populacao.iterrows():
        id_clones = []
        fit_clones = []
        val_clones = []
        af_clones = []
        rt_clones = []

        for contador in range(num_clones):
            id = celula_mae["id"].split("_")
            id[0] = str(geracao)
            id[1] = id[2]
            id[2] = str(contador)
            id = id[0] + "_" + id[1] + "_" + id[2]
            id_clones.append(id)

            rota = mutacionar(celula_mae["rota"])
            rt_clones.append(rota)

            fit = Fitness(rota, cidades)
            fit_clones.append(fit.calcular())

            val_clones.append(validade)

            af_clones.append(0)

        clones = {'id': id_clones, 'fitness': fit_clones, 'validade': val_clones, 'afinidade': af_clones, 'rota': rt_clones}
        clones = pd.DataFrame(clones)

        populacao = populacao.append(clones)

    populacao = calcular_afinidade(populacao)
    populacao.index = range(populacao.shape[0])

    return populacao


class Aiso:

    def __init__(self, mapa, num_ger, num_cel, num_clones):
        self.__num_ger = num_ger
        self.__num_cel = num_cel
        self.__num_clones = num_clones
        self.__mapa = mapa



