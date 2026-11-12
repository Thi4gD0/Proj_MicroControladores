import numpy as np
from fisica.corpos import planeta, foguete
from fisica.config import DELTA_T

# calcula a aceleracao que a gravidade de um planeta gera no foguete e na posicao atual que ele esta

def aceleracao_gravitacional(foguete, planeta):
    r = foguete["posicao"] - planeta["posicao"]
    modulo_de_r = np.linalg.norm(r)
    return -planeta["mi"] * r / modulo_de_r ** 3

# calcula a movimentacao do foguete, com sua velocidade e posicao, de acordo com um planeta e variacao com o tempo

def movimenta_foguete(foguete, planeta, dt):
    a = aceleracao_gravitacional(foguete, planeta)
    foguete["velocidade"] = foguete["velocidade"] + a * dt
    foguete["posicao"] = foguete["posicao"] + foguete["velocidade"] * dt
    return foguete


if __name__ == "__main__":
    print(aceleracao_gravitacional(foguete, planeta))
    print(movimenta_foguete(foguete, planeta, DELTA_T))