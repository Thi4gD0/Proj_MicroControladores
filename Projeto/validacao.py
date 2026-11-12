import numpy as np 
from fisica.corpos import planeta, foguete
from fisica.simulacao import movimenta_foguete
from fisica.config import DELTA_T

# for que mostra qual a distancia do foguete para um planeta em determinado instante, variando no momento de 3 em 3 segundos

for mov in range(3000):
    movimenta_foguete(foguete, planeta, DELTA_T)
    if (mov + 1) % 300 == 0:
        distancia = np.linalg.norm(foguete["posicao"] - planeta["posicao"])
        print("%.1f %.2f mm" % ((mov + 1) * DELTA_T, distancia))