# Projeto de Micro Controladores

# 🚀 Simulador de Órbita — Módulo de Simulação Física

> **Etapa atual:** Semana 3 — Integração inicial (entrega em 26/11)
> **Status:** 🟢 Semanas 1 e 2 concluídas · 🟢 Comunicação com a CNC pronta (modo de teste) · 🟡 Integração e teste real em andamento

Este módulo é o "cérebro físico" do simulador: ele calcula como o foguete se move sob a gravidade de um planeta e o empuxo do próprio motor, e envia a trajetória para a CNC, que move o foguete sobre a mesa. A física recebe os parâmetros escolhidos pelo usuário na interface gráfica e devolve, a cada passo, o estado do foguete.

O simulador é voltado para **crianças**, por isso algumas simplificações foram escolhidas de propósito (planetas fixos, combustível sem peso).

---

## 🎯 Objetivos

**Semana 1 — Protótipo funcional** ✅
- [x] Modelo físico, unidades, gravidade e atualização do movimento.
- [x] Validação da órbita circular.

**Semana 2 — Evolução do protótipo** ✅ (código)
- [x] Criação de planeta, foguete e alvo a partir de parâmetros, com validação.
- [x] Motor (giro, empuxo e combustível) e eventos.
- [x] Função `passo_simulacao` e animação no matplotlib.

**Semana 3 — Integração inicial**
- [x] Conversão das posições para as coordenadas da mesa da CNC.
- [x] Envio dos pontos pela Serial no formato `x;y;t`, com confirmação `ok` (modo de teste).
- [x] Função `executa_na_cnc`, pronta para ser chamada pela interface.
- [x] Dimensões reais da área útil da CNC (400 × 800 mm).
- [ ] Combinar o contrato de dados com a interface gráfica.
- [ ] Montar a caixa, testar o eletroímã e imprimir o foguete em 3D.
- [ ] Testar a trajetória na CNC real.
- [ ] Detectar o marcador ArUco da nave com OpenCV (pode passar para a Semana 4).

---

## 📐 Modelo físico

| Decisão | Escolha | Motivo |
|---|---|---|
| Dimensões | 2D (plano XY) | A mesa é vista de cima |
| Origem (0, 0) | Centro da caixa | Simplifica a física; a conversão para a CNC é feita no envio |
| Planetas | Fixos | São peças físicas paradas na caixa |
| Foguete | Ponto (sem tamanho) | Simplifica o cálculo sem perder o comportamento |
| Nave | Sempre a mesma | Massa, força, combustível e consumo são constantes |
| Combustível | Não tem peso | Funciona como uma barra de 100 a 0 L |

### Unidades

A simulação trabalha em **milímetros e segundos**. A força usa **milinewtons**, pois com massa em kg a conta `a = F / m` sai direto em mm/s² (1 mN = 1 kg·mm/s²).

| Grandeza | Unidade | Grandeza | Unidade |
|---|---|---|---|
| Distância | mm | Massa | kg |
| Tempo | s | Força | mN |
| Velocidade | mm/s | Combustível | L |
| Aceleração e gravidade | mm/s² | Consumo | L/s |
| μ (parâmetro gravitacional) | mm³/s² | Ângulo | rad |

### Gravidade e parâmetro gravitacional (μ)

A física usa **μ = G · M**. O usuário escolhe a **gravidade na superfície** (g), e a conversão é feita na criação do planeta: `μ = g · R²`.

O planeta padrão foi escolhido para que uma órbita de raio 100 mm leve 10 s:

```
μ ≈ 394.800 mm³/s²      g ≈ 438,67 mm/s²      v orbital ≈ 62,83 mm/s      v escape ≈ 88,8 mm/s
```

---

## 🧱 Estrutura

```
Projeto/
├── validacao.py          # validação da órbita circular
├── animacao.py           # animação da simulação no matplotlib (substitui a CNC nos testes)
├── simulacao_na_cnc.py   # executa a simulação e envia a trajetória para a CNC
└── fisica/
    ├── __init__.py
    ├── config.py         # constantes do modelo + velocidade_orbital()
    ├── corpos.py         # criação do planeta, do foguete e do alvo
    ├── simulacao.py      # gravidade, motor, validação, eventos e passo da simulação
    └── cnc.py            # conversão de coordenadas e comunicação Serial com a CNC
```

### `config.py` — constantes

