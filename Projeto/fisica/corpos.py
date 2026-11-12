import numpy as np
from fisica.config import MI, RAIO_PLANETA, POSICAO_PLANETA, velocidade_orbital

# dicionario de planetas, usando sua posicao inicial, raio e a constante mi, baseado nas constantes do arquivo, config.py

planeta = {
    "posicao": POSICAO_PLANETA,
    "raio": RAIO_PLANETA,
    "mi": MI,
}

# dicionario de foguete, usando sua posicao inicial, velocidade, angulo e combustivel utilizado

foguete = {
    "posicao": np.array([100.0 , 0.0]),
    "velocidade": np.array([0.0, velocidade_orbital(planeta["mi"], 100)]),
    "angulo": 0.0,
    "combustivel": 100.0,
}

if __name__ == "__main__":
    print(planeta["raio"])
    print(foguete["posicao"])
    print(foguete["velocidade"])