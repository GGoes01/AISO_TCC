class Coordenada:

    def __init__(self, caminho):
        self.__caminho = caminho
        self.__coord = []

    def ler_coordenadas(self):

        arq = open(self.__caminho, "r")

        for line in arq.readlines():
            if line != 'EOF\n':
                cut_point = line.index(' ')
                cut_point += 1
                cut_a = line[cut_point:]
                x, y = cut_a.split(' ')
                jump = y.index('\n')
                y = y[:jump]
                self.__coord.append([float(x), float(y)])

        arq.close()

        return self.__coord
