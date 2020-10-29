import pandas as pd
from Mapa import Mapa
from Memoria import Memoria
from Populacao import Populacao, calcular_afinidade
from Fitness import Fitness
import random


def mutacionar(rota_celula_mae):
    nova_rota = list(rota_celula_mae)
    # num_trocas = random.randint(1, int(len(rota_celula_mae) * 0.05))
    selecao = random.choices(rota_celula_mae, k=2)

    nova_rota[selecao[0]], nova_rota[selecao[1]] = nova_rota[selecao[1]], nova_rota[selecao[0]]

    # for contador in range(0, len(selecao), 2):
    #     aux = nova_rota[selecao[contador]]
    #     nova_rota[selecao[contador]] = nova_rota[selecao[contador + 1]]
    #     nova_rota[selecao[contador + 1]] = aux

    return nova_rota


def clonar(populacao, num_clones, geracao, validade, cidades):
    for index, celula_mae in populacao.iterrows():
        id_clones = []
        fit_clones = []
        val_clones = []
        af_clones = []
        rt_clones = []

        num_clones += int(num_clones * celula_mae.afinidade)

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

    def __init__(self, mapa, num_ger, num_cel, num_clones, validade):
        self.__num_ger = num_ger
        self.__num_cel = num_cel
        self.__num_clones = num_clones
        self.__mapa = mapa
        self.__validade = validade

    def executar(self):

        mapa = Mapa(self.__mapa)
        cidades = mapa.ler_coordenadas()
        pop = Populacao(self.__num_cel, self.__validade, cidades, 0)
        populacao = pop.gerar_populacao()
        mem = Memoria(populacao)
        mem.ordenar_memoria()

        for geracao in range(self.__num_ger):
            populacao = clonar(populacao, self.__num_clones, self.__num_ger, self.__validade, cidades)
            populacao = pd.DataFrame(populacao)

            populacao.sort_values(by='fitness', inplace=True)
            populacao.index = range(populacao.shape[0])

            memoria = pd.DataFrame(mem.get_memoria())

            for index, celula in populacao.iterrows():

                pior_fit = memoria.fitness.max()

                talvez_exista = memoria.id != celula.id
                nao_existe = False

                for possibilidade in talvez_exista:
                    if possibilidade:
                        nao_existe = True

                if (celula.fitness < pior_fit) & nao_existe:
                    memoria.drop([memoria.shape[0] - 1], inplace=True)
                    memoria = memoria.append(celula, ignore_index=True)
                    memoria.sort_values(by='fitness', inplace=True)
                    memoria.index = range(memoria.shape[0])

            memoria.validade -= 1
            memoria_total = memoria.shape[0]
            vivos = memoria.validade > 0
            contagem_vivos = memoria[vivos].shape[0]
            repor = memoria_total - contagem_vivos

            # nova_pop = Populacao(repor, self.__validade, cidades, geracao)
            # memoria.append(nova_pop, ignore_index=True)

            memoria.sort_values(by='fitness', inplace= True)
            memoria.index = range(memoria.shape[0])
            mem.set_memoria(memoria)
            populacao = memoria.copy()

            print(geracao, populacao.iloc[0, 1])





