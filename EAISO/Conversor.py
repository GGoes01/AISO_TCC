from Fitness import calc_dist
from Coordenada import Coordenada


def gerar_matriz(mapa):

    pos = Coordenada(mapa)
    coords = pos.ler_coordenadas()
    coords_mt = []

    for cidade_a in coords:
        dists = []
        for cidade_b in coords:
            dists.append(calc_dist(cidade_a, cidade_b))

        coords_mt.append(dists.copy())

    return coords_mt
