```markdown
# Simulador de Esforços Estruturais - Torre Eólica (Projeto PEF-3208 2026)

Este projeto realiza a simulação numérica dos esforços internos (Força Normal, Esforço Cortante e Momento Fletor) ao longo da altura de uma torre eólica de concreto armado (tronco-cônica) utilizando Python, NumPy e Matplotlib.

## 🚀 Como Rodar o Projeto

Como o projeto utiliza um ambiente virtual do Python (`ambienteTorre`) dentro do ambiente WSL (Ubuntu/Linux no Windows), siga os passos abaixo no seu terminal para executar a simulação.

### 1. Ativar o Ambiente Virtual
Navegue até a pasta do projeto e ative o ambiente virtual para carregar as dependências corretas (NumPy, Pandas, Matplotlib):
```bash
cd ~/ProjetoPEF
source ambienteTorre/bin/activate

```

### 2. Executar o Script

Com o ambiente ativado, basta rodar o arquivo principal em Python:

```bash
python Simulation.py

```

---

## ⚙️ Funcionalidades do Código

O script realiza a discretização da torre eólica em "fatias" infinitesimais (com passo `dz = 1.0 m`) e integra os esforços de cima para baixo (da nacelle até a base), aplicando os princípios da estática para determinar as reações ao longo de toda a estrutura.

As principais etapas do código incluem:

* **Cálculo Geométrico Dinâmico:** Determina o raio externo, raio interno e a área da seção transversal vazada para qualquer altura `z`.
* **Distribuição de Cargas:** Calcula o peso próprio da estrutura (concreto) e a força distribuída do vento, que varia proporcionalmente ao diâmetro da torre em cada cota.
* **Integração de Esforços:** Acumula as cargas verticais e horizontais, além de calcular os momentos fletores gerados pelas forças cortantes e pelas cargas concentradas no topo.
* **Geração Automática de Gráficos:** Plota os perfis de N, V e M e os salva automaticamente.

---

## 🏗️ Hipóteses Simplificadoras

Para fins didáticos e de simulação, o modelo matemático assume as seguintes premissas:

1. **Engaste Perfeito:** A base da torre é considerada perfeitamente engastada no solo.
2. **Geometria de Tronco de Cone:** O raio da torre diminui de forma linear desde a base ($R_{base}$) até o topo ($R_{nacelle}$), mantendo uma espessura de parede constante ($e$).
3. **Peso Próprio Discretizado:** O peso de cada fatia infinitesimal é calculado multiplicando a densidade do concreto pelo volume da coroa circular daquela seção.
4. **Cargas de Vento:** A carga de vento distribuída na torre resulta em uma força proporcional ao diâmetro exposto na respectiva altura. Na nacelle, atua uma força concentrada de vento e um momento fletor inicial.

---

## 🌪️ Cenários de Carga Simulados

O programa testa a estrutura sob seis condições distintas, separadas em dois grupos:

### 1. Cenários Documentados (Base ALSTOM / EGT Engenharia)

* **Vento Extremo:** Cargas máximas com coeficientes de majoração ($\gamma_F = 1.35$).
* **Serviço (DLC 1.1):** Cargas quase-permanentes de operação normal ($\gamma_F = 1.00$).
* **Fadiga (m=4):** Cargas equivalentes para verificação de vida útil sob ciclos repetitivos.

### 2. Cenários Extremos Hipotéticos (Gerados por IA baseados na IEC 61400-1)

* **Tempestade 50 Anos (Parada):** Turbina em repouso enfrentando rajadas críticas de vento.
* **Frenagem de Emergência (DLC 2.1):** Simula o colossal momento fletor no topo gerado pelo travamento brusco das pás.
* **Rajada com Mudança de Direção (DLC 1.4):** Carga severa oblíqua testando o cisalhamento da torre.

---

## 📂 Saída de Dados (Outputs)

Ao finalizar a execução, o código organiza os resultados automaticamente para não poluir o diretório raiz:

1. **Criação de Pasta Inteligente:** Uma pasta nomeada com as propriedades da torre é criada automaticamente (Exemplo: `Torre_H119.0m_Rb225.0cm_Rn1.0m_e20.0cm`).
2. **Gráficos Individuais:** Salva imagens `.png` com os três gráficos (N, V, M) para **cada** cenário simulado.
3. **Gráfico Comparativo Geral:** Um arquivo consolidado (`00_Comparativo_Geral_de_Cenarios.png`) é gerado sobrepondo todos os cenários nos mesmos eixos, facilitando a análise crítica das situações mais exigentes para o dimensionamento.

```

```