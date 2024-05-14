import random as rd
import numpy as np

# Classe para guardar e trabalhar com os dados do ambiente
class Ambiente:
    # Metódo de inicialização do Ambiente
    def __init__(self, l, c, size, qtdSuj):
        # Cria o mapa totalmente limpo, l é o número de linhas e c é o número de colunas
        mapa = [['L' for i in range(c)] for j in range(l)]

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

    # Método para printar o mapa com aspirador(#) 
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

    # Método para limpar o quadrado onde o aspirador está
    def limpar_posicao(self):
        self.mapa[self.posicao[0]][self.posicao[1]] = 'L'

    # Método para atualizar a pontuação
    def atualizar_pontuacao(self, acao):
        # Se acao for L, o aspirador limpou um lugar sujo
        if acao == 'L':
            self.pontos += 3
        # Se acao for M, o aspirador se movimentou
        elif acao == 'M':
            self.pontos -= 1

    # Método para atualizar a posição do aspirador
    def atualizar_posicao(self, x, y):
        self.posicao[0] = x
        self.posicao[1] = y

# Classe para guardar dados e trabalhar com o aspirador
class Aspirador:
    # Método de inicialização do Aspirador
    def __init__(self, bateria):
        # Guarda os últimos três movimentos do aspirador
        self.memoria = [[], [], []]

        # Guarda todas as direções de movimentação possíveis do aspirador
        self.direcoes = ['U', 'D', 'L', 'R']

        # Guarda para qual direção o aspirador têm que seguir
        self.direcao = ''

        # Guarda quanta bateria o aspirador possui
        self.bateria = bateria

    # Método para o aspirador ver se o quadrado está sujo
    def sensor_aspirador(self, amb):
        # Retorna Sujo se o quadrado está sujo
        if amb.mapa[amb.posicao[0]][amb.posicao[1]] == 'S':
            return 'Sujo'
        # Retorna Limpo se o quadrado não está sujo
        else:
            return 'Limpo'
    
    # Método para definir fazer ação do aspirador
    def acao_aspirador(self, amb, status):
        # Se o status for Sujo, o aspirador limpa o quadrado
        if status == 'Sujo':
            amb.limpar_posicao()
            amb.atualizar_pontuacao('L')

    # Método para atualizar os dados do aspirador e do ambiente
    def atualizar_dados(self, amb, direcao, status):
        # Guarda o movimento feito pelo aspirador junto com o status do movimento, B se foi bloqueado ou L se foi livre
        movimento = [direcao, status]

        # Remove a primeira posição da memória
        self.memoria.pop(0)
        
        # Adiciona o último movimento na memória
        self.memoria.append(movimento)

        # Atualiza a pontuação do ambiente
        amb.atualizar_pontuacao('M')

        # Atualiza a bateria do aspirado, cada movimento remove 1
        self.bateria -= 1

    # Método para retornar o inverso de uma direção
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

    # Método para mover o aspirador
    def mover_aspirador(self, amb , direcao):
        # Pega os dados da posição atual do aspirador
        x = amb.posicao[0]
        y = amb.posicao[1]

        # Verifica a direção que o aspirador está indo
        match direcao:
            case 'U':
                x -= 1
            case 'D':
                x += 1
            case 'L':
                y -= 1
            case 'R':
                y += 1
        
        # Verifica se o aspirador pode fazer o movimento, senão poder retona B
        if x == len(amb.mapa) or x < 0 or y == len(amb.mapa[0]) or y < 0:
            return 'B'
        # Se poder retona L
        else:
            # Atualiza a posição do aspirador
            amb.atualizar_posicao(x,y)
            return 'L'
    
    # Método para decidir o movimento do aspirador
    def movimentar_aspirador(self, amb):
        # Guarda uma cópia da memória
        memoria = list(x for x in self.memoria if x)
        
        # Guarda uma cópia das possíveis direções
        direcoes = list(self.direcoes)

        # Guarda uma cópia o último movimento se ele existir
        anterior = memoria[-1] if memoria else []

        # Serve para guardar a direcao do último movimento
        temp_anterior = ''

        # Se anteiror existir tira o reverso do da direcao do anterior da lista de direções
        if anterior:
            temp_anterior = self.get_reverse(anterior[0])
            direcoes.remove(temp_anterior)
        # Senão existir anterior sorteia uma direção
        else:
            self.direcao = rd.choice(direcoes)

        # Move o aspirador na direção guardada no aspirador
        status = self.mover_aspirador(amb, self.direcao)

        # Atualiza os dados depois do movimento
        self.atualizar_dados(amb, self.direcao, status)

        # Se o retorno do movimento for B o aspirador bateu em algum lugar
        if status == 'B':
            # Remove a direção do movimento que aspirador acabou de fazer
            direcoes.remove(self.direcao)

            # Inverte a direção do que o aspirador anda
            self.direcao = self.get_reverse(self.direcao)

            # Sorteia uma direção temporária para o aspirador movimentar
            temp_direcao = rd.choice(direcoes)

            # Move o aspirador na direção temporária sorteada
            status = self.mover_aspirador(amb, temp_direcao)
            self.atualizar_dados(amb, temp_direcao, status)

            # Se o retorno do movimento for B o aspirador bateu em um canto
            if status == 'B':
                direcoes.remove(temp_direcao)

                # Sorteia uma nova direção temporária para o aspirador movimentar
                temp_direcao = rd.choice(direcoes)

                # Seta para o aspirador mover nessa direção
                self.direcao = temp_direcao
                
                # Move o aspirador na direção temporária sorteada
                status = self.mover_aspirador(amb, self.direcao)
                self.atualizar_dados(amb, self.direcao, status)

                # Se o retorno do movimento for B o aspirador está num beco
                if status == 'B':
                    # Se ainda tiver direções para o aspirador movimentar tenta elas, ou seja, é o primeiro movimento do aspirador
                    if direcoes:
                        direcoes.remove(temp_direcao)

                        # Pega a última direção possível
                        temp_direcao = rd.choice(direcoes)
                        
                        # Move o aspirador na última direção possível
                        status = self.mover_aspirador(amb, temp_direcao)
                        self.atualizar_dados(amb, temp_direcao, status)

                        # Se o retorno fo B, o aspirador está preso, então ele se desliga
                        if status == 'B':
                            self.bateria = 0
                    # Senão tiver direções para o aspirador fazer, ele volta para o quadrado anterior, vai cair nessa condição se não for o primeiro movimento do aspirador
                    else:
                        # Move o aspirador para o quadrado anterior
                        status = self.mover_aspirador(amb, temp_anterior)
                        self.atualizar_dados(amb, temp_anterior, status)

                        # Se o retorno for B, o quadrado anterior ficou inácessível, então ele se desliga
                        if status == 'B':
                            self.bateria = 0

