# Projeto de Micro Controladores

# 🚀 Simulador de Órbita — Módulo de Simulação Física

> **Etapa atual:** Semana 2 — Evolução do protótipo (entrega em 19/11)
> **Status:** 🟢 Semana 1 concluída

Este módulo é o "cérebro físico" do simulador: ele calcula como o foguete se move sob a gravidade de um planeta. Na Semana 1, o objetivo foi ter um foguete orbitando um planeta de forma estável. Na Semana 2, a física passa a receber os parâmetros escolhidos pelo usuário na interface gráfica.

O simulador é voltado para **crianças**, por isso algumas simplificações foram escolhidas de propósito (planetas fixos, combustível sem peso).

---

## 🎯 Objetivos

**Semana 1 — Protótipo funcional** ✅
- [x] Definir o modelo físico e as unidades usadas no projeto.
- [x] Representar o planeta e o foguete como dicionários.
- [x] Implementar a gravidade e a atualização do movimento a cada passo de tempo.
- [x] Validar que uma órbita circular se mantém estável por várias voltas.

**Semana 2 — Evolução do protótipo**
- [x] Criar planeta e foguete a partir de parâmetros (`criar_planeta`, `criar_foguete`).
- [ ] Criar o alvo e validar os parâmetros recebidos (`criar_alvo`, `validar_parametros`).
- [ ] Implementar o motor (giro, empuxo e consumo de combustível).
- [ ] Detectar eventos (colisão, saída da caixa, alvo atingido, sem combustível).
- [ ] Reunir tudo na função `passo_simulacao`, chamada pela interface.
- [ ] Simular visualmente no matplotlib, substituindo a CNC nos testes.

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
| Atmosfera / atrito | Ignorados | Fora do escopo do projeto |

### Unidades

A simulação trabalha internamente em **milímetros e segundos**. A força usa **milinewtons**, pois com massa em kg a conta `a = F / m` sai direto em mm/s², sem conversão (1 mN = 1 kg·mm/s²).

| Grandeza | Unidade |
|---|---|
| Distância | mm |
| Tempo | s |
| Velocidade | mm/s |
| Aceleração e gravidade | mm/s² |
| μ (parâmetro gravitacional) | mm³/s² |
| Massa | kg |
| Força | mN |
| Combustível | L |
| Consumo | L/s |

### Gravidade e parâmetro gravitacional (μ)

A física usa o parâmetro **μ = G · M**, pois G e M sempre aparecem multiplicados na fórmula. Para o usuário, porém, é mais intuitivo escolher a **gravidade na superfície** (g). A conversão é feita pela `criar_planeta`:

```
g = μ / R²      →      μ = g · R²
```

O planeta padrão foi escolhido para que uma órbita de raio 100 mm leve 10 s:

```
μ = 4π² · r³ / T² = 4π² · 100³ / 10² ≈ 394.800 mm³/s²
g = μ / R² = 394.800 / 30² ≈ 438,67 mm/s²   (≈ 0,44 m/s²)
```

Velocidade para órbita circular a 100 mm:

```
v = √(μ / r) = √(394.800 / 100) ≈ 62,83 mm/s
```

---

## 🧱 Estrutura

```
Projeto/
├── validacao.py          # validação da órbita circular
└── fisica/
    ├── __init__.py       # marca a pasta como pacote Python
    ├── config.py         # constantes do modelo + velocidade_orbital()
    ├── corpos.py         # criação do planeta e do foguete
    └── simulation.py     # gravidade e atualização do movimento
```

### `config.py` — constantes

**Planeta padrão**
| Constante | Valor | Unidade |
|---|---|---|
| `POSICAO_PLANETA` | (0.0, 0.0) | mm |
| `RAIO_PLANETA` | 30.0 | mm |
| `GRAVIDADE_PLANETA` | 438.67 | mm/s² |

**Simulação e caixa**
| Constante | Valor | Unidade |
|---|---|---|
| `DELTA_T` | 0.01 | s |
| `LARGURA_CAIXA` / `ALTURA_CAIXA` | 400.0 / 300.0 (provisórios) | mm |

**Nave** (características fixas)
| Constante | Valor | Unidade | Efeito |
|---|---|---|---|
| `MASSA_FOGUETE` | 0.03 | kg | Massa de referência do foguete impresso |
| `FORCA_MAX` | 0.3 | mN | Motor acelera 10 mm/s² (≈ ¼ da gravidade na órbita) |
| `COMBUSTIVEL_MAX` | 100.0 | L | Tanque sempre cheio no início |
| `CONSUMO_MAX` | 5.0 | L/s | 20 s de motor em potência total |
| `VELOCIDADE_GIRO` | π/2 | rad/s | Uma volta do bico em 4 s |

**Lançamento padrão** (usado nos testes até a interface ficar pronta)
| Constante | Valor | Unidade |
|---|---|---|
| `POSICAO_INICIAL_PADRAO` | (100.0, 0.0) | mm |
| `ANGULO_INICIAL_PADRAO` | 0.0 | rad |

**Função `velocidade_orbital(mi, r)`** — devolve `√(mi / r)`, a velocidade para uma órbita circular de raio `r`.

> A força máxima acompanha a massa: `FORCA_MAX = MASSA_FOGUETE × 10` mantém o motor em 10 mm/s². Ao trocar a massa pelo peso real do foguete impresso, a força deve ser recalculada.

### `corpos.py` — criação dos corpos

| Função | Recebe | O que faz |
|---|---|---|
| `criar_planeta(posicao, raio, gravidade)` | Valores escolhidos pelo usuário | Calcula `mi = gravidade · raio²` e devolve o dicionário do planeta |
| `criar_foguete(posicao, velocidade, angulo)` | Condição de lançamento escolhida pelo usuário | Devolve o dicionário do foguete, completando massa, força, combustível e consumo com as constantes da nave |

