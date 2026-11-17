import numpy as np
from fisica.corpos import planeta, foguete, alvo, cria_foguete
from fisica.config import DELTA_T, ALTURA_CAIXA, LARGURA_CAIXA

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

if __name__ == "__main__":
    print(valida_parametros(foguete, planeta, alvo))
    print(valida_parametros(cria_foguete([10.0 , 0.0] , [0.0 , 0.0]), planeta, alvo))
    print(valida_parametros(cria_foguete([500.0 , 0.0] , [0.0 , 0.0]), planeta, alvo))

    print(aceleracao_gravitacional(foguete, planeta))
    print(movimenta_foguete(foguete, planeta, DELTA_T))