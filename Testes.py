from AISO import mutacionar, clonar
from Mapa import Mapa
from Populacao import Populacao
import pandas as pd
import numpy as np
from AISO import Aiso

aiso = Aiso('paths/kroA100.tsp', num_ger=200, num_cel=5, num_clones=500, validade=10)
aiso.executar()

# falta implementar a validade
# restringir a quantidade de trocas

