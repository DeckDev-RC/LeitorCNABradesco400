#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para gerar planilha de exemplo com mapeamentos de NOSSO_NUMERO
Demonstra como criar a planilha para usar com o Editor Gráfico
"""

import pandas as pd
import os

def criar_planilha_exemplo():
    """Cria uma planilha de exemplo com mapeamentos"""
    
    print("=" * 80)
    print("📊 GERADOR DE PLANILHA DE MAPEAMENTOS - EXEMPLO")
    print("=" * 80)
    print("Este script cria uma planilha de exemplo que pode ser usada")
    print("com o Editor Gráfico para aplicar múltiplas substituições.")
    print("=" * 80)
    
    # Dados de exemplo (incluindo alguns com letras)
    mapeamentos_exemplo = [
        {"NOSSO_NUMERO_ATUAL": "000000064319", "NOSSO_NUMERO_CORRIGIDO": "100000064319"},
        {"NOSSO_NUMERO_ATUAL": "000000064572", "NOSSO_NUMERO_CORRIGIDO": "100000064572"},
        {"NOSSO_NUMERO_ATUAL": "000000065471", "NOSSO_NUMERO_CORRIGIDO": "100000065471"},
        {"NOSSO_NUMERO_ATUAL": "000000065501", "NOSSO_NUMERO_CORRIGIDO": "100000065501"},
        {"NOSSO_NUMERO_ATUAL": "000000066516", "NOSSO_NUMERO_CORRIGIDO": "100000066516"},
        {"NOSSO_NUMERO_ATUAL": "000000066468", "NOSSO_NUMERO_CORRIGIDO": "100000066468"},
        {"NOSSO_NUMERO_ATUAL": "000000067210", "NOSSO_NUMERO_CORRIGIDO": "100000067210"},
        {"NOSSO_NUMERO_ATUAL": "000000067300", "NOSSO_NUMERO_CORRIGIDO": "100000067300"},
        {"NOSSO_NUMERO_ATUAL": "000000067385", "NOSSO_NUMERO_CORRIGIDO": "100000067385"},
        {"NOSSO_NUMERO_ATUAL": "000000067644", "NOSSO_NUMERO_CORRIGIDO": "100000067644"},
        {"NOSSO_NUMERO_ATUAL": "000000067458", "NOSSO_NUMERO_CORRIGIDO": "100000067458"},
        {"NOSSO_NUMERO_ATUAL": "000000067490", "NOSSO_NUMERO_CORRIGIDO": "100000067490"},
        {"NOSSO_NUMERO_ATUAL": "000000067539", "NOSSO_NUMERO_CORRIGIDO": "100000067539"},
        {"NOSSO_NUMERO_ATUAL": "000000067571", "NOSSO_NUMERO_CORRIGIDO": "100000067571"},
        {"NOSSO_NUMERO_ATUAL": "000000067589", "NOSSO_NUMERO_CORRIGIDO": "100000067589"},
        {"NOSSO_NUMERO_ATUAL": "000000068489", "NOSSO_NUMERO_CORRIGIDO": "100000068489"},
        {"NOSSO_NUMERO_ATUAL": "000000068241", "NOSSO_NUMERO_CORRIGIDO": "100000068241"},
        {"NOSSO_NUMERO_ATUAL": "000000067954", "NOSSO_NUMERO_CORRIGIDO": "100000067954"},
        {"NOSSO_NUMERO_ATUAL": "000000068748", "NOSSO_NUMERO_CORRIGIDO": "100000068748"},
        {"NOSSO_NUMERO_ATUAL": "00000006646P", "NOSSO_NUMERO_CORRIGIDO": "10000006646P"}  # Exemplo com letra
    ]
    
    # Criar DataFrame
    df_mapeamentos = pd.DataFrame(mapeamentos_exemplo)
    
    # Nome do arquivo
    nome_arquivo = "exemplo_mapeamentos_nosso_numero.xlsx"
    caminho_arquivo = os.path.join("..", nome_arquivo)
    
    # Salvar planilha
    try:
        df_mapeamentos.to_excel(caminho_arquivo, index=False)
        
        print(f"\n✅ Planilha de exemplo criada com sucesso!")
        print(f"📄 Arquivo: {nome_arquivo}")
        print(f"📍 Localização: {os.path.abspath(caminho_arquivo)}")
        print(f"📊 Total de mapeamentos: {len(df_mapeamentos)}")
        
        print("\n📋 ESTRUTURA DA PLANILHA:")
        print("┌─────────────────────────┬──────────────────────────┐")
        print("│ NOSSO_NUMERO_ATUAL      │ NOSSO_NUMERO_CORRIGIDO   │")
        print("├─────────────────────────┼──────────────────────────┤")
        
        for i, row in df_mapeamentos.head(5).iterrows():
            atual = row['NOSSO_NUMERO_ATUAL']
            corrigido = row['NOSSO_NUMERO_CORRIGIDO']
            print(f"│ {atual:<23} │ {corrigido:<24} │")
        
        if len(df_mapeamentos) > 5:
            print(f"│ {'...':<23} │ {'...':<24} │")
            print(f"│ (mais {len(df_mapeamentos) - 5} mapeamentos)")
        
        print("└─────────────────────────┴──────────────────────────┘")
        
        print("\n🎯 COMO USAR:")
        print("1. Abra o Editor Gráfico no sistema CNAB")
        print("2. Clique em '📁 Selecionar Planilha'")
        print(f"3. Escolha o arquivo: {nome_arquivo}")
        print("4. Verifique o preview dos mapeamentos")
        print("5. Clique em '🔄 Aplicar Mapeamentos'")
        print("6. Salve o arquivo CNAB editado")
        
        print("\n💡 EXEMPLO DE APLICAÇÃO:")
        print("Este exemplo adiciona o prefixo '1' a todos os nossos números,")
        print("transformando '000000064319' em '100000064319'.")
        
        print("\n📝 PERSONALIZANDO:")
        print("- Edite a planilha para seus próprios mapeamentos")
        print("- Mantenha as colunas 'NOSSO_NUMERO_ATUAL' e 'NOSSO_NUMERO_CORRIGIDO'")
        print("- Os números podem ter no máximo 12 caracteres")
        print("- Use letras e números (alfanumérico, sem símbolos especiais)")
        
        return True, caminho_arquivo
        
    except Exception as e:
        print(f"\n❌ Erro ao criar planilha: {str(e)}")
        return False, None

def criar_planilha_personalizada():
    """Permite ao usuário criar uma planilha personalizada"""
    
    print("\n" + "=" * 80)
    print("✏️ CRIADOR DE PLANILHA PERSONALIZADA")
    print("=" * 80)
    
    mapeamentos = []
    
    print("Digite os mapeamentos (pressione Enter em 'Atual' para finalizar):")
    print("Formato: NOSSO_NUMERO_ATUAL → NOSSO_NUMERO_CORRIGIDO")
    print("-" * 60)
    
    while True:
        try:
            atual = input("Nosso Número Atual (ou Enter para finalizar): ").strip()
            if not atual:
                break
            
            # Validar número atual
            if len(atual) > 12 or not atual.replace(' ', '').isalnum():
                print("❌ Número inválido. Use apenas letras e números com até 12 caracteres.")
                continue
            
            corrigido = input(f"Nosso Número Corrigido para {atual}: ").strip()
            
            # Validar número corrigido
            if len(corrigido) > 12 or not corrigido.replace(' ', '').isalnum():
                print("❌ Número inválido. Use apenas letras e números com até 12 caracteres.")
                continue
            
            mapeamentos.append({
                "NOSSO_NUMERO_ATUAL": atual,
                "NOSSO_NUMERO_CORRIGIDO": corrigido
            })
            
            print(f"✅ Mapeamento adicionado: {atual} → {corrigido}")
            
        except KeyboardInterrupt:
            print("\n\n👋 Operação cancelada pelo usuário.")
            return False, None
    
    if not mapeamentos:
        print("❌ Nenhum mapeamento foi adicionado.")
        return False, None
    
    # Criar DataFrame
    df_mapeamentos = pd.DataFrame(mapeamentos)
    
    # Nome do arquivo
    nome_arquivo = input(f"\nNome do arquivo (padrão: mapeamentos_personalizados.xlsx): ").strip()
    if not nome_arquivo:
        nome_arquivo = "mapeamentos_personalizados.xlsx"
    
    if not nome_arquivo.endswith('.xlsx'):
        nome_arquivo += '.xlsx'
    
    caminho_arquivo = os.path.join("..", nome_arquivo)
    
    # Salvar planilha
    try:
        df_mapeamentos.to_excel(caminho_arquivo, index=False)
        
        print(f"\n✅ Planilha personalizada criada com sucesso!")
        print(f"📄 Arquivo: {nome_arquivo}")
        print(f"📍 Localização: {os.path.abspath(caminho_arquivo)}")
        print(f"📊 Total de mapeamentos: {len(df_mapeamentos)}")
        
        return True, caminho_arquivo
        
    except Exception as e:
        print(f"\n❌ Erro ao criar planilha: {str(e)}")
        return False, None

def main():
    """Função principal"""
    
    print("🎯 ESCOLHA UMA OPÇÃO:")
    print("1. Criar planilha de exemplo (automática)")
    print("2. Criar planilha personalizada (manual)")
    print("3. Sair")
    
    while True:
        try:
            opcao = input("\n🎯 Digite sua escolha (1-3): ").strip()
            
            if opcao == '1':
                sucesso, arquivo = criar_planilha_exemplo()
                if sucesso:
                    print(f"\n🎉 Planilha criada com sucesso: {arquivo}")
                break
                
            elif opcao == '2':
                sucesso, arquivo = criar_planilha_personalizada()
                if sucesso:
                    print(f"\n🎉 Planilha criada com sucesso: {arquivo}")
                break
                
            elif opcao == '3':
                print("\n👋 Encerrando...")
                break
                
            else:
                print("❌ Opção inválida. Digite 1, 2 ou 3.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Programa encerrado pelo usuário.")
            break
        except Exception as e:
            print(f"\n❌ Erro inesperado: {str(e)}")
            break

if __name__ == "__main__":
    main() 