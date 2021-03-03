class Celula:
    def __init__(self, id, fitness, validade, afinidade, rota):
        self.__id = id
        self.__fitness = fitness
        self.__validade = validade
        self.__afinidade = afinidade
        self.__rota = rota

    def get_id(self):
        return self.__id

    def set_id(self, id):
        self.__id = id

    def get_fitness(self):
        return self.__fitness

    def set_fitness(self, fitness):
        self.__fitness = fitness

    def get_validade(self):
        return self.__validade

    def set_validade(self, validade):
        self.__validade = validade

    def get_afinidade(self):
        return self.__afinidade

    def set_afinidade(self, afinidade):
        self.__afinidade = afinidade

    def get_rota(self):
        return self.__rota

    def set_rota(self, rota):
        self.__rota = rota

    def get_celula(self):
        celula = {'id': self.__id, 'fitness': self.__fitness, 'validade': self.__validade, 'afinidade': self.__afinidade, 'rota': self.__rota}
        return celula
