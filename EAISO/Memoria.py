def recuperar_memoria(memoria):
    rotas = []
    arq = open(memoria, "r")
    for line in arq.readlines():
        aux1 = line.replace('\n', '')
        aux1 = aux1.replace('[', '')
        aux1 = aux1.replace(']', '')
        aux2 = aux1.split(', ')
        rota = [int(num) for num in aux2]

        rotas.append(rota)

    arq.close()

    return rotas


class Memoria:

    def __init__(self):
        self.__memoria = []

    def get_memoria(self):
        return self.__memoria

    def ordenar_memoria(self, populacao):
        for contador in range(len(populacao)):
            for contador2 in range(contador, len(populacao)):
                if populacao[contador].get_fitness() > populacao[contador2].get_fitness():
                    populacao[contador2], populacao[contador] = populacao[contador], populacao[contador2]

                    contador2 -= 1

        self.__memoria = populacao

    def registrar_memoria(self, memoria):
        arq = open(memoria, "w")
        for celula in self.__memoria:
            rota = celula.get_rota()
            arq.write(str(rota) + '\n')
        arq.close()
