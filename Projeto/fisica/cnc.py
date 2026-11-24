import numpy as np
from fisica.config import (LARGURA_CAIXA, ALTURA_CAIXA)
from fisica.simulacao import dentro_do_limite

def converte_para_cnc(posicao):
    if not dentro_do_limite(posicao):
        return None

    x_cnc = posicao[0] + LARGURA_CAIXA/2
    y_cnc = posicao[1] + ALTURA_CAIXA/2
    return np.array([x_cnc , y_cnc])

def cria_mensagem(posicao_cnc , tempo):
    x = posicao_cnc[0]
    y = posicao_cnc[1]
    return "%.2f;%.2f;%.2f\n" % (x, y, tempo)

if __name__ == "__main__":
    print(converte_para_cnc([0.0 , 0.0]))
    print(converte_para_cnc([100.0 , 0.0]))
    print(converte_para_cnc([-100.0 , 0.0]))
    print(converte_para_cnc([0.0 , 500.0]))
    print(converte_para_cnc([500.0 , 0.0]))

    print(repr(cria_mensagem(np.array([300.0 , 400.0]) , 0.1)))