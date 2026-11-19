import numpy as np
from fisica.corpos import planeta, foguete, alvo, cria_foguete
from fisica.config import (DELTA_T, ALTURA_CAIXA, LARGURA_CAIXA, 
                           VELOCIDADE_GIRO, POSICAO_INICIAL)

# calcula a aceleracao que a gravidade de um planeta gera no foguete e na posicao atual que ele esta

def aceleracao_gravitacional(foguete, planeta):
    r = foguete["posicao"] - planeta["posicao"]
    modulo_de_r = np.linalg.norm(r)
    return -planeta["mi"] * r / modulo_de_r ** 3

# calcula a movimentacao do foguete, com sua velocidade e posicao, de acordo com um planeta e variacao com o tempo

def movimenta_foguete(foguete, planeta, dt, comando=None):
    a = aceleracao_gravitacional(foguete, planeta)
    if (comando is not None):
        a = a + aplica_comando(foguete, comando, dt)
    foguete["velocidade"] = foguete["velocidade"] + a * dt
    foguete["posicao"] = foguete["posicao"] + foguete["velocidade"] * dt
    return foguete

# calcula a area limite usada na simulacao, baseada na altura e larrgura da caixa

def dentro_do_limite(posicao):
    x = posicao[0]
    y = posicao[1]
    metade_largura = LARGURA_CAIXA / 2
    metade_altura = ALTURA_CAIXA / 2
    return (-metade_largura <= x <= metade_largura) and (-metade_altura <= y <= metade_altura)

# analisa os parametros e verifica se os valores estao validos para os calculos

def valida_parametros(foguete, planeta, alvo):
    if (foguete["posicao"].shape != (2,)):
        return "A posicao do foguete precisa ter somente 2 valores (x,y)"

    if (foguete["velocidade"].shape != (2,)):
        return "A velocidade do foguete deve ter somente 2 valores"

    if (planeta["posicao"].shape != (2,)):
        return "A posicao do planeta deve ter somente 2 valores (x,y)"

    if (alvo["posicao"].shape != (2,)):
        return "A posicao do alvo deve ter somente 2 valores (x,y)"

    if (planeta["raio"] <= 0):
        return "O raio do planeta deve ser maior que 0"

    if (planeta["mi"] <= 0):
        return "A gravidade do planeta deve ser maior que 0"

    if not (dentro_do_limite(foguete["posicao"])):
        return "A posicao do foguete esta fora da area limite da caixa"

    if not (dentro_do_limite(planeta["posicao"])):
        return "A posicao do planeta esta fora da area limite da caixa"

    if not (dentro_do_limite(alvo["posicao"])):
        return "A posicao do alvo esta fora da area limite da caixa"

    if (np.linalg.norm(foguete["posicao"] - planeta["posicao"]) <= planeta["raio"]):
        return "O foguete nao pode comecar dentro do planeta"

    if (np.linalg.norm(alvo["posicao"] - planeta["posicao"]) <= planeta["raio"] + alvo["tolerancia"]):
        return "O alvo esta muito perto do planeta"
    
    return None

# aplica os comando vindos do usuario e calcula consumo de combustivel, potencia e angulo da nave

def aplica_comando(foguete, comando, dt):
    if "angulo" in comando:
        foguete["angulo"] = comando["angulo"]

    elif "girar" in comando:
        foguete["angulo"] = foguete["angulo"] + comando["girar"] * VELOCIDADE_GIRO * dt

    foguete["combustivel"] = max(0 , foguete["combustivel"] - foguete["consumo_max"] * comando["acelerador"] * dt)

    if foguete["combustivel"] > 0:
        intensidade = foguete["forca_max"] * comando["acelerador"]/foguete["massa"]
        direcao = np.array([np.cos(foguete["angulo"]) , np.sin(foguete["angulo"])])
        return intensidade * direcao
    return np.array([0.0 , 0.0])

# verifica o estado do foguete a cada passo: colisao, saida da caixa, alvo atingido ou sem combustivel

def verifica_eventos(foguete, planeta, alvo):
    distancia_planeta = np.linalg.norm(foguete["posicao"] - planeta["posicao"])
    distancia_alvo = np.linalg.norm(foguete["posicao"] - alvo["posicao"])

    if distancia_planeta <= planeta["raio"]:
        return "colisao"

    if not dentro_do_limite(foguete["posicao"]):
        return "fora_da_caixa"

    if distancia_alvo <= alvo["tolerancia"]:
        return "alvo_atingido"

    if foguete["combustivel"] == 0:
        return "sem_combustivel"

    return "voando"

if __name__ == "__main__":
    print(valida_parametros(foguete, planeta, alvo))
    print(valida_parametros(cria_foguete([10.0 , 0.0] , [0.0 , 0.0]), planeta, alvo))
    print(valida_parametros(cria_foguete([500.0 , 0.0] , [0.0 , 0.0]), planeta, alvo))

    foguete_teste = cria_foguete(POSICAO_INICIAL, [0.0, 0.0])
    print(aplica_comando(foguete_teste, {"girar": 0, "acelerador": 1}, DELTA_T))
    print(foguete_teste["combustivel"])

    f1 = cria_foguete(POSICAO_INICIAL, [0.0, 62.83])
    f2 = cria_foguete(POSICAO_INICIAL, [0.0, 62.83])
    movimenta_foguete(f1, planeta, DELTA_T)
    movimenta_foguete(f2, planeta, DELTA_T, {"angulo": np.pi / 2, "acelerador": 1})
    print(f1["velocidade"], f2["velocidade"], f2["combustivel"])

    print(aceleracao_gravitacional(foguete, planeta))
    print(movimenta_foguete(foguete, planeta, DELTA_T))

    print(verifica_eventos(cria_foguete(POSICAO_INICIAL, [0.0, 0.0]), planeta, alvo))
    print(verifica_eventos(cria_foguete([10.0, 0.0], [0.0, 0.0]), planeta, alvo))
    print(verifica_eventos(cria_foguete([500.0, 0.0], [0.0, 0.0]), planeta, alvo))
    print(verifica_eventos(cria_foguete(alvo["posicao"], [0.0, 0.0]), planeta, alvo))

    f = cria_foguete(POSICAO_INICIAL, [0.0, 0.0])
    f["combustivel"] = 0
    print(verifica_eventos(f, planeta, alvo))