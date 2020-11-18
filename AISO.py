import pandas as pd
from Mapa import Mapa
from Memoria import Memoria
from Populacao import Populacao, calcular_afinidade
from Fitness import Fitness
import random


def mutacionar(rota_celula_mae):
    nova_rota = list(rota_celula_mae)
    selecao = random.choices(rota_celula_mae, k=2)
    nova_rota[selecao[0]], nova_rota[selecao[1]] = nova_rota[selecao[1]], nova_rota[selecao[0]]

    return nova_rota


def clonar(populacao, num_clones, geracao, validade, cidades):
    for index, celula_mae in populacao.iterrows():
        id_clones = []
        fit_clones = []
        val_clones = []
        af_clones = []
        rt_clones = []

        bonus = num_clones * celula_mae.afinidade
        total_clones = num_clones + bonus

        for contador in range(int(total_clones)):
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

        clones = {'id': id_clones, 'fitness': fit_clones, 'validade': val_clones, 'afinidade': af_clones,
                  'rota': rt_clones}
        clones = pd.DataFrame(clones)

        populacao = populacao.append(clones)

    populacao = calcular_afinidade(populacao)
    populacao.index = range(populacao.shape[0])

    return populacao


class Aiso:

    def __init__(self, mapa, num_ger, num_cel, num_clones, validade, execucao=1):
        self.__num_ger = num_ger
        self.__num_cel = num_cel
        self.__num_clones = num_clones
        self.__mapa = mapa
        self.__validade = validade
        self.__execucao = execucao

    def executar(self):

        mapa = Mapa(self.__mapa)
        cidades = mapa.ler_coordenadas()
        pop = Populacao(self.__num_cel, self.__validade, cidades, 0)
        populacao = pop.gerar_populacao()
        mem = Memoria(populacao.copy())
        mem.ordenar_memoria()
        resultados = pd.DataFrame({'melhores': [], 'piores': []})

        for geracao in range(self.__num_ger):
            # Clona a população de acordo com a quantidade estipulada de clones
            populacao = clonar(populacao, self.__num_clones, geracao, self.__validade, cidades)
            populacao = pd.DataFrame(populacao)

            # Ordena os valores da população de acordo com o 'fitness'
            populacao.sort_values(by='fitness', inplace=True)
            populacao.index = range(populacao.shape[0])

            # Cria um data set temporário para a memória
            memoria = pd.DataFrame(mem.get_memoria())

            for index, celula in populacao.iterrows():

                # Armazena o pior valor de 'fitness'
                pior_fit = memoria.fitness.max()

                # Verifica quais células já estão presentes na memória
                talvez_exista = memoria.fitness == celula.fitness
                existe = False

                for possibilidade in talvez_exista:
                    if possibilidade:
                        existe = True

                # Armazena somente as células que não estão presentes na memória e possuem um 'fitness' melhor do que o
                # pior já armazenado
                if (celula.fitness < pior_fit) and (not existe):
                    memoria.drop([memoria.shape[0] - 1], inplace=True)
                    memoria = memoria.append(celula, ignore_index=True)
                    memoria.sort_values(by='fitness', inplace=True)
                    memoria.index = range(memoria.shape[0])

            resultados = resultados.append({'melhores': memoria.fitness.min().copy(),
                                            'piores': populacao.fitness.max().copy()}, ignore_index=True)

            memoria.validade -= 1
            for index, row in memoria.iterrows():
                if row.validade < 0:
                    memoria.loc[index, 'fitness'] = 100000

            populacao = memoria.copy()
            populacao.sort_values(by='fitness', inplace=True)
            populacao.index = range(populacao.shape[0])
            mem.set_memoria(memoria.copy())
            mem.ordenar_memoria()

            print(f'\n### {geracao} - {self.__execucao} ###\n{populacao.loc[0, "fitness"]}')

        return resultados

