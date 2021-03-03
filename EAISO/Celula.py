import random


class Celula:

    def __init__(self, rota, fitness, afinidade, ganho, comportamento):
        self.__rota = list(rota)
        self.__fitness = fitness
        self.__afinidade = afinidade
        self.__ganho = ganho
        self.__comportamento = comportamento

    def set_rota(self, rota):
        self.__rota = rota

    def get_rota(self):
        return self.__rota

    def set_fitness(self, fitness):
        self.__fitness = fitness

    def get_fitness(self):
        return self.__fitness

    def set_afinidade(self, afinidade):
        self.__afinidade = afinidade

    def get_afinidade(self):
        return self.__afinidade

    def set_ganho(self, ganho):
        self.__ganho = ganho

    def get_ganho(self):
        return self.__ganho

    def set_comportamento(self, comportamento):
        self.__comportamento = comportamento

    def get_comportamento(self):
        return self.__comportamento

    # def get__celula(self):
    #     celula =f'Fitness: {self.__fitness} Afinidade: {self.__afinidade * 100} Ganho: {self.__ganho} Comportamento: {self.__comportamento} Rota: {self.__rota}'
    #     return celula
