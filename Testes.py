from AISO import Aiso
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from datetime import datetime

resultados = pd.DataFrame({'melhores': [], 'piores': []})
num_execucoes = 1

for execucao in range(num_execucoes):
    aiso = Aiso('paths/kroA100.tsp', num_ger=20, num_cel=10, num_clones=10, validade=3)
    if resultados.shape[0] == 0:
        resultados = aiso.executar().copy()

    else:
        resultados += aiso.executar().copy()

resultados /= num_execucoes
geracao = [i for i in range(resultados.shape[0])]

# palette = ['#4AAD36', '#BD2F2D', '#C79E3A', '#3396C4', '#9224BD']

paletteA = ['#4AAD36']
paletteB = ['#BD2F2D']

sns.set_style("darkgrid", {"axes.facecolor": ".9"})
sns.set_context("poster", font_scale=0.5)
plt.figure(figsize=(20, 15))

sns.set_palette(paletteA)
grafico = plt.subplot(1, 2, 1)
sns.lineplot(x=geracao, y='melhores', data=resultados)
plt.title('Melhores Resultados')
plt.ylabel('Fitness')
plt.xlabel('Geração')

sns.set_palette(paletteB)
plt.subplot(1, 2, 2)
sns.lineplot(x=geracao, y='piores', data=resultados)
plt.title('Piores Resultados')
plt.ylabel('Fitness')
plt.xlabel('Geração')

arquivo = str(datetime.now()).replace(' ', '_').replace(':', '').split('.')[0]
arquivo = 'resultados/' + arquivo + '.png'
plt.savefig(fname=arquivo, format='png')
plt.show()

# É melhor separar os gráficos
