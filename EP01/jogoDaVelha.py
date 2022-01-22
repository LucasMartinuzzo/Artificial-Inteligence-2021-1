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
            if(x == 0):
                return 0
            if(x < 0 or x > 9):
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
    if((len(jogadasRestantes) == 0) or pontuacao != 0):
        return pontuaJogada(campo)
    
    if(jogadorAtual == jogadorIA):
        pontuacoes = [-np.Inf for i in range(9)]
    else:
        pontuacoes = [np.Inf for i in range(9)]
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
        return np.max(pontuacoes)
    else:
        return np.min(pontuacoes)
        

def jogadaIA(campo,jogadasRestantes,jogadorAtual = jogadorIA):
    pontuacoes = [-np.Inf for i in range(9)]
    for jogada in jogadasRestantes:
        indiceJogada = jogada - 1
        campoTemp = campo.copy()
        jogadasTemp = jogadasRestantes.copy()
        campoTemp[indiceJogada] = jogadorAtual
        jogadasTemp.remove(jogada)
        pontuacoes[indiceJogada] = testaJogadas(campoTemp, jogadasTemp,
                  jogadorHumano)
    #print('pontuacoes: ', pontuacoes)
    indiceJogada = np.argmax(pontuacoes)
    return indiceJogada, indiceJogada+1
    
    
        

def main():
    print("Olá, Vamos brincar de Jogo da Velha!")
    print("Você jogará com o símbolo 'o', o computador será 'x'.")
    x = input("Você deseja jogar primeiro (s/n)?: ")
    print("Campo:")
    campo = [1,2,3,4,5,6,7,8,9]
    jogadasValidas = [1,2,3,4,5,6,7,8,9]
    if(x != 's' and x != "S"):
        indiceJogada = np.random.randint(9,size=1)[0]
        jogada = indiceJogada+1
        campo[indiceJogada] = jogadorIA
        jogadasValidas.remove(jogada)
    desenhaCampo(campo)
    while(True):
        x = entradaJogador(campo)
        if(x == 0):
            print("O programa será encerrado.")
            return 0
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

main()