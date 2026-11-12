import numpy as np
from fisica.corpos import planeta, foguete

def aceleracao_gravitacional(foguete, planeta):
    r = foguete["posicao"] - planeta["posicao"]
    modulo_de_r = np.linalg.norm(r)
    return -planeta["mi"] * r / modulo_de_r ** 3


if __name__ == "__main__":
    print(aceleracao_gravitacional(foguete, planeta))