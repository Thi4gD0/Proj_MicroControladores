import numpy as np
from serial import Serial
from time import sleep
from fisica.simulacao import dentro_do_limite
from fisica.config import (LARGURA_CAIXA, ALTURA_CAIXA, PORTA_SERIAL,
                           BAUD_RATE, MODO_TESTE)

def posicao_para_cnc(posicao):
    if not dentro_do_limite(posicao):
        return None

    x_cnc = posicao[0] + LARGURA_CAIXA/2
    y_cnc = posicao[1] + ALTURA_CAIXA/2
    return np.array([x_cnc , y_cnc])

def cria_mensagem(posicao_cnc , tempo):
    x = posicao_cnc[0]
    y = posicao_cnc[1]
    return "%.2f;%.2f;%.2f\n" % (x, y, tempo)

def inicia_conexao():
    if MODO_TESTE == True:
        return None
    else:
        meu_serial = Serial(PORTA_SERIAL, baudrate=BAUD_RATE, timeout=2)
        sleep(2)
        return meu_serial

def envia_posicao(conexao, mensagem):
    if MODO_TESTE:
        print(mensagem)
        return True

    conexao.write(mensagem.encode("UTF-8"))
    result = conexao.readline().decode().strip()
    if result != "ok":
        print("Erro ao enviar coordenadas para cnc")
        return False
    return True

def finaliza_conexao(conexao):
    if conexao != None:
        conexao.close()

if __name__ == "__main__":
    print(posicao_para_cnc([0.0 , 0.0]))
    print(posicao_para_cnc([100.0 , 0.0]))
    print(posicao_para_cnc([-100.0 , 0.0]))
    print(posicao_para_cnc([0.0 , 500.0]))
    print(posicao_para_cnc([500.0 , 0.0]))

    print(repr(cria_mensagem(np.array([300.0 , 400.0]) , 0.1)))

    conexao = inicia_conexao()
    posicao_cnc = posicao_para_cnc([100.0 , 0.0])
    mensagem = cria_mensagem(posicao_cnc , 0.1)
    print(envia_posicao(conexao , mensagem))
    finaliza_conexao(conexao)