from AISO import Aiso
import matplotlib.pyplot as plt

<<<<<<< Updated upstream
aiso = Aiso('paths/kroA100.tsp', num_ger=500, num_cel=10, num_clones=150, validade=3)
aiso.executar()
=======
aiso = Aiso('paths/kroA100.tsp', num_ger=100, num_cel=10, num_clones=200, validade=3)
resultados = aiso.executar()
>>>>>>> Stashed changes

plt.plot(resultados.index, resultados.melhores)
plt.scatter(resultados.index, resultados.melhores)
plt.show()

<<<<<<< Updated upstream
'''
250, 5, 100 - 37948.021
250, 5, 100 - 43293.418
250, 5, 125 - 44819.489
250, 5, 75 - 39216.513
250, 5, 75 - 40728.226
250, 5, 75 - 41073.638
250, 5, 75 - 42082.060
500, 5, 75 - 36201.949
250, 3, 75 - 42407.352
'''
=======
# Implementar gráficos
>>>>>>> Stashed changes
