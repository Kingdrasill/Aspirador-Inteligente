import random as rd
import numpy as np

# Classe para guardar e trabalhar com os dados do ambiente
class Ambiente:
    # Metódo de inicialização do Ambiente
    def __init__(self, l, c, size, qtdSuj):
        # Cria o mapa totalmente limpo, l é o número de linhas e c é o número de colunas
        mapa = [['L' for i in range(l)] for j in range(c)]

        # Todas as possíveis posições do mapa
        posicoes = list(range(size))
        
        # Sorteia as posições que terão sujeira, qtdSuj é o número de quadrados sujos
        for i in range(qtdSuj):
            posicao = rd.choice(posicoes)
            x = int(posicao / c)
            y = posicao % c
            mapa[x][y] = 'S'
            posicoes.remove(posicao)
        
        # Sorteia a posição inicial do aspirador 
        inicial = rd.choice(range(size))
        
        # Guarda as informações do mapa
        self.mapa = mapa
        
        # Guarda a posição do aspirador
        self.posicao = [int(inicial / c), inicial % c]
        
        # Guarda a pontuação do aspirador
        self.pontos = 0

    def __str__(self):
        map = ""
        for x in range(len(self.mapa)):
            for y in range(len(self.mapa[0])):
                if x == self.posicao[0] and y == self.posicao[1]:
                    map += f'{self.mapa[x][y]}# '
                else:
                    map += f'{self.mapa[x][y]}  '
            map += '\n'
        return map

    def limpar_posicao(self):
        self.mapa[self.posicao[0]][self.posicao[1]] = 'L'

    def atualizar_pontuacao(self, acao):
        if acao == 'L':
            self.pontos += 3
        elif acao == 'M':
            self.pontos -= 1

    def atualizar_posicao(self, x, y):
        self.posicao[0] = x
        self.posicao[1] = y

class Aspirador:
    def __init__(self, bateria):
        self.memoria = [[], [], []]
        self.direcoes = ['U', 'D', 'L', 'R']
        self.direcao = ''
        self.bateria = bateria

    def sensor_aspirador(self, amb):
        if amb.mapa[amb.posicao[0]][amb.posicao[1]] == 'S':
            return 'Sujo'
        else:
            return 'Limpo'
    
    def acao_aspirador(self, amb, status):
        if status == 'Sujo':
            amb.limpar_posicao()
            amb.atualizar_pontuacao('L')

    def atualizar_dados(self, amb, direcao, status):
        movimento = [direcao, status]
        self.memoria.pop(0)
        self.memoria.append(movimento)

        amb.atualizar_pontuacao('M')
        self.bateria -= 1

    def get_reverse(self, direcao):
        match direcao:
            case 'U':
                return 'D'
            case 'D':
                return 'U'
            case 'L':
                return 'R'
            case 'R':
                return 'L'

    def mover_aspirador(self, amb , direcao):
        x = amb.posicao[0]
        y = amb.posicao[1]

        match direcao:
            case 'U':
                x -= 1
            case 'D':
                x += 1
            case 'L':
                y -= 1
            case 'R':
                y += 1
        
        if x == len(amb.mapa) or x < 0 or y == len(amb.mapa[0]) or y < 0:
            return 'B'
        else:
            amb.atualizar_posicao(x,y)
            return 'L'
        
    def movimentar_aspirador(self, amb):
        memoria = list(x for x in self.memoria if x)
        direcoes = list(self.direcoes)
        anterior = memoria[-1] if memoria else []
        temp_anterior = ''

        if anterior:
            temp_anterior = self.get_reverse(anterior[0])
            direcoes.remove(temp_anterior)
        else:
            self.direcao = rd.choice(direcoes)

        status = self.mover_aspirador(amb, self.direcao)
        self.atualizar_dados(amb, self.direcao, status)

        if status == 'B':
            direcoes.remove(self.direcao)
            self.direcao = self.get_reverse(self.direcao)

            temp_direcao = rd.choice(direcoes)
            status = self.mover_aspirador(amb, temp_direcao)
            self.atualizar_dados(amb, temp_direcao, status)

            if status == 'B':
                direcoes.remove(temp_direcao)
                temp_direcao = rd.choice(direcoes)
                self.direcao = temp_direcao
                
                status = self.mover_aspirador(amb, self.direcao)
                self.atualizar_dados(amb, self.direcao, status)

                if status == 'B':
                    if direcoes:
                        direcoes.remove(temp_direcao)
                        temp_direcao = rd.choice(direcoes)
                        
                        status = self.mover_aspirador(amb, temp_direcao)
                        self.atualizar_dados(amb, temp_direcao, status)

                        if status == 'B':
                            self.bateria = 0
                    else:
                        if temp_anterior != '':
                            status = self.mover_aspirador(amb, temp_anterior)
                            self.atualizar_dados(amb, temp_anterior, status)

def penalizarAspirador(amb):
    for x in range(len(amb.mapa)):
        for y in range(len(amb.mapa[0])):
            if amb.mapa[x][y] == 'S': 
                amb.pontos -= 20

def processData(testes):
    for i in range(len(testes['qtdSujeira'])):
        data = sorted(list(testes['pontuacoes'][i]))
        media = np.mean(data) 
        desvio = np.std(data)

        print(f"{testes['qtdSujeira'][i]} quadrados sujos:")
        print(f"\tMelhor resultado: {data[-1]}")
        print(f"\tPior resultado: {data[0]}")
        print(f"\tMedia: {media}")
        print(f"\tDesvio padrao: {desvio}")
        print()

testes = {
    "qtdSujeira": [16, 12, 8, 4],
    "repeticoes": 10,
    "dimensions": [4,4],
    "bateria": 40,
    "pontuacoes": []
}

for qtd in testes['qtdSujeira']:
    pontuacoes = []
    for rep in range(testes['repeticoes']):
        size = testes['dimensions'][0] * testes['dimensions'][1]
        
        amb = Ambiente(testes['dimensions'][0], testes['dimensions'][1], size, qtd)
        asp = Aspirador(testes['bateria'])

        while amb.pontos > -10:
            status = asp.sensor_aspirador(amb)
            asp.acao_aspirador(amb, status)
            asp.movimentar_aspirador(amb)
        
        penalizarAspirador(amb)
        pontuacoes.append(amb.pontos)
    testes['pontuacoes'].append(pontuacoes)

processData(testes)