# Projeto de Micro Controladores
 
# 🚀 Simulador de Órbita — Módulo de Simulação Física
 
> **Etapa atual:** Semana 2 — Evolução do protótipo (entrega em 19/11)
> **Status:** 🟢 Semana 1 concluída · 🟢 Código da Semana 2 concluído · 🟡 Montagem física em andamento
 
Este módulo é o "cérebro físico" do simulador: ele calcula como o foguete se move sob a gravidade de um planeta e o empuxo do próprio motor. A física recebe os parâmetros escolhidos pelo usuário na interface gráfica e devolve, a cada passo, o estado do foguete. Enquanto a CNC não está disponível, o movimento é visualizado por uma animação no matplotlib.
 
O simulador é voltado para **crianças**, por isso algumas simplificações foram escolhidas de propósito (planetas fixos, combustível sem peso).
 
---
 
## 🎯 Objetivos
 
**Semana 1 — Protótipo funcional** ✅
- [x] Definir o modelo físico e as unidades.
- [x] Representar o planeta e o foguete como dicionários.
- [x] Implementar a gravidade e a atualização do movimento.
- [x] Validar que uma órbita circular se mantém estável.
**Semana 2 — Evolução do protótipo**
- [x] Criar planeta, foguete e alvo a partir de parâmetros.
- [x] Validar os parâmetros recebidos.
- [x] Implementar o motor (giro, empuxo e consumo de combustível).
- [x] Detectar eventos (colisão, saída da caixa, alvo atingido, sem combustível).
- [x] Reunir tudo na função `passo_simulacao`, chamada pela interface.
- [x] Simular visualmente no matplotlib, substituindo a CNC nos testes.
- [ ] Montar a caixa, testar o eletroímã e imprimir o foguete em 3D.
- [ ] Combinar o formato dos dados com a interface gráfica.
---
 
## 📐 Modelo físico
 
| Decisão | Escolha | Motivo |
|---|---|---|
| Dimensões | 2D (plano XY) | A caixa é vista de cima, igual à CNC |
| Origem (0, 0) | Centro da caixa | Simplifica a física; a conversão para a CNC é feita na integração |
| Planetas | Fixos | São peças físicas paradas dentro da caixa |
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
 
A física usa **μ = G · M**, pois G e M sempre aparecem multiplicados. O usuário escolhe a **gravidade na superfície** (g), mais intuitiva, e a conversão é feita na criação do planeta:
 
```
μ = g · R²
```
 
O planeta padrão foi escolhido para que uma órbita de raio 100 mm leve 10 s:
 
```
μ = 4π² · r³ / T² ≈ 394.800 mm³/s²        g = μ / R² ≈ 438,67 mm/s²
v orbital = √(μ / r) ≈ 62,83 mm/s          v escape = √2 · v orbital ≈ 88,8 mm/s
```
 
---
 
## 🧱 Estrutura
 
```
Projeto/
├── validacao.py          # validação da órbita circular (Semana 1)
├── animacao.py           # animação da simulação no matplotlib
└── fisica/
    ├── __init__.py
    ├── config.py         # constantes do modelo + velocidade_orbital()
    ├── corpos.py         # criação do planeta, do foguete e do alvo
    └── simulacao.py      # gravidade, motor, validação, eventos e passo da simulação
```
 
### `config.py` — constantes
 
| Grupo | Constante | Valor | Unidade |
|---|---|---|---|
| Planeta | `POSICAO_PLANETA` | (0.0, 0.0) | mm |
| | `RAIO_PLANETA` | 30.0 | mm |
| | `GRAVIDADE_PLANETA` | 438.67 | mm/s² |
| Simulação | `DELTA_T` | 0.01 | s |
| Caixa | `LARGURA_CAIXA` / `ALTURA_CAIXA` | 400.0 / 300.0 (provisórios) | mm |
| Nave | `MASSA_FOGUETE` | 0.03 | kg |
| | `FORCA_MAX` | 0.3 | mN |
| | `COMBUSTIVEL_MAX` | 100.0 | L |
| | `CONSUMO_MAX` | 5.0 | L/s |
| | `VELOCIDADE_GIRO` | π/2 | rad/s |
| Lançamento | `POSICAO_INICIAL` | (100.0, 0.0) | mm |
| | `ANGULO_INICIAL` | 0.0 | rad |
| Alvo | `TOLERANCIA_ALVO` | 10.0 | mm |
| Animação | `PASSOS_POR_QUADRO` | 10 | passos (0,1 s por quadro) |
 
