import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math

nome_pasta = "graficos_resultados"
os.makedirs(nome_pasta, exist_ok=True)

#Hipóteses Siplificadoras para os fins da simulação:
#   1) A torre consiste em um engaste fixo no solo com altura H;
#   2) A torre é um tronco de cone cujo raio diminui linearmente com a altura (de R_base até R_nacelle) 
#      e possui espessura (e) constante;
#   3) O peso de um corte infinitesimal dz é dado pela densidade (d) do concreto pela área da coroa circular
#      criada pela geometria; A = pi*(R^2-[R-e]^2). 
#   4) O vento possui uma carga distribuida na torre cuja força é proporcional ao diâmetro da torre naquele ponto.
#      também há uma força concentrada do vento na nacelle.


# parametros fixos iniciais apenas para codar (pandas depois para fazer iterações):
R_base =  2.25      #metros
R_nacelle = 1.0     #metros
H = 119.0           #metros

e = 0.2             #metros
d = 2500.0          #kg/m3
g = 9.81            #m/s2

pressaoVento = 1.5          #KPa
pesoNacelle = 2907.0        #KN
forcaNacelle = 1044.0       #KN
momentoNacelle = 12817.0    #KNm
  
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

def vento_distribuido(z, dz):
    """calcula a força do vento sobre uma fatia da torre na altura z"""
    Diametro = 2*calcular_raio(z)
    return (Diametro*dz*pressaoVento)

#esforços
def calcular_Esforcos(z,dz):
    """Calcula os vetores esforços internos ao longo da altura, de cima para baixo"""
   
    peso_fatias = peso_distribuido(z, dz)
    vento_fatias = vento_distribuido(z, dz)

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

normal, forcaCortante, momentoFletor = calcular_Esforcos(z, dz)

print("Gráfico gerado:")
plt.figure(figsize=(12, 6))

#Força Normal
plt.subplot(1, 3, 1) # (1 linha, 3 colunas, gráfico nº 1)
plt.plot(normal, z, color='blue', linewidth=2)
plt.title("Força Normal (N)")
plt.xlabel("Força (kN)")
plt.ylabel("Altura da Torre (m)")
plt.grid(True, linestyle='--', alpha=0.7)

#Esforço Cortante
plt.subplot(1, 3, 2) # (1 linha, 3 colunas, gráfico nº 2)
plt.plot(forcaCortante, z, color='green', linewidth=2)
plt.title("Esforço Cortante (V)")
plt.xlabel("Força (kN)")
plt.grid(True, linestyle='--', alpha=0.7)

#Momento Fletor
plt.subplot(1, 3, 3) # (1 linha, 3 colunas, gráfico nº 3)
plt.plot(momentoFletor, z, color='red', linewidth=2)
plt.title("Momento Fletor (M)")
plt.xlabel("Momento (kNm)")
plt.grid(True, linestyle='--', alpha=0.7)

plt.tight_layout()
nome_pasta = "graficos_resultados"
os.makedirs(nome_pasta, exist_ok=True)  
caminho_salvamento = os.path.join(nome_pasta, "grafico_caso_base.png")
plt.savefig(caminho_salvamento, dpi=300)

print(f"Sucesso! O gráfico foi salvo em: {caminho_salvamento}")