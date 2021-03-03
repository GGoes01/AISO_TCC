class Mapa:

    def __init__(self, arquivo):
        self.__arquivo = arquivo
        self.__coord = []

    def ler_coordenadas(self):

        arq = open(self.__arquivo, "r")

        for line in arq.readlines():
            if line != 'EOF\n':
                index, x, y = line.split()
                self.__coord.append([float(x), float(y)])

        arq.close()

        return self.__coord
