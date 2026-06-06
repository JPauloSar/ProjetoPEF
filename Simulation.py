import os
import numpy as np
import matplotlib.pyplot as plt
import math

#Hipóteses Siplificadoras para os fins da simulação:
#   1) A torre consiste em um engaste fixo no solo com altura H;
#   2) A torre é um tronco de cone cujo raio diminui linearmente com a altura (de R_base até R_nacelle) 
#      e possui espessura (e) constante;
#   3) O peso de um corte infinitesimal dz é dado pela densidade (d) do concreto pela área da coroa circular
#      criada pela geometria; A = pi*(R^2-[R-e]^2). 
#   4) O vento possui uma carga distribuida na torre cuja força é proporcional ao diâmetro da torre naquele ponto.
#      também há uma força concentrada do vento na nacelle.


# parametros fixos iniciais apenas para codar (pandas depois para fazer iterações):
R_base =  2.25             #metros
R_nacelle = 1.0            #metros
H = 119.0                  #metros
pesoNacelle = 2907.0       #KN
d = 2500.0                 #kg/m3
e = 0.2                    #metros


nome_pasta = f"Torre_H{H}m_Rb{R_base*100}cm_Rn{R_nacelle}m_e{e*100}cm"
os.makedirs(nome_pasta, exist_ok=True)

g = 9.81            #m/s2

#pressaoVento = 1.5          #KPa
#forcaNacelle = 1044.0       #KN
#momentoNacelle = 12817.0    #KNm

cenarios = {
    # =========================================================================================
    # 1. CENÁRIOS DOCUMENTADOS (Baseados no doc ALSTOM / EGT Engenharia cedidos pelo professor)
    # =========================================================================================
    
    # Cargas Extremas - Com coeficientes de majoração (γF = 1.35)
    "Vento_Extremo_ALSTOM": {"pressao": 1.50, "forca": 1044.0, "momento": 12817.0},
    
    # Caso DLC 1.1 (Serviço) - Cargas quase-permanentes sem majoração (γF = 1.00)
    "Vento_Servico_DLC_1_1": {"pressao": 0.82, "forca": 574.0, "momento": 7049.0},
    
    # Cargas de Fadiga Equivalente - (Curva S-N m=4)
    "Vento_Fadiga_m4": {"pressao": 0.54, "forca": 378.0, "momento": 4644.0},

    # ==============================================================================
    # 2. CENÁRIOS EXTREMOS HIPOTÉTICOS (CRIADOS POR INTELIGÊNCIA ARTIFICIAL - GEMINI)
    # Valores plausíveis inspirados nos Design Load Cases (DLC) da norma IEC 61400-1 
    # gerados exclusivamente para fins didáticos e testes de simulação.
    # ==============================================================================
    
    # Turbina parada na tempestade (Pás em bandeira protegem a nacelle, mas a torre sofre)
    "Tempestade_50Anos_Parada": {"pressao": 2.80, "forca": 450.0, "momento": 6200.0},
    
    # Travamento brusco do rotor em operação (Inércia cria momento fletor colossal no topo)
    "Frenagem_Emergencia_DLC21": {"pressao": 1.40, "forca": 1400.0, "momento": 18500.0},
    
    # Rajada lateral (Vento obliquo força a estrutura de lado antes da turbina girar)
    "Rajada_Mudanca_Direcao_DLC14": {"pressao": 1.80, "forca": 1250.0, "momento": 10500.0}
}

#contas:
def calcular_raio(z):
    """calcula o raio para determinada altura"""
    return  R_base - ((R_base-R_nacelle) / H) * z 

def calcular_area(z):
    """calcula a área da seção transversal vazada para alturas z"""
    r_ext = calcular_raio(z)
    r_int = r_ext - e
    return np.pi * (r_ext**2 - r_int**2)

def peso_distribuido(z, dz):
    """calcula o peso de cada fatia na altura z"""
    area = calcular_area(z)
    return g*area*d*dz /1000.0

def vento_distribuido(z, dz, pressaoVento):
    """calcula a força do vento sobre uma fatia da torre na altura z"""
    Diametro = 2*calcular_raio(z)
    return (Diametro*dz*pressaoVento)

