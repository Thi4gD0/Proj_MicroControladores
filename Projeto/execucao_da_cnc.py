import numpy as np
from fisica.corpos import (planeta, alvo, cria_foguete)
from fisica.config import (POSICAO_INICIAL, PASSOS_POR_ENVIO)
from fisica.simulacao import (valida_parametros, passo_simulacao)
from fisica.cnc import (inicia_conexao, posicao_para_cnc, 
                        cria_mensagem, envia_posicao, finaliza_conexao)


# funcao que executa a simulacao e envia a trajetoria do foguete para a CNC
# um ponto a cada PASSOS_POR_ENVIO passos, ate a partida terminar

def executa_na_cnc(foguete, planeta, alvo):
    erro = valida_parametros(foguete, planeta, alvo)
    if erro is not None:
        print("Parametro Invalido:", erro)
        return erro
    
    conexao = inicia_conexao()

    for i in range(3000):
        comando = {"angulo": np.pi / 2 , "acelerador": 0}
        estado = passo_simulacao(foguete, planeta, alvo, comando)

        if (i + 1) % PASSOS_POR_ENVIO == 0:
            coordenadas_cnc = posicao_para_cnc(estado["posicao"])
            if coordenadas_cnc is None:
                break
            mensagem = cria_mensagem(coordenadas_cnc)
            if envia_posicao(conexao , mensagem) == False:
                break

        if estado["evento"] in ("colisao", "fora_da_caixa", "alvo_atingido"):
            break

    finaliza_conexao(conexao)
    return estado["evento"]

if __name__ == "__main__":
    foguete = cria_foguete(POSICAO_INICIAL, [0.0, 62.83])
    print(executa_na_cnc(foguete, planeta, alvo))
