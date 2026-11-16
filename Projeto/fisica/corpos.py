import numpy as np
from fisica.config import (GRAVIDADE_PLANETA, RAIO_PLANETA, POSICAO_PLANETA, 
                           MASSA_FOGUETE, FORCA_MAX, COMBUSTIVEL_MAX, 
                           CONSUMO_MAX, ANGULO_INICIAL, POSICAO_INICIAL,
                           TOLERANCIA_ALVO, velocidade_orbital)

# funcao que cria um dicionario de planetas, usando sua posicao inicial, raio 
# e a calcula a constante mi, baseado na constante gravidade que esta no arquivo, config.py

def cria_planeta(posicao, raio, gravidade):
    mi = gravidade * raio**2
    novo_planeta = {
        "posicao": posicao,
        "raio": raio,
        "mi": mi,
    }
    return novo_planeta

# funcao que cria um dicionario de foguete

def cria_foguete(posicao, velocidade):
    novo_foguete = {
        "posicao": np.array(posicao, dtype=float),
        "velocidade": np.array(velocidade, dtype=float),
        "angulo": ANGULO_INICIAL,
        "combustivel": COMBUSTIVEL_MAX,
        "massa": MASSA_FOGUETE,
        "forca_max": FORCA_MAX,
        "consumo_max": CONSUMO_MAX, 
    }
    return novo_foguete

# funcao que determina o ponto de chegada da nave, onde finaliza o trajeto

def cria_alvo(posicao):
    novo_alvo= {
        "posicao": np.array(posicao, dtype=float),
        "tolerancia": TOLERANCIA_ALVO,
    }
    return novo_alvo

# Variaveis / Chamadas

planeta = cria_planeta(POSICAO_PLANETA,RAIO_PLANETA, GRAVIDADE_PLANETA)
foguete = cria_foguete(POSICAO_INICIAL, velocidade=[0.0 , velocidade_orbital(planeta["mi"] , 100.0)])
alvo = cria_alvo([-100.0 , 0.0])

if __name__ == "__main__":
    print(foguete["posicao"])
    print(foguete["velocidade"])