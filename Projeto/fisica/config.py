import numpy as np

# --PLANETA-- #
# medida em mm
RAIO_PLANETA = 30

# medida em mm
POSICAO_PLANETA = [0.0 , 0.0]

# medida em mm por segundo ao quadrado
GRAVIDADE_PLANETA = 438.67


# --simulacao-- #
# medida em seg
DELTA_T = 0.01


# --caixa-- #
# medida em mm
LARGURA_CAIXA = 400.0

# medida em mm
ALTURA_CAIXA = 300.0


# --Nave-- #
# medida em kg
MASSA_FOGUETE = 0.03

# medida em Litros por segundo
CONSUMO_MAX = 5.0

# medida em miliNewtowns
FORCA_MAX = 0.3

# medida em Litros
COMBUSTIVEL_MAX = 100.0

# medida em rad por segundo
VELOCIDADE_GIRO = np.pi / 2

# medida em rad
ANGULO_INICIAL = 0.0

# medida em mm
POSICAO_INICIAL = [100.0 , 0.0]

# medida em mm
TOLERANCIA_ALVO = 20.0


# calcula velocidade do fogute na orbita v = √(μ / r) 

def velocidade_orbital(mi, r):
    return np.sqrt (mi / r)

if __name__ == "__main__":
    novo_mi = GRAVIDADE_PLANETA * RAIO_PLANETA ** 2 
    print("%.2f" % velocidade_orbital(novo_mi, 100))