| Grupo | Constante | Valor | Unidade |
|---|---|---|---|
| Planeta | `POSICAO_PLANETA` | (0.0, 0.0) | mm |
| | `RAIO_PLANETA` | 30.0 | mm |
| | `GRAVIDADE_PLANETA` | 438.67 | mm/s² |
| Simulação | `DELTA_T` | 0.01 | s |
| Caixa (área útil da CNC) | `LARGURA_CAIXA` (eixo x) | 400.0 | mm |
| | `ALTURA_CAIXA` (eixo y) | 800.0 | mm |
| Nave | `MASSA_FOGUETE` | 0.03 | kg |
| | `FORCA_MAX` | 0.3 | mN |
| | `COMBUSTIVEL_MAX` | 100.0 | L |
| | `CONSUMO_MAX` | 5.0 | L/s |
| | `VELOCIDADE_GIRO` | π/2 | rad/s |
| Lançamento | `POSICAO_INICIAL` / `ANGULO_INICIAL` | (100.0, 0.0) / 0.0 | mm / rad |
| Alvo | `TOLERANCIA_ALVO` | 10.0 | mm |
| Animação | `PASSOS_POR_QUADRO` | 10 | passos (0,1 s por quadro) |
| Comunicação | `PORTA_SERIAL` | provisória | — |
| | `BAUD_RATE` | a confirmar com o Arduino | bits/s |
| | `MODO_TESTE` | `True` | — |
| | `PASSOS_POR_ENVIO` | 10 | passos (0,1 s por ponto) |

`MODO_TESTE = True` imprime as mensagens no terminal em vez de enviá-las pela Serial, permitindo testar todo o fluxo sem o Arduino.

### `corpos.py` — criação dos corpos

| Função | Recebe | Devolve |
|---|---|---|
| `cria_planeta(posicao, raio, gravidade)` | Valores escolhidos pelo usuário | Planeta com `"posicao"`, `"raio"` e `"mi"` |
| `cria_foguete(posicao, velocidade)` | Condição de lançamento | Foguete com posição, velocidade, ângulo, combustível, massa, força e consumo |
| `cria_alvo(posicao)` | Ponto de chegada | Alvo com `"posicao"` e `"tolerancia"` |

### `simulacao.py` — regras da simulação

| Função | O que faz | Retorno |
|---|---|---|
| `aceleracao_gravitacional(foguete, planeta)` | Puxão da gravidade na posição atual | Vetor aceleração (mm/s²) |
| `aplica_comando(foguete, comando, dt)` | Atualiza o ângulo, gasta combustível e calcula o empuxo | Vetor aceleração do motor (mm/s²) |
| `movimenta_foguete(foguete, planeta, dt, comando=None)` | Avança um passo somando gravidade e motor | O foguete atualizado |
| `dentro_do_limite(posicao)` | Confere se a posição está dentro da caixa | `True` ou `False` |
| `valida_parametros(foguete, planeta, alvo)` | Recusa parâmetros impossíveis | Mensagem de erro ou `None` |
| `verifica_eventos(foguete, planeta, alvo)` | Identifica o que está acontecendo | Nome do evento |
| `passo_simulacao(foguete, planeta, alvo, comando=None)` | Passo completo: movimento + eventos | Estado do foguete |

### `cnc.py` — comunicação com a CNC

| Função | O que faz | Retorno |
|---|---|---|
| `posicao_para_cnc(posicao)` | Converte a posição da física (origem no centro) para a mesa (origem no canto) | Vetor em mm, ou `None` se estiver fora da caixa |
| `cria_mensagem(coordenadas, tempo)` | Monta o texto no formato combinado | `"x;y;t\n"` |
| `inicia_conexao()` | Abre a Serial e espera 2 s o Arduino reiniciar | A conexão, ou `None` em modo de teste |
| `envia_posicao(conexao, mensagem)` | Envia a mensagem e espera a confirmação | `True` se recebeu `ok`, senão `False` |
| `finaliza_conexao(conexao)` | Fecha a Serial | — |

### `simulacao_na_cnc.py` — execução na mesa

**`executa_na_cnc(foguete, planeta, alvo)`** valida os parâmetros, abre a conexão e roda a simulação. A cada `PASSOS_POR_ENVIO` passos (0,1 s), converte a posição, monta a mensagem e envia para a CNC. Para quando a partida termina, quando uma posição sairia da mesa ou quando o Arduino não confirma. Devolve o evento final, ou a mensagem de erro da validação.

---

## 🔌 Comunicação

### Com a interface

A interface chama **`passo_simulacao`** a cada quadro (ou **`executa_na_cnc`** para enviar a trajetória à mesa).

**Comando** (enviado pela interface):

| Chave | Valor | Significado |
|---|---|---|
| `"acelerador"` | 0 a 1 | Quanto o usuário acelera (0 = motor desligado) |
| `"angulo"` **ou** `"girar"` | rad **ou** −1, 0, +1 | Direção do bico escolhida diretamente, ou girando aos poucos |

**Estado** (devolvido pela física): `"posicao"`, `"velocidade"`, `"angulo"`, `"combustivel"` (%) e `"evento"` (`"voando"`, `"sem_combustivel"`, `"colisao"`, `"fora_da_caixa"` ou `"alvo_atingido"`).

### Com a CNC (Serial)

**Conversão de coordenadas:**

```
x_cnc = x + LARGURA_CAIXA / 2        y_cnc = y + ALTURA_CAIXA / 2
```

