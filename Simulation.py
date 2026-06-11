import os
import json
import numpy as np
import matplotlib.pyplot as plt
import math

#Hipóteses Siplificadoras para os fins da simulação:
#   1) A torre consiste em um engaste fixo no solo com altura H;
#   2) A torre é um tronco de cone cujo raio diminui linearmente com a altura (de R_base até R_nacelle) 
#      até sua metade, onde ela passa a ser um cilindro. A estrutura possui espessura (e) constante ao longo de
#      toda a sua extensão;
#   3) O peso de um corte infinitesimal dz é dado pela densidade (d) do concreto pela área da coroa circular
#      criada pela geometria; A = pi*(R^2-[R-e]^2); 
#   4) O vento possui uma carga distribuida na torre cuja força é proporcional ao diâmetro, seguindo o 
#      perfil de Hellmann (IEC 61400-1) para pressão do vento na torre naquele ponto. Ou seja: P_z= P_H*(z/H)**(2*alfa).
#      também há uma força concentrada do vento na nacelle.

#Leitura do .json da torre 

with open( "parametros_torre.json" , "r" ) as torre :
    dados_torre = json.load(torre)

params = dados_torre["parametros_torre"]

R_base = params["R_base"]
R_nacelle = params["R_nacelle"]
H = params["H"]
pesoNacelle = params["pesoNacelle"]
d = params["d"]
e = params["e"]
alfa = params["alfa"]
Cd = params["Cd"]

#leitura do .json cenarios_vento

with open( "cenarios_vento.json" , "r" ) as arquivo_cenarios :
    dados_cenarios = json.load(arquivo_cenarios)

cenarios = dados_cenarios["cenarios"]

#criação da pasta 

nome_pasta = f"Torre_H{H}m_Rb{R_base*100}cm_Rn{R_nacelle}m_e{e*100}cm"
os.makedirs(nome_pasta, exist_ok=True)

#Dados hardcode

g = 9.81            #m/s2


#contas:
def calcular_raio(z):
    """calcula o raio para determinada altura"""

    return  np.where(z < (H/2) , R_base - ((R_base-R_nacelle) / (H/2)) * z , R_nacelle ) 

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
    return (Cd * Diametro * dz * pressaoVento * ( ( z / H ) ** (2*alfa) ))

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
    momentoFletor_inv = momentoNacelle + np.cumsum(forcaCortante_inv * dz) - (forcaNacelle * dz) 

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

# --- CORREÇÃO DE SOBREPOSIÇÃO ---
# Força notação científica no eixo X
axs_global[2].ticklabel_format(style='sci', axis='x', scilimits=(0,0))
fig_global.tight_layout()

caminho_global = os.path.join(nome_pasta, "00_Comparativo_Geral_de_Cenarios.png")
fig_global.savefig(caminho_global, dpi=300)
plt.close(fig_global)

print(f"Sucesso! Os gráficos foram salvos em: {nome_pasta}")