from Coordenada import Coordenada
from Gerador import Gerador
from Gerador import calcular_afinidade
from Celula import Celula
from Memoria import Memoria
from Memoria import recuperar_memoria
from Fitness import Fitness
from GameTheory import GameTheory as gt
from Conversor import gerar_matriz
import random as rnd
import time
import os


class AISO:

    def __init__(self, num_cel, num_ger, num_clones, file, num_par=0, num_rod=0, game_theory=False, evolutionary=True):
        self.__num_cel = num_cel
        self.__num_ger = num_ger
        self.__num_clones = num_clones
        self.__file = file
        self.__num_par = num_par
        self.__num_rod = num_rod
        self.__gt = game_theory
        self.__e = evolutionary

    def mutacionar(self, rota_celula_mae):
        num_trocas = rnd.randint(1, int(len(rota_celula_mae)*.35))
        posicoes = [cont for cont in range(len(rota_celula_mae))]  # gera uma lista com valores de 0 até len(rota_mae)-1
        nova_rota = list(rota_celula_mae)  # copia a rota da celula mãe

        for cont in range(num_trocas):  # de acordo com o número de trocas
            pos_a = rnd.choice(posicoes)  # escolhe uma posição desntre as da lista
            posicoes.pop(posicoes.index(pos_a))  # remove a posição da lista

            pos_b = rnd.choice(posicoes)
            posicoes.pop(posicoes.index(pos_b))

            nova_rota[pos_a], nova_rota[pos_b] = nova_rota[pos_b], nova_rota[pos_a]

        return nova_rota

    def clonar(self, vetor_celulas, quantidade_de_clones, matriz_dist):
        novo_vetor = []

        for celula in vetor_celulas:
            novo_vetor.append(celula)
            clones_bonus = int(quantidade_de_clones * celula.get_afinidade())
            total_clones = clones_bonus + quantidade_de_clones

            for contador in range(total_clones):
                rota_mutacionada = self.mutacionar(list(celula.get_rota()))
                fit = Fitness(rota_mutacionada, matriz_dist)
                fitness = fit.calcular()
                celula_clone = Celula(rota_mutacionada, fitness, 0, 0, 0)
                novo_vetor.append(celula_clone)

        return novo_vetor

    def executar(self):

        matriz_dist = gerar_matriz(self.__file)

        pop = Gerador(self.__num_cel, matriz_dist, evolutionary=self.__e)
        populacao = pop.gerar_populacao()

        melhores_fitness = []  # lista preenchida com o melhor fitness de cada geração
        piores_fitness = []  # lista preenchida com os piores fitness de cada geração

        mem = Memoria()
        vetor_memoria = list(populacao)
        mem.ordenar_memoria(vetor_memoria)
        for ger in range(self.__num_ger):
            inicio = time.time()

            num_clones = int(self.__num_clones)

            populacao = self.clonar(populacao, num_clones, matriz_dist)
            if self.__e:
                populacao = calcular_afinidade(populacao)

            if self.__gt:
                jogo = gt(populacao, num_rodadas=self.__num_rod, num_partidas=self.__num_par)
                populacao = jogo.jogar()

            mem_temp = Memoria()
            mem_temp.ordenar_memoria(list(populacao))
            vetor_memoria_temp = mem_temp.get_memoria()

            for celula in vetor_memoria_temp:
                ja_existe = False

                for outra_celula in vetor_memoria:
                    if celula == outra_celula:
                        ja_existe = True

                if not ja_existe:
                    if celula.get_fitness() < vetor_memoria[-1].get_fitness():
                        vetor_memoria[-1] = celula
                        mem.ordenar_memoria(list(vetor_memoria))
                        vetor_memoria = mem.get_memoria()

            melhor_fitness = populacao[0].get_fitness()
            pior_fitness = populacao[0].get_fitness()
            fit_total = 0

            for celula in populacao:
                if celula.get_fitness() < melhor_fitness:
                    melhor_fitness = celula.get_fitness()

                elif celula.get_fitness() > pior_fitness:
                    pior_fitness = celula.get_fitness()

                fit_total += celula.get_fitness()

            populacao = list(vetor_memoria)

            num_eliminados = int(len(populacao)*0.1)

            for contador in range(num_eliminados):
                populacao.pop(-1)

            novas_celulas = Gerador(num_eliminados, matriz_dist)
            pop_adicional = novas_celulas.gerar_populacao()

            populacao += pop_adicional

            fim = time.time()
            print(ger, populacao[0].get_fitness(), fim-inicio)

            melhores_fitness.append(melhor_fitness)
            piores_fitness.append(pior_fitness)

        return melhores_fitness, piores_fitness
