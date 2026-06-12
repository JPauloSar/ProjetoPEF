import os
import sys
import time

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    limpar_tela()
    print("="*95)
    print('''
 .d8888b.  d8b                        888               888                                 
d88P  Y88b Y8P                        888               888                                 
Y88b.                                 888               888                                 
 "Y888b.   888 88888b.d88b.  888  888 888  8888b.   .d88888  .d88b.  888d888                
    "Y88b. 888 888 "888 "88b 888  888 888     "88b d88" 888 d88""88b 888P"                  
      "888 888 888  888  888 888  888 888 .d888888 888  888 888  888 888                    
Y88b  d88P 888 888  888  888 Y88b 888 888 888  888 Y88b 888 Y88..88P 888                    
 "Y8888P"  888 888  888  888  "Y88888 888 "Y888888  "Y88888  "Y88P"  888                    
                                                                                            
                                                                                            
                                                                                            
88888888888                                    8888888888         888 d8b                   
    888                                        888                888 Y8P                   
    888                                        888            pd  888                       
    888   .d88b.  888d888 888d888 .d88b.       8888888    .d88b.  888 888  .d8888b  8888b.  
    888  d88""88b 888P"   888P"  d8P  Y8b      888       d88""88b 888 888 d88P"        "88b 
    888  888  888 888     888    88888888      888       888  888 888 888 888      .d888888 
    888  Y88..88P 888     888    Y8b.          888       Y88..88P 888 888 Y88b.    888  888 
    888   "Y88P"  888     888     "Y8888       8888888888 "Y88P"  888 888  "Y8888P "Y888888 
   ___             _     __         ___  ________    ____ ___  ___  ___    ___  ___  ___  ____
  / _ \_______    (_)__ / /____    / _ \/ __/ __/___|_  /|_  |/ _ \( _ )  |_  |/ _ \|_  |/ __/
 / ___/ __/ _ \  / / -_) __/ _ \  / ___/ _// _//___//_ </ __// // / _  | / __// // / __// _ \ 
/_/  /_/  \___/_/ /\__/\__/\___/ /_/  /___/_/     /____/____/\___/\___/ /____/\___/____/\___/ 
             |___/                                                                            
                                    coded by: Sara3va
                                                                                        ''')
    print("="*95)
    
    # 1. Definimos o nome da pasta onde estão os JSONs das torres
    pasta_modelos = "modelos_torres"
    
    # Cria a pasta automaticamente se ela ainda não existir
    if not os.path.exists(pasta_modelos):
        os.makedirs(pasta_modelos)
    
    # 2. Procura os ficheiros APENAS dentro dessa nova pasta
    arquivos_disponiveis = [f for f in os.listdir(pasta_modelos) if f.endswith('.json')]
    
    if arquivos_disponiveis:
        print(f"\nModelos de Torre disponíveis na pasta '{pasta_modelos}/':")
        for arq in arquivos_disponiveis:
            print(f"  -> {arq}")
    else:
        print(f"\nNenhum arquivo .json encontrado na pasta '{pasta_modelos}/'.")
        print("Por favor, adicione os seus modelos lá dentro e tente novamente.")
        return # Encerra o wrapper
    
    print("-" * 50)
    
    # Pede a entrada do utilizador
    torre_escolhida = input("\nQual Torre quer simular? (passe o nome do .json): ").strip()
    
    if not torre_escolhida.endswith(".json"):
        torre_escolhida += ".json"
        
    # 3. Monta o caminho completo (ex: modelos_torres/torre_gigante.json)
    caminho_completo = os.path.join(pasta_modelos, torre_escolhida)
        
    # Verifica se o ficheiro existe no novo caminho
    if os.path.exists(caminho_completo):
        print(f"\n[+] Carregando parâmetros de: {caminho_completo}")
        print("[+] Iniciando motor de cálculo estrutural...\n")
        time.sleep(1)
        
        # Chama o Simulation.py passando o caminho completo!
        comando = f"python Simulation.py {caminho_completo}"
        os.system(comando)
        
        print("\n" + "✅"*58)
        print('''
   ______                 __      _     __                                 _____                                 __
  / ____/___  ____  _____/ /_  __(_)___/ /___     _________  ____ ___     / ___/__  __________  ______________  / /
 / /   / __ \/ __ \/ ___/ / / / / / __  / __ \   / ___/ __ \/ __ `__ \    \__ \/ / / / ___/ _ \/ ___/ ___/ __ \/ / 
/ /___/ /_/ / / / / /__/ / /_/ / / /_/ / /_/ /  / /__/ /_/ / / / / / /   ___/ / /_/ / /__/  __(__  |__  ) /_/ /_/  
\____/\____/_/ /_/\___/_/\__,_/_/\__,_/\____/   \___/\____/_/ /_/ /_/   /____/\__,_/\___/\___/____/____/\____(_)   
                                                                                                                   
        ''')
        print("✅"*58 + "\n")
    else:
        print(f"\n❌ ERRO: O arquivo '{torre_escolhida}' não foi encontrado na pasta '{pasta_modelos}/'.")
        print("Verifique se digitou o nome corretamente e tente de novo.\n")

if __name__ == "__main__":
    main()