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

    def __init__(self, mapa, num_ger, tamanho_mem, num_cel, num_clones, validade, execucao=1):
        self.__mapa = mapa
        self.__num_ger = num_ger
        self.__tamanho_mem = tamanho_mem
        self.__num_cel = num_cel
        self.__num_clones = num_clones
        self.__validade = validade
        self.__execucao = execucao

    def executar(self):

        resultados = pd.DataFrame({'melhores': [], 'piores': []})  # Cria o DF para armazenar os resultados

        mapa = Mapa(self.__mapa)  # Instancia e lê as coordenadas do mapa escolhido
        cidades = mapa.ler_coordenadas()

        pop = Populacao(self.__num_cel, self.__validade, cidades, 0)  # Instancia uma nova população
        populacao = pop.gerar_populacao()  # Gera o DF da população
        populacao.sort_values(by='fitness', inplace=True)  # Ordena a população de acordo com o fitness
        populacao.index = range(populacao.shape[0])  # Ajusta o índice da população
        mem = Memoria(populacao[:self.__tamanho_mem].copy())  # Armazena na memória uma parcela da população
        mem.ordenar_memoria()  # Ordena a memória

        for geracao in range(self.__num_ger):  # Para cada geração:

            # Clona a população de acordo com a quantidade estipulada de clones
            populacao = clonar(populacao, self.__num_clones, geracao, self.__validade, cidades)
            populacao = pd.DataFrame(populacao)

            # Ordena os valores da população de acordo com o 'fitness'
            populacao.sort_values(by='fitness', inplace=True)
            populacao.index = range(populacao.shape[0])

            # Cria um data set temporário para a memória
            memoria = pd.DataFrame(mem.get_memoria())

            # Verifica uma a uma as células presentes na memória
            for index, celula in populacao.iterrows():

                # Armazena o pior valor de fitness
                pior_fit = memoria.fitness.max()

                # Verifica quais células já estão presentes na memória de acordo com o fitness
                talvez_exista = memoria.fitness == celula.fitness
                existe = False

                for possibilidade in talvez_exista:
                    if possibilidade:
                        existe = True

                # Armazena somente as células que não estão presentes na memória e possuem um 'fitness' melhor do que o
                # pior já armazenado
                if (celula.fitness < pior_fit) and (not existe):
                    memoria.drop([memoria.shape[0] - 1], inplace=True)  # Remove a última célula
                    memoria = memoria.append(celula, ignore_index=True)  # Adiciona a célula nova
                    memoria.sort_values(by='fitness', inplace=True)  # Ordena a população de acordo com o fitness
                    memoria.index = range(memoria.shape[0])  # Ajusta o índice da população

            # Armazena o melhor fitness da memória e o pior fitness da população
            resultados = resultados.append({'melhores': memoria.fitness.min().copy(),
                                            'piores': populacao.fitness.max().copy()}, ignore_index=True)

            # Diminui a validade das células
            memoria.validade -= 1

            # Verifica uma a uma as células presentes na memória
            for index, row in memoria.iterrows():
                if row.validade < 0:  # Modifica o fitness se a validade for menor que zero
                    memoria.loc[index, 'fitness'] += row.fitness * 0.5

            populacao = memoria.copy()
            populacao = clonar(populacao, int(self.__num_cel/self.__tamanho_mem - 1),
                               geracao, self.__validade, cidades)
            populacao.sort_values(by='fitness', inplace=True)
            populacao.index = range(populacao.shape[0])

            mem.set_memoria(memoria.copy())
            mem.ordenar_memoria()

            print(f'\n### {geracao} - {self.__execucao} ###\n{populacao.loc[0, "fitness"]}')

        return resultados

