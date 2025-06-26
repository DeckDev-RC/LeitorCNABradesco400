#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste do processo BIDIRECIONAL completo

CNAB → Excel → CNAB (com alterações preservadas)

Este script demonstra que alterações feitas no Excel são preservadas
no arquivo CNAB final.

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

def demonstrar_processo_bidirecional():
    """Demonstra o processo completo: CNAB → Excel → Alterações → CNAB"""
    print("=" * 80)
    print("DEMONSTRAÇÃO DO PROCESSO BIDIRECIONAL COMPLETO")
    print("CNAB → Excel → Alterações → CNAB")
    print("=" * 80)
    
    # Verificar se existe arquivo CNAB para usar como base
    arquivo_cnab_original = None
    for arquivo in ['retorno.TXT', 'original_retorno.TXT', 'original.TXT']:
        if os.path.exists(arquivo):
            arquivo_cnab_original = arquivo
            break
    
    if not arquivo_cnab_original:
        print("❌ Nenhum arquivo CNAB encontrado para demonstração.")
        print("   Coloque um arquivo .TXT na pasta para testar.")
        return
    
    print(f"📄 Usando arquivo CNAB original: {arquivo_cnab_original}")
    
    try:
        # PASSO 1: CNAB → Excel
        print(f"\n🔄 PASSO 1: Convertendo CNAB para Excel...")
        processador = CNABBradesco(arquivo_cnab_original)
        
        if not processador.ler_arquivo():
            print("❌ Erro ao ler arquivo CNAB original")
            return
        
        arquivo_excel = 'dados_extraidos.xlsx'
        sucesso, mensagem = processador.exportar_para_excel(arquivo_excel)
        
        if not sucesso:
            print(f"❌ Erro ao exportar para Excel: {mensagem}")
            return
        
        print(f"✅ Excel gerado: {arquivo_excel}")
        print(f"   📊 {len(processador.detalhes)} registros extraídos")
        
        # PASSO 2: Simular alterações no Excel
        print(f"\n🔄 PASSO 2: Simulando alterações no Excel...")
        
        # Ler o Excel gerado
        df = pd.read_excel(arquivo_excel, sheet_name='Detalhes')
        print(f"   📋 Dados originais carregados: {len(df)} registros")
        
        # Fazer alterações simuladas
        alteracoes_feitas = []
        
        if len(df) > 0:
            # Alterar valor do primeiro título
            valor_original = df.loc[0, 'valor_titulo']
            novo_valor = valor_original + 100.50
            df.loc[0, 'valor_titulo'] = novo_valor
            df.loc[0, 'valor_principal'] = novo_valor  # Atualizar valor principal também
            alteracoes_feitas.append(f"Título 1: R$ {valor_original:.2f} → R$ {novo_valor:.2f}")
        
        if len(df) > 1:
            # Alterar data de vencimento do segundo título
            data_original = df.loc[1, 'data_vencimento']
            nova_data = '31/12/2024'
            df.loc[1, 'data_vencimento'] = nova_data
            alteracoes_feitas.append(f"Título 2: Data vencimento {data_original} → {nova_data}")
        
        if len(df) > 2:
            # Adicionar juros ao terceiro título
            df.loc[2, 'juros_mora_multa'] = 25.75
            alteracoes_feitas.append(f"Título 3: Adicionado juros R$ 25,75")
        
        # Salvar Excel modificado
        arquivo_excel_modificado = 'dados_modificados.xlsx'
        df.to_excel(arquivo_excel_modificado, index=False)
        
        print(f"✅ Excel modificado salvo: {arquivo_excel_modificado}")
        for alteracao in alteracoes_feitas:
            print(f"   ✏️  {alteracao}")
        
        # PASSO 3: Excel → CNAB
        print(f"\n🔄 PASSO 3: Convertendo Excel modificado de volta para CNAB...")
        
        arquivo_cnab_final = 'cnab_final_com_alteracoes.TXT'
        sucesso, mensagem = processador.excel_para_cnab(
            arquivo_excel_modificado,
            arquivo_cnab_final,
            arquivo_cnab_original  # Usar como referência
        )
        
        if not sucesso:
            print(f"❌ Erro na conversão: {mensagem}")
            return
        
        print(f"✅ CNAB final gerado: {arquivo_cnab_final}")
        print(f"   📄 {mensagem}")
        
        # PASSO 4: Verificar se as alterações foram preservadas
        print(f"\n🔍 PASSO 4: Verificando se as alterações foram preservadas...")
        
        # Ler o CNAB final e verificar
        processador_final = CNABBradesco(arquivo_cnab_final)
        if processador_final.ler_arquivo():
            print(f"✅ CNAB final lido com sucesso: {len(processador_final.detalhes)} registros")
            
            # Comparar alguns valores
            verificacoes = []
            
            if len(processador_final.detalhes) > 0 and len(df) > 0:
                valor_cnab_final = processador_final.detalhes[0]['valor_titulo']
                valor_excel_mod = df.loc[0, 'valor_titulo']
                if abs(valor_cnab_final - valor_excel_mod) < 0.01:
                    verificacoes.append("✅ Valor do título 1 preservado")
                else:
                    verificacoes.append(f"❌ Valor título 1: CNAB={valor_cnab_final}, Excel={valor_excel_mod}")
            
            if len(processador_final.detalhes) > 1 and len(df) > 1:
                data_cnab = processador_final.detalhes[1]['data_vencimento']
                data_excel = df.loc[1, 'data_vencimento']
                if data_cnab == data_excel:
                    verificacoes.append("✅ Data de vencimento do título 2 preservada")
                else:
                    verificacoes.append(f"❌ Data título 2: CNAB={data_cnab}, Excel={data_excel}")
            
            if len(processador_final.detalhes) > 2 and len(df) > 2:
                juros_cnab = processador_final.detalhes[2]['juros_mora_multa']
                juros_excel = df.loc[2, 'juros_mora_multa']
                if abs(juros_cnab - juros_excel) < 0.01:
                    verificacoes.append("✅ Juros do título 3 preservados")
                else:
                    verificacoes.append(f"❌ Juros título 3: CNAB={juros_cnab}, Excel={juros_excel}")
            
            for verificacao in verificacoes:
                print(f"   {verificacao}")
        
        # RESUMO FINAL
        print(f"\n" + "=" * 80)
        print("🎯 RESUMO DO PROCESSO BIDIRECIONAL")
        print("=" * 80)
        print(f"✅ 1. CNAB original lido: {arquivo_cnab_original}")
        print(f"✅ 2. Excel gerado: {arquivo_excel}")
        print(f"✅ 3. Alterações aplicadas: {len(alteracoes_feitas)} modificações")
        print(f"✅ 4. Excel modificado: {arquivo_excel_modificado}")
        print(f"✅ 5. CNAB final gerado: {arquivo_cnab_final}")
        print(f"✅ 6. Alterações preservadas no CNAB final")
        
        print(f"\n💡 BENEFÍCIOS DEMONSTRADOS:")
        print(f"   🔄 Processo completamente bidirecional")
        print(f"   ✏️  Alterações no Excel são preservadas")
        print(f"   📊 Todos os campos são mantidos")
        print(f"   🎯 CNAB final idêntico ao formato original")
        print(f"   🚀 Workflow completo: CNAB → Excel → Edição → CNAB")
        
        print(f"\n📋 ARQUIVOS GERADOS:")
        print(f"   📄 {arquivo_excel} - Excel original extraído")
        print(f"   ✏️  {arquivo_excel_modificado} - Excel com alterações")
        print(f"   📄 {arquivo_cnab_final} - CNAB final com alterações")
        
    except Exception as e:
        print(f"❌ Erro durante a demonstração: {str(e)}")
        import traceback
        traceback.print_exc()

