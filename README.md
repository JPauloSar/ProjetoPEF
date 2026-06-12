---

# Simulador de Esforços Estruturais - Torre Eólica (Projeto PEF-3208 2026)

Este projeto realiza a simulação numérica dos esforços internos (Força Normal, Esforço Cortante e Momento Fletor) ao longo da altura de uma torre eólica de concreto armado utilizando Python, NumPy e Matplotlib.

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

### 2. Executar o Simulador

Com o ambiente ativado, inicie a Interface de Linha de Comando (CLI) executando o script principal de interação:

```bash
python wrapper.py

```

O menu interativo será aberto no terminal, listando automaticamente todos os modelos de torres disponíveis para simulação.

---

## 📁 Estrutura do Repositório

A arquitetura do projeto aplica o conceito de *Separation of Concerns* (Separação de Preocupações), dividindo dados, código e saídas em diretórios específicos:

* **`modelos_torres/`**: Diretório que armazena as "receitas" das torres em arquivos `.json` individuais.
* **`Simulações_Feitas/`**: Pasta gerada automaticamente onde os resultados visuais e de dados são salvos de forma organizada.
* **`cenarios_vento.json`**: Banco de dados unificado contendo as premissas de carregamento para as simulações.
* **`Simulation.py`**: Motor matemático (backend) encarregado da discretização e integração numérica.
* **`wrapper.py`**: Interface iterativa e segura que orienta a experiência do usuário pelo terminal.

---

## ⚙️ Funcionalidades do Código

O script atua como um simulador paramétrico, realizando a discretização da torre eólica em "fatias" de elementos finitos (com passo de **1.0 m**). Ele integra os esforços numericamente de cima para baixo (da nacelle até o engaste na base).

A torre possui **geometria de tronco de cone** até metade da sua altura, passando então a ter raio constante.

As principais etapas e diferenciais do código incluem:

* **Cálculo Geométrico Dinâmico:** Determina o raio externo, raio interno e a área da seção transversal vazada para qualquer altura da torre de forma contínua e vetorizada.
* **Carregamento Aerodinâmico Não-Linear:** Aplica o perfil de *Wind Shear* (Camada Limite Atmosférica). A pressão do vento é calculada exponencialmente para cada cota e multiplicada pelo diâmetro local, simulando com precisão o escoamento real exigido em normas.
* **Integração Numérica de Esforços:** Utiliza funções otimizadas do NumPy (`np.cumsum`) para acumular as cargas verticais e horizontais, construindo iterativamente os braços de alavanca para o Momento Fletor.
* **CLI e Rastreabilidade:** O sistema lista os modelos, executa os cálculos e, ao salvar os gráficos de saída, cria uma cópia de segurança do `.json` original na mesma pasta dos resultados para garantir a reprodutibilidade dos dados.

---

## 🏗️ Hipóteses Simplificadoras

Para fins didáticos e de simulação, o modelo matemático assume as seguintes premissas:

1. **Engaste Perfeito:** A base da torre é considerada perfeitamente engastada no solo.
2. **Geometria Específica:** O raio da torre diminui de forma linear desde a base até sua metade, a partir de onde mantém um perfil cilíndrico. A estrutura possui espessura de parede constante durante todo o seu comprimento.
3. **Peso Próprio Discretizado:** O peso de cada fatia infinitesimal é calculado multiplicando a densidade do concreto pelo volume da coroa circular daquela seção.
4. **Cargas de Vento (Wind Shear):** A pressão dinâmica do vento obedece ao Perfil de Hellmann (norma **IEC 61400-1**). A pressão varia com a altura pela relação $P_z=P_H(z/H)^{2\alpha}$. A força distribuída em cada cota é o produto dessa pressão pelo diâmetro local exposto. Adicionalmente, atuam no topo uma força e um momento fletor concentrados gerados pelo rotor/nacelle.

---

## 🌪️ Cenários de Carga Simulados

O programa testa a estrutura sob diversas condições distintas, separadas em dois grupos principais:

* **Vento Extremo:** Cargas máximas com coeficientes de majoração.
* **Serviço (DLC 1.1):** Cargas quase-permanentes de operação normal.
* **Fadiga:** Cargas equivalentes para verificação de vida útil sob ciclos repetitivos.
* **Tempestade 50 Anos:** Turbina em repouso enfrentando rajadas críticas de vento.
* **Frenagem de Emergência (DLC 2.1):** Simula o colossal momento fletor no topo gerado pelo travamento brusco das pás.
* **Rajada com Mudança de Direção (DLC 1.4):** Carga severa oblíqua testando o cisalhamento da torre.

---

## 📂 Saída de Dados (Outputs)

Ao finalizar a execução, o código organiza os resultados automaticamente dentro da pasta genitora `Simulações_Feitas/`:

1. **Pasta Dedicada:** O sistema cria um subdiretório com o nome exato do modelo simulado (Exemplo: `Torre_ALSTOM_T119/`).
2. **Backup de DNA:** O arquivo `.json` original é copiado para dentro desta pasta, garantindo o registro exato dos parâmetros que geraram aqueles resultados.
3. **Gráficos Individuais:** Imagens `.png` com os três gráficos estruturais para **cada** cenário.
4. **Comparativo Global:** Um arquivo consolidado (`00_Comparativo_Geral_de_Cenarios.png`) é gerado sobrepondo todos os cenários nos mesmos eixos.

---

## 🛠️ Como Criar Torres Personalizadas

O simulador é 100% paramétrico. Qualquer pessoa pode testar novos designs (como torres mais altas, mais finas ou para rotores mais pesados) sem precisar alterar uma única linha de código Python.

**Atenção ao Perfil Geométrico:** O modelo matemático deste script assume que a torre afunila linearmente (tronco de cone) desde a base até **metade da sua altura** ($H/2$). A partir da metade até o topo, a torre assume um perfil **cilíndrico** de raio constante.

Basta criar um novo arquivo `.json` dentro da pasta `modelos_torres/` seguindo esta estrutura padrão:

```json
{
    "parametros_torre": {
        "R_base": 3.75,       // Raio na base da torre (m)
        "R_nacelle": 2.05,    // Raio no topo da torre. A torre mantém este raio constante da metade (H/2) até o topo (m)
        "H": 119.0,           // Altura total da torre (m)
        "pesoNacelle": 1938.0,// Força Vertical / Peso do conjunto rotor+nacelle (kN)
        "d": 2500.0,          // Densidade do material, ex: concreto (kg/m³)
        "e": 0.30,            // Espessura constante da parede da torre (m)
        "alfa": 0.085,        // Expoente de perfil de vento (Wind Shear de Hellmann)
        "Cd": 0.6             // Coeficiente de arrasto aerodinâmico
    }
}

```

Assim que o arquivo for salvo, basta executar o comando `python wrapper.py` novamente. O seu novo modelo será automaticamente detectado e listado no menu interativo do terminal!