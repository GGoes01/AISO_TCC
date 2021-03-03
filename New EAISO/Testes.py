from AISO import Aiso
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from datetime import datetime

resultados = pd.DataFrame({'melhores': [], 'piores': []})
num_execucoes = 1

mapa = 'att532.tsp'

for execucao in range(num_execucoes):
    aiso = Aiso('paths/' + mapa, num_ger=200, num_cel=25, tamanho_mem=25, num_clones=1000,
                validade=3, execucao=execucao)
    if resultados.shape[0] == 0:
        resultados = aiso.executar().copy()

    else:
        resultados += aiso.executar().copy()

resultados /= num_execucoes
mapa = mapa.split('.')[0]
arquivo = str(datetime.now()).replace(' ', '_').replace(':', '').split('.')[0]
resultados.to_csv('resultados/resultados'+arquivo+'.csv', sep=';', index=False)
geracao = [i for i in range(resultados.shape[0])]

# palette = ['#4AAD36', '#BD2F2D', '#C79E3A', '#3396C4', '#9224BD']

paletteA = ['#4AAD36']
paletteB = ['#BD2F2D']

plt.figure(0)
sns.set_style("darkgrid", {"axes.facecolor": ".9"})
sns.set_context("talk", font_scale=0.5)
sns.set_palette(paletteA)
grafico_melhores = sns.lineplot(x=geracao, y='melhores', data=resultados)
grafico_melhores.figure.set_size_inches(12, 8)
grafico_melhores.set_title('Melhores Resultados - ' + mapa, fontsize=18, loc='left')
grafico_melhores.set_xlabel('Geração', fontsize=14)
grafico_melhores.set_ylabel('Resultado', fontsize=14)
nome_arquivo = 'resultados/melhores' + arquivo + '.png'
plt.savefig(fname=nome_arquivo, format='png', transparent=True)

plt.figure(1)
sns.set_style("darkgrid", {"axes.facecolor": ".9"})
sns.set_context("talk", font_scale=0.5)
sns.set_palette(paletteB)
grafico_piores = sns.lineplot(x=geracao, y='piores', data=resultados)
grafico_piores.figure.set_size_inches(12, 8)
grafico_piores.set_title('Piores Resultados - ' + mapa, fontsize=18, loc='left')
grafico_piores.set_xlabel('Geração', fontsize=14)
grafico_piores.set_ylabel('Resultado', fontsize=14)
nome_arquivo = 'resultados/piores' + arquivo + '.png'
plt.savefig(fname=nome_arquivo, format='png', transparent=True)


