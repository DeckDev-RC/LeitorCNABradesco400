#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para gerar planilha de exemplo com mapeamentos de SEU_NUMERO
Demonstra como criar a planilha para usar com o Editor Gráfico
"""

import pandas as pd
import os

def criar_planilha_exemplo_seu_numero():
    """Cria uma planilha de exemplo com mapeamentos de SEU_NUMERO"""
    
    print("=" * 80)
    print("📊 GERADOR DE PLANILHA DE MAPEAMENTOS - SEU_NUMERO")
    print("=" * 80)
    print("Este script cria uma planilha de exemplo que pode ser usada")
    print("com o Editor Gráfico para aplicar múltiplas substituições")
    print("no campo SEU_NUMERO (apenas a parte antes da barra).")
    print("=" * 80)
    
    # Dados de exemplo para SEU_NUMERO (apenas parte antes da barra)
    # EXEMPLO ESPECÍFICO: Acrescentar letras aos números
    mapeamentos_exemplo = [
        # Casos específicos: acrescentar letra ao final
        {"PARTE_ANTES_BARRA_ATUAL": "49635", "PARTE_ANTES_BARRA_NOVA": "49635C"},
        {"PARTE_ANTES_BARRA_ATUAL": "48695", "PARTE_ANTES_BARRA_NOVA": "48695A"},
        {"PARTE_ANTES_BARRA_ATUAL": "12345", "PARTE_ANTES_BARRA_NOVA": "12345Z"},
        {"PARTE_ANTES_BARRA_ATUAL": "98765", "PARTE_ANTES_BARRA_NOVA": "98765X"},
        {"PARTE_ANTES_BARRA_ATUAL": "11111", "PARTE_ANTES_BARRA_NOVA": "11111B"},
        # Outros exemplos
        {"PARTE_ANTES_BARRA_ATUAL": "48721", "PARTE_ANTES_BARRA_NOVA": "56790"},
        {"PARTE_ANTES_BARRA_ATUAL": "48878", "PARTE_ANTES_BARRA_NOVA": "56791"},
        {"PARTE_ANTES_BARRA_ATUAL": "49001", "PARTE_ANTES_BARRA_NOVA": "56792"},
        {"PARTE_ANTES_BARRA_ATUAL": "49002", "PARTE_ANTES_BARRA_NOVA": "56793"},
        {"PARTE_ANTES_BARRA_ATUAL": "49003", "PARTE_ANTES_BARRA_NOVA": "56794"},
        # Exemplos com letras existentes
        {"PARTE_ANTES_BARRA_ATUAL": "49635C", "PARTE_ANTES_BARRA_NOVA": "67890A"},
        {"PARTE_ANTES_BARRA_ATUAL": "12345B", "PARTE_ANTES_BARRA_NOVA": "98765Z"},
        {"PARTE_ANTES_BARRA_ATUAL": "ABC123", "PARTE_ANTES_BARRA_NOVA": "XYZ789"},
        # Mais exemplos de acréscimo de letras
        {"PARTE_ANTES_BARRA_ATUAL": "55555", "PARTE_ANTES_BARRA_NOVA": "55555Y"},
        {"PARTE_ANTES_BARRA_ATUAL": "77777", "PARTE_ANTES_BARRA_NOVA": "77777W"},
    ]
    
    # Criar DataFrame
    df_mapeamentos = pd.DataFrame(mapeamentos_exemplo)
    
    # Nome do arquivo
    nome_arquivo = "exemplo_mapeamentos_seu_numero.xlsx"
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
        print("│ PARTE_ANTES_BARRA_ATUAL │ PARTE_ANTES_BARRA_NOVA   │")
        print("├─────────────────────────┼──────────────────────────┤")
        
        for i, row in df_mapeamentos.head(8).iterrows():
            atual = row['PARTE_ANTES_BARRA_ATUAL']
            novo = row['PARTE_ANTES_BARRA_NOVA']
            print(f"│ {atual:<23} │ {novo:<24} │")
        
        if len(df_mapeamentos) > 8:
            print(f"│ {'...':<23} │ {'...':<24} │")
            print(f"│ (mais {len(df_mapeamentos) - 8} mapeamentos)")
        
        print("└─────────────────────────┴──────────────────────────┘")
        
        print("\n🎯 COMO USAR:")
        print("1. Abra o Editor Gráfico no sistema CNAB")
        print("2. Na seção 'Importar Mapeamentos', selecione 'SEU_NUMERO'")
        print("3. Clique em '📁 Selecionar Planilha'")
        print(f"4. Escolha o arquivo: {nome_arquivo}")
        print("5. Verifique o preview dos mapeamentos")
        print("6. Clique em '🔄 Aplicar Mapeamentos'")
        print("7. Salve o arquivo CNAB editado")
        
        print("\n🔥 CASOS ESPECÍFICOS DE USO:")
        print("✅ Acrescentar letra: 49635 → 49635C")
        print("✅ Acrescentar letra: 48695 → 48695A") 
        print("✅ Acrescentar letra: 12345 → 12345Z")
        print("✅ Trocar números: 48721 → 56790")
        print("✅ Alfanumérico: 49635C → 67890A")
        
        print("\n💡 REGRAS IMPORTANTES:")
        print("🔹 Para valores COM barra (ex: '48695/004'):")
        print("   - Apenas a parte ANTES da barra será alterada")
        print("   - A parte DEPOIS da barra será preservada")
        print("   - '48695/004' → '56789/004' (preserva '/004')")
        
        print("\n🔹 Para valores SEM barra (ex: 'TESTE001'):")
        print("   - O valor inteiro será substituído")
        print("   - 'TESTE001' → 'NOVO001'")
        
        print("\n🔹 Se o valor corrigido não tem barra:")
        print("   - '48695/004' + 'NOVO' → 'NOVO/004'")
        print("   - A parte após a barra original é preservada")
        
        print("\n📝 PERSONALIZANDO:")
        print("- Edite a planilha para seus próprios mapeamentos")
        print("- Mantenha as colunas 'SEU_NUMERO_ATUAL' e 'SEU_NUMERO_CORRIGIDO'")
        print("- A parte antes da barra pode ter no máximo 10 caracteres")
        print("- Use apenas caracteres alfanuméricos para a parte antes da barra")
        
        print("\n⚠️ EXEMPLOS DE TRANSFORMAÇÃO:")
        print("📋 Valor original: '12345/999'")
        print("📋 Valor corrigido na planilha: '67890'")
        print("📋 Resultado final: '67890/999' (preserva '/999')")
        print()
        print("📋 Valor original: 'TESTE001'")
        print("📋 Valor corrigido na planilha: 'NOVO001'")
        print("📋 Resultado final: 'NOVO001' (sem barra)")
        
        return True, caminho_arquivo
        
    except Exception as e:
        print(f"\n❌ Erro ao criar planilha: {str(e)}")
        return False, None

def criar_planilha_personalizada_seu_numero():
    """Permite ao usuário criar uma planilha personalizada para SEU_NUMERO"""
    
    print("\n" + "=" * 80)
    print("✏️ CRIADOR DE PLANILHA PERSONALIZADA - SEU_NUMERO")
    print("=" * 80)
    
    mapeamentos = []
    
    print("Digite os mapeamentos (pressione Enter em 'Atual' para finalizar):")
    print("Formato: SEU_NUMERO_ATUAL → SEU_NUMERO_CORRIGIDO")
    print("Lembre-se: apenas a parte ANTES da barra será alterada!")
    print("-" * 60)
    
    while True:
        try:
            atual = input("Seu Número Atual (ou Enter para finalizar): ").strip()
            if not atual:
                break
            
            # Validar número atual
            if len(atual) > 10:
                print("❌ Seu Número muito longo. Use até 10 caracteres.")
                continue
            
            corrigido = input(f"Seu Número Corrigido para {atual}: ").strip()
            
            # Validar número corrigido (apenas a parte antes da barra)
            if '/' in corrigido:
                parte_antes = corrigido.split('/')[0]
            else:
                parte_antes = corrigido
            
            if len(parte_antes) > 10:
                print("❌ A parte antes da barra no Seu Número deve ter no máximo 10 caracteres.")
                continue
            
            mapeamentos.append({
                "PARTE_ANTES_BARRA_ATUAL": atual,
                "PARTE_ANTES_BARRA_NOVA": corrigido
            })
            
            # Mostrar como ficará o resultado
            if '/' in atual:
                parte_depois = '/' + atual.split('/', 1)[1]
                if '/' in corrigido:
                    resultado = corrigido.split('/')[0] + parte_depois
                else:
                    resultado = corrigido + parte_depois
                print(f"✅ Mapeamento adicionado: {atual} → {resultado}")
            else:
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
    nome_arquivo = input(f"\nNome do arquivo (padrão: mapeamentos_seu_numero_personalizados.xlsx): ").strip()
    if not nome_arquivo:
        nome_arquivo = "mapeamentos_seu_numero_personalizados.xlsx"
    
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
    """Função principal do script"""
    print("🚀 Iniciando gerador de planilhas de mapeamento para SEU_NUMERO...")
    
    while True:
        print("\n" + "=" * 80)
        print("📊 GERADOR DE PLANILHAS - SEU_NUMERO")
        print("=" * 80)
        print("Escolha uma opção:")
        print("1. Criar planilha de exemplo")
        print("2. Criar planilha personalizada")
        print("0. Sair")
        print("-" * 80)
        
        try:
            opcao = input("Digite sua opção: ").strip()
            
            if opcao == "0":
                print("\n👋 Encerrando programa. Obrigado!")
                break
            elif opcao == "1":
                sucesso, arquivo = criar_planilha_exemplo_seu_numero()
                if sucesso:
                    print(f"\n🎯 Planilha de exemplo criada: {arquivo}")
            elif opcao == "2":
                sucesso, arquivo = criar_planilha_personalizada_seu_numero()
                if sucesso:
                    print(f"\n🎯 Planilha personalizada criada: {arquivo}")
            else:
                print("❌ Opção inválida. Digite 1, 2 ou 0.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Programa interrompido pelo usuário.")
            break
    
    print("\n" + "=" * 80)
    print("✨ PROGRAMA FINALIZADO!")
    print("=" * 80)
    print("\n💡 Dicas finais:")
    print("- Use as planilhas geradas no Editor Gráfico do sistema CNAB")
    print("- Selecione 'SEU_NUMERO' no tipo de mapeamento")
    print("- Apenas a parte antes da barra será alterada")
    print("- A parte após a barra será sempre preservada")

if __name__ == "__main__":
    main() 