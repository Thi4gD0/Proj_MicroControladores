import numpy as np

# medida em mm3/S2

MI = 394800

# medida em mm

RAIO_PLANETA = 30

# medida em mm

POSICAO_PLANETA = (0.0 , 0.0)

# medida em seg

DELTA_T = 0.01

# medida em mm

LARGURA_CAIXA = 20 

# medida em mm

ALTURA_CAIXA = 10

# calcula velocidade do fogute na orbita v = √(μ / r) 

def velocidade_orbital(mi, r):
    return np.sqrt (mi / r)

# printa os dados do arquivo, caso o mesmo tenha sido requisitado

if __name__ == "__main__":
    print("%.2f" % velocidade_orbital(mi, 100))