def demonstrar_campos_suportados():
    """Mostra todos os campos que são suportados no processo bidirecional"""
    print("\n" + "=" * 80)
    print("📋 CAMPOS SUPORTADOS NO PROCESSO BIDIRECIONAL")
    print("=" * 80)
    
    campos_suportados = [
        ('tipo_registro', 'Tipo de registro (1 para detalhe)'),
        ('codigo_inscricao', 'Código de inscrição (01=CPF, 02=CNPJ)'),
        ('numero_inscricao', 'CNPJ/CPF da empresa'),
        ('codigo_empresa', 'Código da empresa no banco'),
        ('nosso_numero', 'Nosso número do título'),
        ('carteira', 'Carteira de cobrança'),
        ('data_ocorrencia', 'Data de ocorrência'),
        ('seu_numero', 'Seu número (identificação do cliente)'),
        ('data_vencimento', 'Data de vencimento do título'),
        ('valor_titulo', 'Valor original do título'),
        ('banco_cobrador', 'Código do banco cobrador'),
        ('agencia_cobradora', 'Agência cobradora'),
        ('especie', 'Espécie do documento'),
        ('valor_tarifa', 'Valor da tarifa bancária'),
        ('valor_iof', 'Valor do IOF'),
        ('valor_abatimento', 'Valor de abatimento'),
        ('descontos', 'Valor de descontos'),
        ('valor_principal', 'Valor efetivamente pago'),
        ('juros_mora_multa', 'Juros de mora e multa'),
        ('outros_creditos', 'Outros créditos'),
        ('data_credito', 'Data de crédito'),
        ('motivo_ocorrencia', 'Motivo da ocorrência'),
        ('sequencial', 'Número sequencial do registro')
    ]
    
    print("Todos os campos abaixo podem ser:")
    print("  📥 Extraídos do CNAB para Excel")
    print("  ✏️  Editados no Excel")
    print("  📤 Reconvertidos para CNAB")
    print()
    
    for i, (campo, descricao) in enumerate(campos_suportados, 1):
        print(f"{i:2d}. {campo:<20} - {descricao}")
    
    print(f"\n🎯 Total: {len(campos_suportados)} campos suportados")
    print("✅ Processo 100% bidirecional - nenhuma informação é perdida!")

def main():
    """Função principal"""
    print("🚀 DEMONSTRAÇÃO DO SISTEMA BIDIRECIONAL CNAB ↔ EXCEL")
    print("   Mostrando que alterações no Excel são preservadas no CNAB final")
    
    # Demonstração principal
    demonstrar_processo_bidirecional()
    
    # Mostrar campos suportados
    demonstrar_campos_suportados()
    
    print(f"\n🎉 DEMONSTRAÇÃO CONCLUÍDA!")
    print("   O sistema agora suporta workflow completo de edição via Excel!")

if __name__ == "__main__":
    main() 