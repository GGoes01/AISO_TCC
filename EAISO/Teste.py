import time
from datetime import datetime
import matplotlib.pyplot as plt
from AISO import AISO
import seaborn as sns
import numpy as np
import pandas as pd


num_execucoes = 5
pop_ini = 25
num_geracoes = 200
evolucao = True
gt = False
mapa = "paths/att532.tsp"

melhores = np.zeros(num_geracoes)
piores = np.zeros(num_geracoes)

for execuao in range(num_execucoes):

    eaiso = AISO(num_cel=pop_ini, num_ger=num_geracoes, num_clones=250, file=mapa)
    print(execuao)

    inicio = time.time()
    melhores_aux, piores_aux = eaiso.executar()
    fim = time.time()
    tempo = fim - inicio

    print(tempo, end="\n")

    melhores += melhores_aux
    piores += piores_aux

melhores /= num_execucoes
piores /= num_execucoes

paletteA = ['#4AAD36']
paletteB = ['#BD2F2D']

geracao = [i for i in range(num_geracoes)]
arquivo = str(datetime.now()).replace(' ', '_').replace(':', '').split('.')[0]
mapa = mapa.split('.')[0]
mapa = mapa.split('/')[1]

plt.figure(0)
sns.set_style("darkgrid", {"axes.facecolor": ".9"})
sns.set_context("notebook", font_scale=1.25)
sns.set_palette(paletteA)
grafico_melhores = sns.lineplot(x=geracao, y=melhores)
grafico_melhores.figure.set_size_inches(12, 8)
grafico_melhores.set_title('Melhores Resultados - ' + mapa, fontsize=22, loc='left')
grafico_melhores.set_xlabel('Geração', fontsize=18)
grafico_melhores.set_ylabel('Resultado', fontsize=18)
nome_arquivo = 'resultados/melhores' + arquivo + '.png'
plt.savefig(fname=nome_arquivo, format='png')

plt.figure(1)
sns.set_style("darkgrid", {"axes.facecolor": ".9"})
sns.set_context("notebook", font_scale=1.25)
sns.set_palette(paletteB)
grafico_piores = sns.lineplot(x=geracao, y=piores)
grafico_piores.figure.set_size_inches(12, 8)
grafico_piores.set_title('Piores Resultados - ' + mapa, fontsize=22, loc='left')
grafico_piores.set_xlabel('Geração', fontsize=18)
grafico_piores.set_ylabel('Resultado', fontsize=18)
nome_arquivo = 'resultados/piores' + arquivo + '.png'
plt.savefig(fname=nome_arquivo, format='png')

resultados = pd.DataFrame({"melhores": melhores, "piores": piores})
resultados.to_csv('resultados/resultados'+arquivo+'.csv', sep=';', index=False)
