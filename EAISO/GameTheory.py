import random


def aplicar_penalidade(celula, rodadas, partidas):
    temptation = 24
    pior_resultado = temptation*rodadas*partidas
    taxa_penalidade = celula.get_ganho()/pior_resultado
    penalidade = celula.get_afinidade()*(1-taxa_penalidade)
    celula.set_afinidade(penalidade)


class GameTheory:

    def __init__(self, populacao, num_rodadas=1, num_partidas=1):
        self.__dilema = list(populacao)
        self.__rodadas = num_rodadas
        self.__partidas = num_partidas

    def jogar(self):

        celulas = self.__dilema
        for celula in celulas:
            celula.set_comportamento(random.choice(["Cooperar", "Trair"]))

        sucker = 3
        punishment = 6
        reward = 18
        temptation = 24

        for partida in range(self.__partidas):
            for rodada in range(self.__rodadas):
                tamanho = len(celulas)
                random.shuffle(celulas)

                adversarios = [[], []]

                for cont in range(int(tamanho/2)):
                    adversarios[0].append(celulas[cont])

                for cont in range(int(tamanho/2), tamanho):
                    adversarios[1].append(celulas[cont])

                num_confrontos = tamanho//2

                for cont in range(num_confrontos):
                    comportamento_a = adversarios[0][cont].get_comportamento()
                    comportamento_b = adversarios[1][cont].get_comportamento()

                    if comportamento_a == comportamento_b:
                        if comportamento_a == "Cooperar":
                            ganho_a = reward + adversarios[0][cont].get_ganho()
                            ganho_b = reward + adversarios[1][cont].get_ganho()

                            adversarios[0][cont].set_ganho(ganho_a)
                            adversarios[1][cont].set_ganho(ganho_b)

                        if comportamento_a == "Trair":
                            ganho_a = punishment + adversarios[0][cont].get_ganho()
                            ganho_b = punishment + adversarios[1][cont].get_ganho()

                            adversarios[0][cont].set_ganho(ganho_a)
                            adversarios[1][cont].set_ganho(ganho_b)

                    elif comportamento_a == "Cooperar" and comportamento_b == "Trair":
                        ganho_a = sucker + adversarios[0][cont].get_ganho()
                        ganho_b = temptation + adversarios[1][cont].get_ganho()

                        adversarios[0][cont].set_ganho(ganho_a)
                        adversarios[1][cont].set_ganho(ganho_b)

                    elif comportamento_a == "Trair" and comportamento_b == "Cooperar":
                        ganho_a = temptation + adversarios[0][cont].get_ganho()
                        ganho_b = sucker + adversarios[1][cont].get_ganho()

                        adversarios[0][cont].set_ganho(ganho_a)
                        adversarios[1][cont].set_ganho(ganho_b)

                retorno = []
                retorno += adversarios[0].copy()
                retorno += adversarios[1].copy()

        for celula in retorno:
            aplicar_penalidade(celula, self.__partidas, self.__rodadas)

        return retorno