#esforços
def calcular_Esforcos(z,dz, pressaoVento, forcaNacelle, momentoNacelle):
    """Calcula os vetores esforços internos ao longo da altura, de cima para baixo"""
   
    peso_fatias = peso_distribuido(z, dz)
    vento_fatias = vento_distribuido(z, dz, pressaoVento)

    peso_inv = peso_fatias[::-1]
    vento_inv = vento_fatias[::-1]

    #calculo da normal:
    normal_inv = pesoNacelle + np.cumsum(peso_inv) - peso_inv

    #calculo da forca cortante:
    forcaCortante_inv = forcaNacelle + np.cumsum(vento_inv) - vento_inv 

    #calculo do momento fletor:
    momentoFletor_inv = momentoNacelle + np.cumsum(forcaCortante_inv * dz) - (forcaCortante_inv * dz)

    normal = normal_inv[::-1]
    forcaCortante = forcaCortante_inv[::-1]
    momentoFletor =momentoFletor_inv[::-1]

    return normal, forcaCortante, momentoFletor

#Função principal
print("Começando simulações...\n")

dz = 1.0
z = np.arange(dz / 2, H, dz)


fig_global, axs_global = plt.subplots(1, 3, figsize=(16, 8))
num_cenarios = len(cenarios)
cores_arco_iris = plt.cm.rainbow(np.linspace(0, 1, num_cenarios))
cores_dinamicas = {cenario: cores_arco_iris[i] for i, cenario in enumerate(cenarios.keys())}

for cenario, dados in cenarios.items():
    # Calcula os esforços estruturais do cenário atual
    normal, forcaCortante, momentoFletor = calcular_Esforcos(z, dz, dados["pressao"], dados["forca"], dados["momento"])


    fig_ind, axs_ind = plt.subplots(1, 3, figsize=(12, 6))
    
    # Força Normal (Individual)
    axs_ind[0].plot(normal, z, color='blue', linewidth=2)
    axs_ind[0].set_title("Força Normal (N)")
    axs_ind[0].set_xlabel("Força (kN)")
    axs_ind[0].set_ylabel("Altura da Torre (m)")
    axs_ind[0].grid(True, linestyle='--', alpha=0.7)

    # Esforço Cortante (Individual)
    axs_ind[1].plot(forcaCortante, z, color='green', linewidth=2)
    axs_ind[1].set_title("Esforço Cortante (V)")
    axs_ind[1].set_xlabel("Força (kN)")
    axs_ind[1].grid(True, linestyle='--', alpha=0.7)

    # Momento Fletor (Individual)
    axs_ind[2].plot(momentoFletor, z, color='red', linewidth=2)
    axs_ind[2].set_title("Momento Fletor (M)")
    axs_ind[2].set_xlabel("Momento (kNm)")
    axs_ind[2].grid(True, linestyle='--', alpha=0.7)

    fig_ind.tight_layout()
    
    
    nome_arquivo_ind = f"grafico_{cenario.replace(' ', '_')}.png"
    caminho_ind = os.path.join(nome_pasta, nome_arquivo_ind)
    
    fig_ind.savefig(caminho_ind, dpi=300)
    plt.close(fig_ind) 
    print(f"-> Gráfico individual de '{cenario}' gerado com sucesso.")


    cor_atual = cores_dinamicas[cenario] 
    
    # O texto do 'label' agora vem direto da chave do dicionário de forma automática
    axs_global[0].plot(normal, z, color=cor_atual, linewidth=2, label=cenario)
    axs_global[1].plot(forcaCortante, z, color=cor_atual, linewidth=2)
    axs_global[2].plot(momentoFletor, z, color=cor_atual, linewidth=2)

#estilização da Força Normal Global
axs_global[0].set_title("Força Normal (N)", fontsize=12, fontweight='bold')
axs_global[0].set_xlabel("Força (kN)", fontsize=10)
axs_global[0].set_ylabel("Altura da Torre (m)", fontsize=10)
axs_global[0].grid(True, linestyle='--', alpha=0.5)

axs_global[0].legend(loc="upper right", fontsize=8)

#estilização do Esforço Cortante Global
axs_global[1].set_title("Esforço Cortante (V)", fontsize=12, fontweight='bold')
axs_global[1].set_xlabel("Força (kN)", fontsize=10)
axs_global[1].grid(True, linestyle='--', alpha=0.5)

#estilização do Momento Fletor Global
axs_global[2].set_title("Momento Fletor (M)", fontsize=12, fontweight='bold')
axs_global[2].set_xlabel("Momento (kNm)", fontsize=10)
axs_global[2].grid(True, linestyle='--', alpha=0.5)

fig_global.tight_layout()

caminho_global = os.path.join(nome_pasta, "00_Comparativo_Geral_de_Cenarios.png")
fig_global.savefig(caminho_global, dpi=300)
plt.close(fig_global)

print(f"Sucesso! Os gráficos foram salvos em: {nome_pasta}")