As posições e velocidades são convertidas com `np.array(..., dtype=float)`, garantindo vetores numpy de decimais mesmo que a interface envie listas ou tuplas.

**Dicionário `planeta`**
| Chave | Unidade |
|---|---|
| `"posicao"` | mm |
| `"raio"` | mm |
| `"mi"` | mm³/s² |

**Dicionário `foguete`**
| Chave | Unidade | Origem |
|---|---|---|
| `"posicao"` | mm | parâmetro |
| `"velocidade"` | mm/s | parâmetro |
| `"angulo"` | rad | parâmetro |
| `"combustivel"` | L | `COMBUSTIVEL_MAX` (diminui durante o voo) |
| `"massa"` | kg | `MASSA_FOGUETE` |
| `"forca_max"` | mN | `FORCA_MAX` |
| `"consumo_max"` | L/s | `CONSUMO_MAX` |

O arquivo também cria um **planeta e um foguete de exemplo** com as constantes padrão, usados nos testes e no `validacao.py`.

### `simulation.py` — movimento

| Função | O que faz | Retorno |
|---|---|---|
| `aceleracao_gravitacional(foguete, planeta)` | Calcula o puxão da gravidade do planeta na posição atual do foguete | Vetor aceleração (mm/s²) |
| `movimenta_foguete(foguete, planeta, dt)` | Avança o foguete um passo `dt`: atualiza a velocidade e depois a posição | O dicionário `foguete` atualizado |

---

## ⚙️ Como o movimento é calculado

### 1. Gravidade

```
a = −μ · r / |r|³        onde   r = posição do foguete − posição do planeta
```

- `r / |r|` dá a **direção** (vetor unitário do planeta para o foguete).
- `μ / |r|²` dá a **intensidade** (a gravidade diminui com o quadrado da distância).
- O sinal **negativo** faz a aceleração apontar **para o planeta**.
- `|r|` é calculado com `np.linalg.norm(r)`.

**Verificação:** com o foguete em (100, 0), `a = (−39,48; 0) mm/s²`, apontando para o planeta.

### 2. Atualização a cada passo (Euler semi-implícito)

```
1.  v = v + a · dt      (primeiro a velocidade)
2.  x = x + v · dt      (depois a posição, usando a velocidade NOVA)
```

A ordem é importante: atualizar a posição com a velocidade antiga (Euler comum) faz a órbita abrir em espiral a cada volta. O método semi-implícito mantém a órbita estável.

**Verificação de um passo:** a velocidade vai de (0; 62,83) para (−0,3948; 62,83) mm/s, e a posição de (100; 0) para (99,996; 0,6283) mm — o início da curva.

### 3. Motor (Semana 2 — em desenvolvimento)

A força aplicada depende da potência escolhida pelo usuário (de 0 a 1) a cada instante:

```
força aplicada        = FORCA_MAX × potência
aceleração do motor   = força aplicada / massa                (mm/s²)
combustível gasto     = CONSUMO_MAX × potência × dt           (L)
```

Sem combustível, o motor deixa de empurrar e o foguete segue só com a gravidade. A aceleração total passa a ser **gravidade + motor**.

---

## ✅ Validação (Semana 1)

| Parâmetro | Valor |
|---|---|
| Planeta | (0, 0) mm, raio 30 mm, g = 438,67 mm/s² |
| Foguete | (100, 0) mm com velocidade (0; 62,83) mm/s |
| Duração | 30 s (3 voltas de 10 s, 3.000 passos) |
| Registro | Distância foguete–planeta a cada 3 s |

**Critério de sucesso:** a distância oscila em torno de 100 mm, sem tendência de crescer ou diminuir.

| Tempo (s) | 3 | 6 | 9 | 12 | 15 | 18 | 21 | 24 | 27 | 30 |
|---|---|---|---|---|---|---|---|---|---|---|
| Distância (mm) | 99,70 | | | | | | | | | |

_(preencher, ex.: "a distância variou entre 99,7 e 100,0 mm — órbita estável")_

**Por que a distância varia:** a simulação calcula em passos de 0,01 s, como desenhar um círculo com segmentos de reta curtos. Isso gera uma oscilação de ~0,3% em torno de 100 mm, que não aumenta com o tempo e é menor que a precisão da CNC.

---

## ▶️ Como executar

O ambiente roda no GitHub Codespaces (Linux). Com o ambiente virtual ativado, execute de dentro da pasta `Projeto`:

```bash
source .venv/bin/activate        # ativar o ambiente
pip install -r requirements.txt  # instalar dependências

python -m fisica.corpos          # planeta e foguete de exemplo (mi ≈ 394800)
python -m fisica.simulation      # aceleração e foguete após um passo
python validacao.py              # validação da órbita completa
```

O `-m` é necessário para os arquivos dentro de `fisica/`, pois eles importam uns aos outros como pacote (`from fisica.config import ...`).

---

## ⚠️ Limitações

- Apenas um planeta.
- Oscilação numérica de ~0,3% na distância da órbita, causada pelo passo de tempo.
- Dimensões da caixa e massa do foguete ainda provisórias.
- Motor, eventos e simulação visual ainda em desenvolvimento (Semana 2).
- Sem integração com a interface e a CNC (Semana 3).

---

## 📚 Referências

- Leis de Newton e Lei da Gravitação Universal.
- 3ª Lei de Kepler (relação entre período e raio da órbita).
- NASA JPL — *Basics of Space Flight*.