Com esses valores, o motor acelera **10 mm/s²** (≈ ¼ da gravidade na órbita) e o tanque dura **20 s** em potência total.
 
### `corpos.py` — criação dos corpos
 
| Função | Recebe | Devolve |
|---|---|---|
| `cria_planeta(posicao, raio, gravidade)` | Valores escolhidos pelo usuário | Planeta com `"posicao"`, `"raio"` e `"mi"` (calculado por `g · R²`) |
| `cria_foguete(posicao, velocidade)` | Condição de lançamento | Foguete com `"posicao"`, `"velocidade"`, `"angulo"`, `"combustivel"`, `"massa"`, `"forca_max"` e `"consumo_max"` |
| `cria_alvo(posicao)` | Ponto de chegada escolhido | Alvo com `"posicao"` e `"tolerancia"` |
 
As posições e velocidades são convertidas com `np.array(..., dtype=float)`, garantindo vetores numpy mesmo que a interface envie listas. O arquivo também cria um planeta, um foguete e um alvo **de exemplo**, usados nos testes.
 
### `simulacao.py` — regras da simulação
 
| Função | O que faz | Retorno |
|---|---|---|
| `aceleracao_gravitacional(foguete, planeta)` | Puxão da gravidade na posição atual do foguete | Vetor aceleração (mm/s²) |
| `aplica_comando(foguete, comando, dt)` | Atualiza o ângulo, gasta combustível e calcula o empuxo do motor | Vetor aceleração do motor (mm/s²) |
| `movimenta_foguete(foguete, planeta, dt, comando=None)` | Avança um passo somando gravidade e motor | O foguete atualizado |
| `dentro_do_limite(posicao)` | Confere se a posição está dentro da caixa | `True` ou `False` |
| `valida_parametros(foguete, planeta, alvo)` | Recusa parâmetros impossíveis antes do lançamento | Mensagem de erro ou `None` |
| `verifica_eventos(foguete, planeta, alvo)` | Identifica o que está acontecendo com o foguete | Nome do evento |
| `passo_simulacao(foguete, planeta, alvo, comando=None)` | Executa um passo completo: movimento + eventos | Estado do foguete |
 
**Validações** feitas por `valida_parametros`: vetores com 2 valores; raio e gravidade positivos; foguete, planeta e alvo dentro da caixa; foguete fora do planeta; alvo a mais de `raio + tolerância` do planeta.
 
---
 
## 🔌 Contrato com a interface
 
A interface chama apenas **`passo_simulacao`**, a cada quadro.
 
**Comando** (enviado pela interface):
 
| Chave | Valor | Significado |
|---|---|---|
| `"acelerador"` | 0 a 1 | Quanto o usuário acelera (0 = motor desligado) |
| `"angulo"` **ou** `"girar"` | rad **ou** −1, 0, +1 | Direção do bico escolhida diretamente, ou girando aos poucos |
 
Exemplo: `{"angulo": 1.57, "acelerador": 1}`
 
**Estado** (devolvido pela física):
 
| Chave | Conteúdo |
|---|---|
| `"posicao"` | Posição do foguete (mm) |
| `"velocidade"` | Velocidade do foguete (mm/s) |
| `"angulo"` | Direção do bico (rad) |
| `"combustivel"` | Combustível restante (%) |
| `"evento"` | `"voando"`, `"sem_combustivel"`, `"colisao"`, `"fora_da_caixa"` ou `"alvo_atingido"` |
 
Os eventos `colisao`, `fora_da_caixa` e `alvo_atingido` **encerram** a partida. Em `sem_combustivel`, o foguete continua voando só com a gravidade.
 
---
 
## ⚙️ Como o movimento é calculado
 
**1. Gravidade**
 
```
a_gravidade = −μ · r / |r|³        onde  r = posição do foguete − posição do planeta
```
 
`r / |r|` dá a direção, `μ / |r|²` dá a intensidade, e o sinal negativo faz a força puxar o foguete para o planeta.
 
**2. Motor**
 
```
ângulo              = comando["angulo"]   ou   ângulo + girar · VELOCIDADE_GIRO · dt
combustível         = máx(0, combustível − consumo_max · acelerador · dt)
a_motor             = (forca_max · acelerador / massa) · (cos θ, sen θ)
```
 
Sem combustível, `a_motor = (0, 0)`.
 
**3. Atualização a cada passo (Euler semi-implícito)**
 
```
a = a_gravidade + a_motor
v = v + a · dt          (primeiro a velocidade)
x = x + v · dt          (depois a posição, com a velocidade nova)
```
 
