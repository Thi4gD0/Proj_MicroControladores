import numpy as np
import matplotlib.pyplot as plt
import matplotlib as matpl
matpl.use("Agg")

from matplotlib.animation import FuncAnimation
from fisica.corpos import planeta, alvo, cria_foguete
from fisica.simulacao import passo_simulacao
from fisica.config import (POSICAO_INICIAL, ALTURA_CAIXA, LARGURA_CAIXA,
                           DELTA_T, PASSOS_POR_QUADROS)

rastro_x = []
rastro_y = []
contador_passo = 0
fim_de_jogo = False

foguete = cria_foguete(POSICAO_INICIAL, [0.0 , 62.83])
fig, ax = plt.subplots()

ax.set_xlim(-LARGURA_CAIXA / 2, LARGURA_CAIXA / 2)
ax.set_ylim(-ALTURA_CAIXA / 2, ALTURA_CAIXA / 2)
ax.set_aspect("equal")
ax.set_title("Simulador de orbita")

ax.add_patch(plt.Circle(planeta["posicao"], planeta["raio"], color="tab:blue"))
ax.add_patch(plt.Circle(alvo["posicao"], alvo["tolerancia"], color="tab:green", fill=False))

ponto_foguete, = ax.plot([] , [] , "ro")
linha_rastro, = ax.plot([] , [] , "r-" , linewidth=0.8)

texto_x = -LARGURA_CAIXA / 2 + 5
texto_y = ALTURA_CAIXA / 2 - 15
texto = ax.text(texto_x , texto_y , "")

def atualiza(quadro):
    global contador_passo , fim_de_jogo

    if fim_de_jogo:
        return ponto_foguete, linha_rastro, texto
    
    for passo in range(PASSOS_POR_QUADROS):
        if (contador_passo < 50):
            comando = {"angulo": np.pi / 2 , "acelerador": 1}
        else:
            comando = {"angulo": np.pi / 2 , "acelerador": 0}
        
        estado = passo_simulacao(foguete, planeta, alvo, comando)
        contador_passo += 1

        if estado["evento"] in ("colisao" , "fora_da_caixa" , "alvo_atingido"):
            fim_de_jogo = True
            break


    rastro_x.append(estado["posicao"][0])
    rastro_y.append(estado["posicao"][1])

    ponto_foguete.set_data([estado["posicao"][0]] , [estado["posicao"][1]])
    linha_rastro.set_data(rastro_x, rastro_y)
    texto.set_text("%.1f s | combustivel %.1f%% | %s" % (contador_passo * DELTA_T, estado["combustivel"], estado["evento"]))

    return ponto_foguete, linha_rastro, texto

animacao = FuncAnimation(fig, atualiza, frames=300, interval=50)
animacao.save("simulacao.gif", writer="pillow", fps=20)
print("GIF salvo: simulacao.gif")