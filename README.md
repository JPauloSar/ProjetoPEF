
# Simulador de Esforços Estruturais - Torre Eólica (Projeto PEF-3208 2026)

Este projeto realiza a simulação numérica dos esforços internos (Força Normal, Esforço Cortante e Momento Fletor) ao longo da altura de uma torre eólica de concreto armado (tronco-cônica) utilizando Python, NumPy e Matplotlib.

## 🚀 Como Rodar o Projeto

Para garantir que o simulador funcione perfeitamente em qualquer máquina, as dependências do projeto são gerenciadas através de um arquivo `requirements.txt`. Siga os passos abaixo no seu terminal para configurar o ambiente e executar a simulação:

### 1. Criar e Ativar o Ambiente Virtual
Navegue até a pasta do projeto e crie um ambiente virtual limpo (para isolar as bibliotecas deste projeto do resto do seu computador):
```bash
cd ~/ProjetoPEF
python -m venv ambienteTorre
source ambienteTorre/bin/activate
pip install -r requirements.txt

```

### 2. Executar o Script

Com o ambiente ativado, basta rodar o arquivo principal em Python:

```bash
python Simulation.py

```
---

## ⚙️ Funcionalidades do Código

O script atua como um simulador paramétrico, realizando a discretização da torre eólica em "fatias" de elementos finitos (com passo `dz = 1.0 m`). Ele integra os esforços numericamente de cima para baixo (da nacelle até o engaste na base), aplicando o Método da Soma de Riemann para determinar as reações ao longo de toda a estrutura.

As principais etapas e diferenciais do código incluem:

* **Cálculo Geométrico Dinâmico:** Determina o raio externo, raio interno e a área da seção transversal vazada para qualquer altura `z` da torre de forma contínua e vetorizada.
* **Carregamento Aerodinâmico Não-Linear:** Além de calcular o peso próprio da estrutura, o script aplica o perfil de *Wind Shear* (Camada Limite Atmosférica). A pressão do vento é calculada exponencialmente para cada cota `z` e multiplicada pelo diâmetro local, simulando com precisão o escoamento real exigido em normas.
* **Integração Numérica de Esforços:** Utiliza funções otimizadas do NumPy (`np.cumsum`) para acumular as cargas verticais (Força Normal) e horizontais (Esforço Cortante), construindo iterativamente os braços de alavanca para o Momento Fletor gerado pelas cortantes e pelas cargas concentradas no topo.
* **Automação de Cenários e Exportação:** O script itera automaticamente sobre um dicionário contendo múltiplos cenários de carga (como vento de serviço, fadiga e frenagem de emergência). Ele cria pastas dinâmicas baseadas nas dimensões da torre, salva os gráficos individuais e gera um diagrama comparativo global formatado em notação científica para análise direta.

---

## 🏗️ Hipóteses Simplificadoras

Para fins didáticos e de simulação, o modelo matemático assume as seguintes premissas:

1. **Engaste Perfeito:** A base da torre é considerada perfeitamente engastada no solo.
2. **Geometria de Tronco de Cone:** O raio da torre diminui de forma linear desde a base ($R_{base}$) até o topo ($R_{nacelle}$), mantendo uma espessura de parede constante ($e$).
3. **Peso Próprio Discretizado:** O peso de cada fatia infinitesimal é calculado multiplicando a densidade do concreto pelo volume da coroa circular daquela seção.
4. **Cargas de Vento Não-Lineares (Wind Shear):** A pressão dinâmica do vento distribuída ao longo da torre obedece ao perfil da camada limite atmosférica (Perfil de Hellmann / Lei da Potência), conforme a norma internacional **IEC 61400-1**. A pressão varia exponencialmente com a altura através da relação $P_z = P_H \cdot (z/H)^{2\alpha}$. A força distribuída em cada cota é o produto dessa pressão variável pelo diâmetro local exposto. Adicionalmente, atuam no topo uma força cortante concentrada e um momento fletor inicial provenientes do empuxo e da inércia do rotor/nacelle.
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

