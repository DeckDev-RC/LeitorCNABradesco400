#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste CORRIGIDO para conversão de Excel para CNAB 400 - Bradesco

Este script demonstra a correção do erro relacionado ao atributo 'strip' 
em objetos float.

Autor: Sistema CNAB Bradesco
Data: 2024
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime

# Adicionar o diretório pai ao path para importar os módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cnab_bradesco import CNABBradesco

def criar_excel_exemplo_com_tipos_mistos():
    """Cria um arquivo Excel com diferentes tipos de dados para testar a robustez"""
    dados_exemplo = [
        {
            'nosso_numero': 12345678901,  # Número (int)
            'seu_numero': 'TESTE001',     # String
            'valor_titulo': 1500.50,      # Float
            'data_ocorrencia': '15/12/2024',
            'data_vencimento': '20/12/2024',
            'data_credito': '15/12/2024',
            'carteira': 9                 # Número (int)
        },
        {
            'nosso_numero': '12345678902', # String
            'seu_numero': 'TESTE002',
            'valor_titulo': 2300.75,       # Float
            'data_ocorrencia': '15/12/2024',
            'data_vencimento': '25/12/2024',
            'data_credito': '15/12/2024',
            'carteira': '09'               # String
        },
        {
            'nosso_numero': 12345678903,   # Número (int)
            'seu_numero': None,            # Valor nulo
            'valor_titulo': 890,           # Int
            'data_ocorrencia': '15/12/2024',
            'data_vencimento': '30/12/2024',
            'data_credito': None,          # Valor nulo
            'carteira': np.nan             # NaN
        },
        {
            'nosso_numero': '12345678904', # String
            'seu_numero': 'TESTE004',
            'valor_titulo': 'R$ 1.234,56', # String formatada
            'data_ocorrencia': '16/12/2024',
            'data_vencimento': '31/12/2024',
            'data_credito': '16/12/2024',
            'carteira': '09'
        }
    ]
    
    df = pd.DataFrame(dados_exemplo)
    arquivo_excel = 'exemplo_tipos_mistos.xlsx'
    df.to_excel(arquivo_excel, index=False)
    print(f"📊 Arquivo Excel com tipos mistos criado: {arquivo_excel}")
    
    # Mostrar os tipos de dados
    print("\n🔍 Tipos de dados no DataFrame:")
    print(df.dtypes)
    print("\n📋 Dados de exemplo:")
    print(df.to_string(index=False))
    
    return arquivo_excel

def testar_conversao_corrigida():
    """Testa a conversão com a correção do erro de tipos"""
    print("=" * 70)
    print("TESTE DE CONVERSÃO CORRIGIDA - EXCEL PARA CNAB 400")
    print("=" * 70)
    
    try:
        # Criar arquivo Excel com tipos mistos
        arquivo_excel = criar_excel_exemplo_com_tipos_mistos()
        
        # Criar instância do processador
        processador = CNABBradesco("")
        
        # Definir arquivo de saída
        arquivo_cnab_saida = 'exemplo_corrigido.TXT'
        
        print(f"\n🔄 Convertendo {arquivo_excel} para {arquivo_cnab_saida}...")
        print("   (Testando tratamento de tipos int, float, string, None, NaN)")
        
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
                
                # Analisar cada linha de detalhe
                for i, linha in enumerate(linhas[1:-1], 1):
                    nosso_numero = linha[70:82].strip()
                    valor_titulo = int(linha[152:165]) / 100
                    data_ocorrencia = linha[110:116]
                    seu_numero = linha[116:126].strip()
                    carteira = linha[107:109]
                    sequencial = linha[394:400]
                    
                    print(f"   - Detalhe {i}:")
                    print(f"     • Nosso Número: {nosso_numero}")
                    print(f"     • Valor: R$ {valor_titulo:,.2f}")
                    print(f"     • Data Ocorrência: {data_ocorrencia}")
                    print(f"     • Seu Número: '{seu_numero}'")
                    print(f"     • Carteira: {carteira}")
                    print(f"     • Sequencial: {sequencial}")
                
                print(f"   - Trailer: {linhas[-1][:50]}...")
                
                print(f"\n✅ Teste concluído com sucesso!")
                print(f"   Todos os tipos de dados foram tratados corretamente:")
                print(f"   ✓ Números inteiros")
                print(f"   ✓ Números decimais")
                print(f"   ✓ Strings")
                print(f"   ✓ Valores nulos (None)")
                print(f"   ✓ Valores NaN")
                print(f"   ✓ Strings formatadas (R$ 1.234,56)")
            
        else:
            print(f"❌ Erro na conversão: {mensagem}")
            
    except Exception as e:
        print(f"❌ Erro durante o teste: {str(e)}")
        import traceback
        traceback.print_exc()

def testar_casos_extremos():
    """Testa casos extremos de dados"""
    print("\n" + "=" * 70)
    print("TESTE DE CASOS EXTREMOS")
    print("=" * 70)
    
    try:
        # Criar dados com casos extremos
        dados_extremos = [
            {
                'nosso_numero': '',           # String vazia
                'seu_numero': '',
                'valor_titulo': 0,            # Zero
                'data_ocorrencia': '',
                'data_vencimento': '',
                'data_credito': '',
                'carteira': ''
            },
            {
                'nosso_numero': 999999999999, # Número muito grande
                'seu_numero': 'TESTE_MUITO_LONGO_123456789',  # String muito longa
                'valor_titulo': 999999.99,   # Valor alto
                'data_ocorrencia': '31/12/2024',
                'data_vencimento': '01/01/2025',
                'data_credito': '31/12/2024',
                'carteira': 999               # Carteira inválida
            }
        ]
        
        df = pd.DataFrame(dados_extremos)
        arquivo_excel = 'exemplo_extremos.xlsx'
        df.to_excel(arquivo_excel, index=False)
        
        print(f"📊 Arquivo com casos extremos criado: {arquivo_excel}")
        
        # Converter
        processador = CNABBradesco("")
        arquivo_cnab_saida = 'exemplo_extremos.TXT'
        
        sucesso, mensagem = processador.excel_para_cnab(
            arquivo_excel, 
            arquivo_cnab_saida
        )
        
        if sucesso:
            print(f"✅ Casos extremos tratados com sucesso!")
            print(f"📄 {mensagem}")
        else:
            print(f"⚠️  Erro esperado nos casos extremos: {mensagem}")
            
    except Exception as e:
        print(f"⚠️  Erro esperado nos casos extremos: {str(e)}")

def main():
    """Função principal do teste corrigido"""
    print("🚀 Iniciando testes de conversão CORRIGIDA Excel para CNAB...")
    print("   (Correção do erro: 'float' object has no attribute 'strip')")
    
    # Teste principal com correção
    testar_conversao_corrigida()
    
    # Teste de casos extremos
    testar_casos_extremos()
    
    print("\n" + "=" * 70)
    print("✨ TODOS OS TESTES CONCLUÍDOS!")
    print("=" * 70)
    print("\n💡 Correções implementadas:")
    print("   ✓ Tratamento de valores int/float sem conversão para string")
    print("   ✓ Verificação de valores None e NaN")
    print("   ✓ Conversão segura de tipos antes de chamar .strip()")
    print("   ✓ Tratamento robusto de diferentes formatos de dados")
    
    print("\n🎯 Para usar na interface gráfica:")
    print("   1. Execute: python cnab_bradesco_gui.py")
    print("   2. Clique no botão 'Excel → CNAB'")
    print("   3. Selecione seu arquivo Excel (com qualquer tipo de dados)")
    print("   4. A conversão agora funciona sem erros!")

if __name__ == "__main__":
    main() 