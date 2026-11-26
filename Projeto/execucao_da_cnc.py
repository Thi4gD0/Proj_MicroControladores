import numpy as np
from time import sleep
from fisica.corpos import (planeta, cria_alvo, cria_foguete)
from fisica.config import (POSICAO_INICIAL, PASSOS_POR_ENVIO, ESPERA_INICIAL)
from fisica.simulacao import (valida_parametros, passo_simulacao)
from fisica.cnc import (inicia_conexao, posicao_para_cnc, 
                        cria_mensagem, envia_posicao, finaliza_conexao,
                        inicia_homing)


# funcao que executa a simulacao e envia a trajetoria do foguete para a CNC
# um ponto a cada PASSOS_POR_ENVIO passos, ate a partida terminar

def executa_na_cnc(foguete, planeta, alvo):
    erro = valida_parametros(foguete, planeta, alvo)
    if erro is not None:
        print("Parametro Invalido:", erro)
        return erro
    
    conexao = inicia_conexao()
    inicia_homing(conexao)
    sleep(5)
    primeiro_ponto = True

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

            if primeiro_ponto:
              sleep(ESPERA_INICIAL)
              primeiro_ponto = False

        if estado["evento"] in ("colisao", "fora_da_caixa", "alvo_atingido"):
            break

    coordenadas_cnc = posicao_para_cnc(estado["posicao"])
    if coordenadas_cnc is not None:
        envia_posicao(conexao , cria_mensagem(coordenadas_cnc))
    sleep(5)
    finaliza_conexao(conexao)
    return estado["evento"]

if __name__ == "__main__":
    cenarios = [
        ["orbita grande", [180.0 , 0.0], [0.0 , 46.83], [-180.0 , 0.0]],
        ["elipse longa", [0.0 , -60.0], [106.0 , 0.0], [0.0 , 340.0]],
        ["queda do canto", [150.0 , 350.0], [-10.0 , 0.0], [-150.0 , -350.0]],
        ["fuga lateral", [180.0 , -350.0], [0.0 , 40.0], [-150.0 , 300.0]],
        ["parametro invalido", [10.0 , 0.0], [0.0 , 0.0], [-100.0 , 0.0]],
    ]

    print("planeta na cnc:", posicao_para_cnc(planeta["posicao"]))

    for cenario in cenarios:
        nome = cenario[0]
        foguete = cria_foguete(cenario[1], cenario[2])
        alvo = cria_alvo(cenario[3])

        print("---", nome, "---")
        print("alvo na cnc:", posicao_para_cnc(alvo["posicao"]))
        input("Marque o alvo na mesa e aperte Enter")
        print("resultado:", executa_na_cnc(foguete, planeta, alvo))