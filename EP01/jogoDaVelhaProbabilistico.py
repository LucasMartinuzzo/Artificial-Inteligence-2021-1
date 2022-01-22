# -*- coding: utf-8 -*-
"""
Aluno: Lucas Martinuzzo Batista
NUSP: 11930158

Jogo da Velha
"""

import numpy as np
import time

jogadorIA = "x"
jogadorHumano = "o"
probabilidadeJogar = 0.5

# Gera um número aleatório de 0 a 99, de 0 a 49 simula Cara e pula o turno,
# de 50 a 99 simula Coroa e mantem o turno.
def humanoJoga():
    print('Uma moeda será lançada, se der Cara o jogador joga, se der coroa o computador joga.')
    time.sleep(0.5)
    randNum = np.random.randint(100,size=1)[0]
    print(randNum)
    deuCara = randNum > 50
    if(deuCara):
        print("Resultado: Cara, o jogador fará a próxima jogada!")
    else:
        print("Resultado: Coroa, o computador fará a próxima jogada!.")
    return deuCara

def desenhaCampo(campo):
    print("=================================")
    print("{} | {} | {}".format(campo[0],campo[1],campo[2]))
    print("----------")
    print("{} | {} | {}".format(campo[3],campo[4],campo[5]))
    print("----------")
    print("{} | {} | {}".format(campo[6],campo[7],campo[8]))
    print("=================================")
    return

def entradaJogador(campo):
    fraseEntrada = "Entre com o número correspondente ao espaço que deseje " +\
                    "preencher ou 0 caso deseje encerrar o programa: "
    while(True):
        try:
            print()
            x = int(input(fraseEntrada))
            if(x == 0 or x == 10):
                return x
            if(x < 0 or x > 10):
                print("\nERRO: Número inválido. Entre com uma posição válida");
            elif(campo[x-1] != x):
                print("\nEsta posição já está ocupada, tente novamente.")
                desenhaCampo(campo)
            else:
                return x
        except:
            print("\nERRO: Entrada inválida. Entre com uma posição válida");


def verificaJogadorVenceu(campo,jogador):
    if((campo[0] == jogador and campo[1] == jogador and campo[2] == jogador) or
       (campo[0] == jogador and campo[3] == jogador and campo[6] == jogador) or
       (campo[0] == jogador and campo[4] == jogador and campo[8] == jogador) or
       (campo[3] == jogador and campo[4] == jogador and campo[5] == jogador) or
       (campo[6] == jogador and campo[7] == jogador and campo[8] == jogador) or
       (campo[1] == jogador and campo[4] == jogador and campo[7] == jogador) or
       (campo[2] == jogador and campo[5] == jogador and campo[8] == jogador) or
       (campo[2] == jogador and campo[4] == jogador and campo[6] == jogador)):
        return True
    return False

def pontuaJogada(campo):
    if(verificaJogadorVenceu(campo,jogadorIA)):
        return 1
    if(verificaJogadorVenceu(campo,jogadorHumano)):
        return -1
    return 0
    
    
def testaJogadas(campo,jogadasRestantes, jogadorAtual):
    pontuacao = pontuaJogada(campo)
    nJogadas = len(jogadasRestantes)
    if((nJogadas == 0) or pontuacao != 0):
        return [pontuaJogada(campo),nJogadas]
    
    if(jogadorAtual == jogadorIA):
        pontuacoes = [[-np.Inf,9] for i in range(9)]
    else:
        pontuacoes = [[np.Inf,9] for i in range(9)]
    for jogada in jogadasRestantes:
        indiceJogada = jogada - 1
        campoTemp = campo.copy()
        jogadasTemp = jogadasRestantes.copy()
        campoTemp[indiceJogada] = jogadorAtual
        jogadasTemp.remove(jogada)
        if(jogadorAtual == jogadorIA):
            pontuacoes[indiceJogada] = testaJogadas(campoTemp, jogadasTemp,
                  jogadorHumano)
        else:
            pontuacoes[indiceJogada] = testaJogadas(campoTemp, jogadasTemp,
                  jogadorIA)
    #print(jogadorAtual,jogadasFeitas, pontuacoes)
    #desenhaCampo(campo)
    #if(jogadasFeitas == [1,2]):
    #    x = input()
    if(jogadorAtual == jogadorIA):
        jogadas = -1
        pontoMaximo = -1
        for pontuacao in pontuacoes:
            if(pontuacao[0] >= pontoMaximo and pontuacao[1] > jogadas):
                pontoMaximo = pontuacao[0]
                jogadas = pontuacao[1]
        return [pontoMaximo,jogadas]
    else:
        jogadas = -1
        pontoMinimo = 1
        for pontuacao in pontuacoes:
            if(pontuacao[0] <= pontoMinimo and pontuacao[1] > jogadas):
                pontoMinimo = pontuacao[0]
                jogadas = pontuacao[1]
        return [pontoMinimo,jogadas]
        

def jogadaIA(campo,jogadasRestantes,jogadorAtual = jogadorIA):
    pontuacoes = [[-np.Inf,9] for i in range(9)]
    for jogada in jogadasRestantes:
        indiceJogada = jogada - 1
        campoTemp = campo.copy()
        jogadasTemp = jogadasRestantes.copy()
        campoTemp[indiceJogada] = jogadorAtual
        jogadasTemp.remove(jogada)
        pontuacoes[indiceJogada] = testaJogadas(campoTemp, jogadasTemp,
                  jogadorHumano)
    print('pontuacoes: ', pontuacoes)
    indiceJogada = 0
    indiceTemp = 0
    jogadas = 9
    pontoMaximo = -1
    for pontuacao in pontuacoes:
        indiceTemp
        if(pontuacao[0] >= pontoMaximo and pontuacao[1] < jogadas):
            pontoMaximo = pontuacao[0]
            jogadas = pontuacao[1]
            indiceJogada = indiceTemp
        indiceTemp +=1
    return indiceJogada, indiceJogada+1
    
    

def main():
    print("Olá, Vamos brincar de Jogo da Velha!")
    print("Você jogará com o símbolo 'o', o computador será 'x'.")
    print("Campo:")
    campo = [1,2,3,4,5,6,7,8,9]
    jogadasValidas = [1,2,3,4,5,6,7,8,9]
    desenhaCampo(campo)
    while(True):
        if(humanoJoga()):
            x = entradaJogador(campo)
            if(x == 0):
                print("O programa será encerrado.")
                return 0
            if(x != 10):
                indiceJogada = x-1
                campo[indiceJogada] = jogadorHumano
                #print(jogadasValidas)
                jogadasValidas.remove(x)
                #print('jogadas válidas:', jogadasValidas)
                desenhaCampo(campo)
                if(verificaJogadorVenceu(campo,jogadorHumano)):
                    print("Fim de jogo. Você venceu, parabéns!")
                    return 0
                elif(len(jogadasValidas) == 0):
                    print("Fim de jogo. Você empatou!")
                    return 0
        else:
            print("Você perdeu a vez :(\n")
            indiceJogada, jogada = jogadaIA(campo,jogadasValidas)
            campo[indiceJogada] = jogadorIA
            jogadasValidas.remove(jogada)
            print("\nO computador fará a jogada dele:")
            time.sleep(1.5)
            desenhaCampo(campo)
            if(verificaJogadorVenceu(campo,jogadorIA)):
                print("Fim de jogo. Você perdeu :(")
                return 0
            elif(len(jogadasValidas) == 0):
                print("Fim de jogo. Você empatou!")
                return 0
    return 0

main()