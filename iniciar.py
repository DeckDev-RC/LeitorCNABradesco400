import os
import sys
import subprocess
import platform

def verificar_dependencias():
    """Verifica se as dependências estão instaladas"""
    try:
        import pandas
        import PyQt5
        import tabulate
        return True
    except ImportError as e:
        print(f"Erro: Dependência não encontrada: {str(e)}")
        return False

def instalar_dependencias():
    """Instala as dependências necessárias"""
    print("Instalando dependências...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Dependências instaladas com sucesso!")
        return True
    except Exception as e:
        print(f"Erro ao instalar dependências: {str(e)}")
        return False

def iniciar_interface():
    """Inicia a interface gráfica"""
    print("Iniciando interface gráfica...")
    
    try:
        if platform.system() == "Windows":
            os.system('start pythonw cnab_bradesco_gui.py')
        else:
            os.system('python cnab_bradesco_gui.py &')
        return True
    except Exception as e:
        print(f"Erro ao iniciar interface: {str(e)}")
        return False

def limpar_tela():
    """Limpa a tela do terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_menu():
    """Exibe o menu principal do sistema"""
    limpar_tela()
    print("=" * 70)
    print("  SISTEMA DE PROCESSAMENTO DE ARQUIVOS CNAB 400 - BRADESCO (237)")
    print("=" * 70)
    print("\nEscolha uma opção:")
    print("1. Processar um arquivo")
    print("2. Processar múltiplos arquivos (lote)")
    print("3. Abrir interface gráfica")
    print("4. Sobre o sistema")
    print("0. Sair")
    print("\n" + "=" * 70)

def sobre_sistema():
    """Exibe informações sobre o sistema"""
    limpar_tela()
    print("=" * 70)
    print("  SOBRE O SISTEMA DE PROCESSAMENTO CNAB 400 - BRADESCO")
    print("=" * 70)
    print("\nVersão: 2.0")
    print("Desenvolvido para leitura e processamento de arquivos CNAB 400 do Bradesco (237)")
    print("\nFuncionalidades:")
    print("- Leitura e interpretação de arquivos CNAB 400 de retorno")
    print("- Extração de dados de header, detalhes e trailer")
    print("- Interface gráfica para visualização dos dados")
    print("- Exportação para CSV e Excel (XLSX)")
    print("- Geração de arquivo CNAB de retorno sem juros/multa")
    print("- Processamento em lote de múltiplos arquivos")
    print("- Formatação monetária no padrão brasileiro (R$ 1.234,56)")
    
    print("\nPressione ENTER para voltar ao menu principal...")
    input()

def iniciar():
    """Função principal que inicia o sistema"""
    while True:
        mostrar_menu()
        opcao = input("\nDigite a opção desejada: ")
        
        if opcao == "1":
            # Processar um arquivo
            limpar_tela()
            print("Iniciando processamento de arquivo único...")
            subprocess.run([sys.executable, "cnab_bradesco.py"])
            print("\nPressione ENTER para voltar ao menu principal...")
            input()
        
        elif opcao == "2":
            # Processar múltiplos arquivos
            limpar_tela()
            print("Iniciando processamento em lote...")
            subprocess.run([sys.executable, "processar_lote.py"])
            print("\nPressione ENTER para voltar ao menu principal...")
            input()
        
        elif opcao == "3":
            # Abrir interface gráfica
            limpar_tela()
            print("Iniciando interface gráfica...")
            subprocess.run([sys.executable, "cnab_bradesco_gui.py"])
            print("\nPressione ENTER para voltar ao menu principal...")
            input()
        
        elif opcao == "4":
            # Sobre o sistema
            sobre_sistema()
        
        elif opcao == "0":
            # Sair
            limpar_tela()
            print("Encerrando o sistema. Obrigado por utilizar!")
            sys.exit(0)
        
        else:
            print("\nOpção inválida! Pressione ENTER para tentar novamente...")
            input()

if __name__ == "__main__":
    iniciar() 