| Posição na física | Posição na mesa |
|---|---|
| (0, 0) — planeta | (200, 400) — centro da mesa |
| (100, 0) — lançamento | (300, 400) |
| (−100, 0) — alvo | (100, 400) |
| (500, 0) — fora da caixa | `None` (não é enviado) |

**Protocolo:**

| Item | Definição |
|---|---|
| Mensagem | `x;y;t\n` — posição na mesa (mm) e tempo (s), com 2 casas decimais. Ex.: `300.00;400.00;0.10` |
| Frequência | Um ponto a cada 0,1 s de simulação |
| Confirmação | O Arduino responde `ok` depois de executar o movimento; só então o próximo ponto é enviado |
| Segurança | Posições fora da mesa não são enviadas; sem `ok`, o envio é interrompido |

A sintaxe da Serial segue o padrão da disciplina (`from serial import Serial`, `write(texto.encode("UTF-8"))` e `readline().decode().strip()`).

---

## ⚙️ Como o movimento é calculado

```
a_gravidade = −μ · r / |r|³              r = posição do foguete − posição do planeta
a_motor     = (forca_max · acelerador / massa) · (cos θ, sen θ)
combustível = máx(0, combustível − consumo_max · acelerador · dt)

a = a_gravidade + a_motor
v = v + a · dt          (primeiro a velocidade)
x = x + v · dt          (depois a posição, com a velocidade nova — Euler semi-implícito)
```

---

## ✅ Validação

### Órbita circular (`validacao.py`)

Foguete em (100, 0) mm com velocidade (0; 62,83) mm/s, sem motor, durante 30 s (3 voltas):

| Tempo (s) | 3 | 6 | 9 | 12 | 15 | 18 | 21 | 24 | 27 | 30 |
|---|---|---|---|---|---|---|---|---|---|---|
| Distância (mm) | 99,70 | 100,19 | 100,18 | 99,70 | 100,01 | 100,30 | 99,82 | 99,82 | 100,30 | 100,00 |

A distância oscilou ±0,3% sem tendência: a órbita é estável.

### Testes das funções

| Arquivo | Testes | Resultado |
|---|---|---|
| `simulacao.py` | Validação, gravidade, motor, motor + gravidade e eventos | ✅ |
| `cnc.py` | Conversão de 5 posições (incluindo fora da mesa) e envio em modo de teste | ✅ |
| `simulacao_na_cnc.py` | Órbita sem motor enviada ponto a ponto até `alvo_atingido` (~5 s) | ✅ |

### Cenários na animação (`animacao.py`)

| GIF | Lançamento | Comando do motor | Eventos |
|---|---|---|---|
| `fases_colisao.gif` | combustível 15 L | Freio (bico contra a velocidade) | `voando` → `sem_combustivel` → `colisao` |
| `fora_da_caixa.gif` | tanque cheio | Para cima nos primeiros 2 s | `voando` → `fora_da_caixa` |
| `alvo_atingido.gif` | tanque cheio | Desligado | `voando` → `alvo_atingido` (~5 s) |

> Os GIFs foram gerados com a caixa provisória de 400 × 300 mm. Com a área real (400 × 800 mm), o cenário de saída da caixa demora mais; os GIFs devem ser gerados novamente.

---

## ▶️ Como executar

De dentro da pasta `Projeto`, com o ambiente ativado:

```bash
source ../.venv/bin/activate        # ativar o ambiente
pip install -r ../requirements.txt  # numpy, matplotlib, pillow e pyserial

python -m fisica.simulacao          # testes da física
python -m fisica.cnc                # testes da conversão e do envio
python validacao.py                 # validação da órbita circular
python animacao.py                  # gera o GIF da animação
python simulacao_na_cnc.py          # envia a trajetória (imprime, em modo de teste)
```

Arquivos dentro de `fisica/` usam `-m` e o nome com ponto (sem `.py`).

**Para usar a CNC real:** rodar no computador com o Arduino conectado (o Codespaces não acessa portas USB), definir a `PORTA_SERIAL` e o `BAUD_RATE` iguais aos do Arduino, e mudar `MODO_TESTE` para `False`.

---

## ⚠️ Limitações e pendências

- Apenas um planeta (vários planetas previstos para a Semana 4).
- Oscilação numérica de ~0,3% na distância da órbita, causada pelo passo de tempo.
- Comunicação com a CNC testada apenas em modo de teste; falta o teste com a máquina real.
- A confirmar com o colega da CNC: baud rate, canto da origem (0, 0) e momento da resposta `ok`.
- A massa do foguete é provisória até a peça impressa ser pesada.
- Parâmetros (gravidade, motor e combustível) ainda não calibrados para a área real de 400 × 800 mm (Semana 4).

---

## 📚 Referências

- Leis de Newton, Lei da Gravitação Universal e 3ª Lei de Kepler.
- NASA JPL — *Basics of Space Flight*.
- Documentação do NumPy, do Matplotlib e do PySerial.
- Material da disciplina ENG1419 (Serial no Arduino e PySerial).