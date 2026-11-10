# Projeto de Micro Controladores

# 🚀 Simulador de Órbita — Módulo de Simulação Física
 
> **Etapa:** Semana 1 — Protótipo funcional (entrega em 12/11)
> **Responsável:** Thiago Duarte Oliveira
> **Status:** 🟡 Em desenvolvimento
 
Este módulo é o "cérebro físico" do simulador: ele calcula como o foguete se move sob a gravidade de um planeta. Nesta primeira etapa, o objetivo é ter um foguete orbitando um planeta de forma estável, validado numericamente.
 
---
 
## 🎯 Objetivo da etapa
 
- Definir o modelo físico e as unidades usadas no projeto.
- Criar as classes `Planet` e `Rocket`.
- Implementar a gravidade e a atualização do movimento a cada passo de tempo.
- Validar que uma órbita circular se mantém estável por várias voltas.
---
 
## 📐 Modelo físico
 
| Decisão | Escolha | Motivo |
|---|---|---|
| Dimensões | 2D (plano XY) | A caixa é vista de cima, igual à câmera e à CNC |
| Unidade de distância | milímetro (mm) | Mesma unidade da caixa, sem conversão de escala |
| Unidade de tempo | segundo (s) | Movimento visível em tempo real |
| Planetas | Fixos | São peças físicas paradas dentro da caixa |
| Foguete | Ponto (sem tamanho) | Simplifica o cálculo sem perder o comportamento |
| Atmosfera / atrito | Ignorados | Fora do escopo do projeto |
 
### Constante gravitacional (μ)
 
Em vez de usar a constante G e a massa M separadas, usamos um único parâmetro:
 
```
μ = G · M
```
 
O valor de μ foi escolhido para que as órbitas **caibam na caixa** e tenham uma **velocidade visível**, e não para reproduzir valores reais.
 
**Exemplo de cálculo:** para uma órbita de raio 100 mm com período de 10 s:
 
```
T = 2π · √(r³ / μ)    →    μ = 4π² · r³ / T²
 
μ = 4 · 9,87 · 100³ / 10²  ≈  394.800 mm³/s²
```
 
Velocidade orbital correspondente:
 
```
v = √(μ / r) = √(394.800 / 100) ≈ 62,8 mm/s
```
 
Verificação: circunferência = 2π · 100 ≈ 628 mm → 628 mm / 10 s = 62,8 mm/s ✅
 
---
 
## 🧱 Estrutura
 
```
physics/
├── bodies.py        # classes Planet e Rocket
└── simulation.py    # cálculo da gravidade e atualização do movimento
validacao.py         # script de validação da órbita
```
 
### Classes
 
**`Planet`**
| Atributo | Unidade | Descrição |
|---|---|---|
| `posicao` | mm | Coordenadas (x, y) do centro |
| `raio` | mm | Usado para detectar colisão |
| `mu` | mm³/s² | Intensidade da gravidade (G · M) |
 
**`Rocket`**
| Atributo | Unidade | Descrição |
|---|---|---|
| `posicao` | mm | Coordenadas (x, y) |
| `velocidade` | mm/s | Componentes (vx, vy) |
| `angulo` | rad | Direção do bico (convertido para graus só na entrada/saída) |
| `combustivel` | — | Quantidade disponível (usada a partir da Semana 2) |
 
---
 
## ⚙️ Como o movimento é calculado
 
### 1. Gravidade
 
```
a = −μ · r / |r|³        onde   r = posição do foguete − posição do planeta
```
 
- `r / |r|` dá a **direção** (vetor unitário do planeta para o foguete).
- `μ / |r|²` dá a **intensidade** (a gravidade diminui com o quadrado da distância).
- O sinal **negativo** faz a aceleração apontar **para o planeta**.
### 2. Atualização a cada passo (Euler semi-implícito)
 
A cada passo de tempo `dt`:
 
```
1.  v = v + a · dt      (primeiro a velocidade)
2.  x = x + v · dt      (depois a posição, usando a velocidade NOVA)
```
 
A ordem é importante: atualizar a posição com a velocidade antiga (Euler comum) faz a órbita abrir em espiral a cada volta, criando energia que não existe. O método semi-implícito mantém a órbita estável.
 
**Passo de tempo usado:** `dt = 0,01 s` (100 passos por segundo).
 
---
 
## ✅ Validação
 
### Teste principal — órbita circular
 
| Parâmetro | Valor |
|---|---|
| Posição do planeta | (0, 0) mm |
| Posição inicial do foguete | (100, 0) mm |
| Velocidade inicial | (0; 62,8) mm/s — perpendicular ao raio |
| μ | 394.800 mm³/s² |
| Duração | 30 s (3 voltas, 3.000 passos) |
 
**Critério de sucesso:** a distância entre o foguete e o planeta permanece próxima de 100 mm (variação máxima de 1 a 2 mm) durante as 3 voltas.
 
**Resultado obtido:** _(preencher após rodar)_
 
### Experimentos de comportamento
 
| Velocidade inicial | Comportamento esperado | Resultado |
|---|---|---|
| 62,8 mm/s (orbital) | Órbita circular estável | _(preencher)_ |
| 44 mm/s (70%) | Elipse que mergulha perto do planeta; colisão se passar do raio | _(preencher)_ |
| 75 mm/s | Elipse que se afasta e volta | _(preencher)_ |
| 88,8 mm/s (√2 × orbital) | Velocidade de escape — o foguete não volta | _(preencher)_ |
 
A velocidade de escape vem de:
 
```
v_escape = √(2μ / r) = √2 · v_orbital
```
 
---
 
## ▶️ Como executar
 
```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install numpy
python validacao.py
```
 
O script imprime a distância do foguete ao planeta a cada 100 passos.
 
---
 
## ⚠️ Limitações desta etapa
 
- Apenas um planeta.
- Sem empuxo, controle por botões ou combustível (entram na Semana 2).
- Sem detecção de colisão e de saída da caixa (Semana 2).
- Sem integração com a câmera e a CNC (Semana 3).
---
 
## 📚 Referências
 
- Leis de Newton e Lei da Gravitação Universal.
- 3ª Lei de Kepler (relação entre período e raio da órbita).
- NASA JPL — *Basics of Space Flight*.