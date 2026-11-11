import numpy as np

# medida em mm3/S2

MI = 394800

# medida em mm

RAIO_PLANETA = 30

# medida em mm

POSICAO_PLANETA = (0,0,0,0)

# medida em seg

DELTA_T = 0.01

# medida em mm

LARGURA_CAIXA = 20 

# medida em mm

ALTURA_CAIXA = 10

# calcula velocidade do fogute na orbita v = √(μ / r) 

def velocidade_orbital(MI, r):
    return np.sqrt (MI / r)

if __name__ == "__main__":
    print("%.2f" % velocidade_orbital(MI, 100))