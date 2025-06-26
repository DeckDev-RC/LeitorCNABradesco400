#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste para conversão de Excel para CNAB 400 - Bradesco

Este script demonstra como usar a funcionalidade de conversão de Excel
para formato CNAB 400 do Bradesco.

Autor: Sistema CNAB Bradesco
Data: 2024
"""

import sys
import os
import pandas as pd
from datetime import datetime

# Adicionar o diretório pai ao path para importar os módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cnab_bradesco import CNABBradesco

def criar_excel_exemplo():
    """Cria um arquivo Excel de exemplo para teste"""
    dados_exemplo = [
        {
            'nosso_numero': '12345678901',
            'seu_numero': 'TESTE001',
            'valor_titulo': 1500.50,
            'data_ocorrencia': '15/12/2024',
            'data_vencimento': '20/12/2024',
            'data_credito': '15/12/2024',
            'carteira': '09'
        },
        {
            'nosso_numero': '12345678902',
            'seu_numero': 'TESTE002',
            'valor_titulo': 2300.75,
            'data_ocorrencia': '15/12/2024',
            'data_vencimento': '25/12/2024',
            'data_credito': '15/12/2024',
            'carteira': '09'
        },
        {
            'nosso_numero': '12345678903',
            'seu_numero': 'TESTE003',
            'valor_titulo': 890.00,
            'data_ocorrencia': '15/12/2024',
            'data_vencimento': '30/12/2024',
            'data_credito': '15/12/2024',
            'carteira': '09'
        }
    ]
    
    df = pd.DataFrame(dados_exemplo)
    arquivo_excel = 'exemplo_para_cnab.xlsx'
    df.to_excel(arquivo_excel, index=False)
    print(f"Arquivo Excel de exemplo criado: {arquivo_excel}")
    return arquivo_excel

def testar_conversao():
    """Testa a conversão de Excel para CNAB"""
    print("=" * 60)
    print("TESTE DE CONVERSÃO EXCEL PARA CNAB 400 - BRADESCO")
    print("=" * 60)
    
    try:
        # Criar arquivo Excel de exemplo
        arquivo_excel = criar_excel_exemplo()
        
        # Criar instância do processador
        processador = CNABBradesco("")
        
        # Definir arquivo de saída
        arquivo_cnab_saida = 'exemplo_convertido.TXT'
        
        print(f"\nConvertendo {arquivo_excel} para {arquivo_cnab_saida}...")
        
        # Executar conversão
        sucesso, mensagem = processador.excel_para_cnab(
            arquivo_excel, 
            arquivo_cnab_saida
        )
        
        if sucesso:
            print(f"✅ Conversão realizada com sucesso!")
            print(f"📄 {mensagem}")
            
            # Verificar se o arquivo foi criado
            if os.path.exists(arquivo_cnab_saida):
                with open(arquivo_cnab_saida, 'r', encoding='utf-8') as f:
                    linhas = f.readlines()
                
                print(f"\n📊 Arquivo CNAB gerado com {len(linhas)} linhas:")
                print(f"   - Header: {linhas[0][:50]}...")
                for i, linha in enumerate(linhas[1:-1], 1):
                    print(f"   - Detalhe {i}: {linha[:50]}...")
                print(f"   - Trailer: {linhas[-1][:50]}...")
                
                # Mostrar estrutura dos campos principais
                print(f"\n🔍 Verificação dos campos principais:")
                for i, linha in enumerate(linhas[1:-1], 1):
                    nosso_numero = linha[70:82].strip()
                    valor_titulo = int(linha[152:165]) / 100
                    data_ocorrencia = linha[110:116]
                    sequencial = linha[394:400]
                    
                    print(f"   Registro {i}:")
                    print(f"     - Nosso Número: {nosso_numero}")
                    print(f"     - Valor: R$ {valor_titulo:,.2f}")
                    print(f"     - Data Ocorrência: {data_ocorrencia}")
                    print(f"     - Sequencial: {sequencial}")
            
        else:
            print(f"❌ Erro na conversão: {mensagem}")
            
    except Exception as e:
        print(f"❌ Erro durante o teste: {str(e)}")
    
    print("\n" + "=" * 60)

def testar_conversao_com_referencia():
    """Testa a conversão usando um arquivo CNAB como referência"""
    print("\n" + "=" * 60)
    print("TESTE COM ARQUIVO DE REFERÊNCIA")
    print("=" * 60)
    
    # Verificar se existe algum arquivo CNAB para usar como referência
    arquivos_cnab = [f for f in os.listdir('.') if f.upper().endswith('.TXT')]
    
    if not arquivos_cnab:
        print("⚠️  Nenhum arquivo CNAB encontrado para usar como referência.")
        print("   Criando um arquivo de referência simples...")
        
        # Criar um arquivo CNAB simples como referência
        with open('referencia.TXT', 'w', encoding='utf-8') as f:
            # Header simples
            header = '0' + ' ' * 399
            f.write(header + '\n')
            
            # Trailer simples
            trailer = '9' + ' ' * 399
            f.write(trailer + '\n')
        
        arquivo_referencia = 'referencia.TXT'
    else:
        arquivo_referencia = arquivos_cnab[0]
        print(f"📄 Usando arquivo de referência: {arquivo_referencia}")
    
    try:
        # Usar o Excel criado anteriormente
        arquivo_excel = 'exemplo_para_cnab.xlsx'
        if not os.path.exists(arquivo_excel):
            arquivo_excel = criar_excel_exemplo()
        
        # Criar instância do processador
        processador = CNABBradesco("")
        
        # Definir arquivo de saída
        arquivo_cnab_saida = 'exemplo_com_referencia.TXT'
        
        print(f"\nConvertendo {arquivo_excel} para {arquivo_cnab_saida} usando referência...")
        
        # Executar conversão com referência
        sucesso, mensagem = processador.excel_para_cnab(
            arquivo_excel, 
            arquivo_cnab_saida,
            arquivo_referencia
        )
        
        if sucesso:
            print(f"✅ Conversão com referência realizada com sucesso!")
            print(f"📄 {mensagem}")
        else:
            print(f"❌ Erro na conversão com referência: {mensagem}")
            
    except Exception as e:
        print(f"❌ Erro durante o teste com referência: {str(e)}")

def main():
    """Função principal do teste"""
    print("🚀 Iniciando testes de conversão Excel para CNAB...")
    
    # Teste básico
    testar_conversao()
    
    # Teste com referência
    testar_conversao_com_referencia()
    
    print("\n✨ Testes concluídos!")
    print("\n💡 Para usar na interface gráfica:")
    print("   1. Execute: python cnab_bradesco_gui.py")
    print("   2. Clique no botão 'Excel → CNAB'")
    print("   3. Selecione seu arquivo Excel")
    print("   4. Escolha se quer usar arquivo de referência")
    print("   5. Defina onde salvar o arquivo CNAB")

if __name__ == "__main__":
    main() 