# Método para penalizar o aspirador por cada quadrado não limpado
def penalizarAspirador(amb, testes):
    for x in range(len(amb.mapa)):
        for y in range(len(amb.mapa[0])):
            if amb.mapa[x][y] == 'S': 
                amb.pontos += testes['penalizacao']

# Processa os dados coletados dos testes
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

# Guarda informações dos testes a serem feitos
testes = {
    "qtdSujeira": [16, 12, 8, 4],
    "repeticoes": 10,
    "dimensions": [4,4],
    "penalizacao": -20,
    "bateria": 40,
    "pontuacoes": []
}

# Para cada quantidade de sujeira
for qtd in testes['qtdSujeira']:
    # Guarada as pontuações de cada repetição
    pontuacoes = []

    # Para cada repetição
    for rep in range(testes['repeticoes']):
        # Calcula tamanho do mapa
        size = testes['dimensions'][0] * testes['dimensions'][1]
        
        # Inicializa o ambiente
        amb = Ambiente(testes['dimensions'][0], testes['dimensions'][1], size, qtd)
        
        # Inicializa o aspirador
        asp = Aspirador(testes['bateria'])

        # Enquanto o aspirador tiver bateria
        while asp.bateria > 0:
            # Verifica a posição do aspirador
            status = asp.sensor_aspirador(amb)

            # Faz a ação para a posição
            asp.acao_aspirador(amb, status)

            # Movimenta o aspirador
            asp.movimentar_aspirador(amb)
        
        # Penaliza o aspirador
        penalizarAspirador(amb, testes)

        # Guarda os dados desta repetição
        pontuacoes.append(amb.pontos)

    # Guarda os dados de todas as repetições
    testes['pontuacoes'].append(pontuacoes)

# Processa os dados dos testes
processData(testes)