Essa ordem mantém a órbita estável; na ordem inversa, a órbita abriria em espiral a cada volta.
 
---
 
## ✅ Validação
 
### Órbita circular (`validacao.py`)
 
Foguete em (100, 0) mm com velocidade (0; 62,83) mm/s, sem motor, durante 30 s (3 voltas):
 
| Tempo (s) | 3 | 6 | 9 | 12 | 15 | 18 | 21 | 24 | 27 | 30 |
|---|---|---|---|---|---|---|---|---|---|---|
| Distância (mm) | 99,70 | 100,19 | 100,18 | 99,70 | 100,01 | 100,30 | 99,82 | 99,82 | 100,30 | 100,00 |
 
**Resultado:** a distância oscilou entre 99,70 e 100,30 mm (±0,3%), sem tendência de crescer ou diminuir. A órbita é estável. A pequena oscilação vem do passo de tempo de 0,01 s e é menor que a precisão da CNC.
 
### Testes das funções (`python -m fisica.simulacao`)
 
| Teste | Esperado | Obtido |
|---|---|---|
| Parâmetros de exemplo | `None` | ✅ |
| Foguete dentro do planeta | erro | ✅ |
| Foguete fora da caixa | erro | ✅ |
| Gravidade em (100, 0) | (−39,48; 0) mm/s² | ✅ |
| Motor com ângulo 0 e acelerador 1 | (10; 0) mm/s² e combustível 99,95 L | ✅ |
| Motor + gravidade (motor para cima) | velocidade y de 62,83 → 62,93 mm/s | ✅ |
| Eventos | `voando`, `colisao`, `fora_da_caixa`, `alvo_atingido`, `sem_combustivel` | ✅ |
 
### Cenários na animação (`animacao.py`)
 
| GIF | Lançamento | Comando do motor | Sequência de eventos |
|---|---|---|---|
| `fases_colisao.gif` | (0; 62,83) mm/s, combustível 15 L | Freio: bico sempre contra a velocidade, acelerador 1 | `voando` → `sem_combustivel` → `colisao` |
| `fora_da_caixa.gif` | (0; 62,83) mm/s, tanque cheio | Para cima nos primeiros 2 s | `voando` → `fora_da_caixa` (~3,5 s) |
| `alvo_atingido.gif` | (0; 62,83) mm/s, tanque cheio | Desligado | `voando` → `alvo_atingido` (~5 s, meia volta) |
 
---
 
## 🎬 Animação no matplotlib
 
O `animacao.py` substitui a CNC nos testes: desenha a caixa (limites do gráfico), o planeta, a zona do alvo, o foguete e o rastro, e mostra o tempo, o combustível e o evento.
 
- A função **`atualiza`** é chamada a cada quadro: avança a física `PASSOS_POR_QUADRO` vezes (0,1 s) e redesenha o foguete.
- A variável **`fim_de_jogo`** congela a animação quando um evento final acontece.
- Como o Codespaces não abre janelas, o matplotlib roda no modo `"Agg"` e a animação é salva como **GIF**.
- A animação usa os mesmos dados que irão para a CNC (posição em mm e tempo): na integração, o desenho é substituído pelo envio pela Serial.
---
 
## ▶️ Como executar
 
O ambiente roda no GitHub Codespaces (Linux). Execute de dentro da pasta `Projeto`, com o ambiente ativado:
 
```bash
source ../.venv/bin/activate        # ativar o ambiente
pip install -r ../requirements.txt  # numpy, matplotlib e pillow
 
python -m fisica.simulacao          # testes das funções
python validacao.py                 # validação da órbita circular
python animacao.py                  # gera o GIF da animação
```
 
Arquivos dentro de `fisica/` usam `-m` e o nome com ponto (sem `.py`), pois importam uns aos outros como pacote.
 
---
 
## ⚠️ Limitações
 
- Apenas um planeta (o suporte a vários planetas está previsto para a Semana 3).
- Oscilação numérica de ~0,3% na distância da órbita, causada pelo passo de tempo.
- Dimensões da caixa e massa do foguete ainda provisórias.
- Com a caixa de 400 × 300 mm, poucos segundos de motor já tiram o foguete da área; a calibração está prevista para a Semana 4.
- Sem integração com a interface e a CNC (Semana 3).
---
 
## 📚 Referências
 
- Leis de Newton e Lei da Gravitação Universal.
- 3ª Lei de Kepler (relação entre período e raio da órbita).
- NASA JPL — *Basics of Space Flight*.
- Documentação do NumPy e do Matplotlib.
 