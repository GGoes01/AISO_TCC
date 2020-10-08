from AISO import mutacionar, clonar
from Mapa import Mapa
from Populacao import Populacao
import pandas as pd
import numpy as np

mapa = Mapa("paths/bayg29.tsp")

pop = Populacao(10, 0, mapa.ler_coordenadas(), 0)
populacao = pop.gerar_populacao()

print(populacao[["id", "fitness", "afinidade"]], end="\n\n")

populacao = clonar(populacao, 5, 1, 0, mapa.ler_coordenadas())

populacao.sort_values(by="fitness", inplace=True)
print(populacao[["id", "fitness", "afinidade"]])

# for index, row in populacao.iterrows():
#     nova_rota = mutacionar(populacao.loc[index, "rota"])
#
#     print(populacao.loc[index, "rota"])
#     row["rota"] = nova_rota
#     populacao.loc[index] = row
#     print(populacao.loc[index, "rota"])
#     print(len(nova_rota), end="\n\n")

