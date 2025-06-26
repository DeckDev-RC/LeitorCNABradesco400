#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de demonstração do Editor Interativo de CNAB
Permite alterações pontuais em dados CNAB com interface amigável
"""

import sys
import os

# Adicionar o diretório pai ao path para importar o módulo
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cnab_bradesco import CNABBradesco

def demonstrar_editor_interativo():
    """Demonstra o uso do editor interativo"""
    print("=" * 80)
    print("🔧 DEMONSTRAÇÃO DO EDITOR INTERATIVO DE CNAB")
    print("=" * 80)
    print("Este script demonstra como usar o editor interativo para")
    print("fazer alterações pontuais em arquivos CNAB.")
    print("=" * 80)
    
    # Verificar se existe arquivo CNAB para teste
    arquivos_cnab = [f for f in os.listdir('.') if f.upper().endswith('.TXT')]
    
    if not arquivos_cnab:
        print("❌ Nenhum arquivo CNAB (.TXT) encontrado no diretório atual.")
        print("💡 Coloque um arquivo CNAB na pasta do projeto e tente novamente.")
        return
    
    print("\n📁 ARQUIVOS CNAB DISPONÍVEIS:")
    for i, arquivo in enumerate(arquivos_cnab, 1):
        tamanho = os.path.getsize(arquivo)
        print(f"{i:2d}. {arquivo:<30} ({tamanho:,} bytes)")
    
    # Selecionar arquivo
    while True:
        try:
            escolha = input(f"\n🎯 Escolha um arquivo (1-{len(arquivos_cnab)}) ou 'q' para sair: ").strip()
            
            if escolha.lower() == 'q':
                print("👋 Encerrando demonstração...")
                return
            
            indice = int(escolha) - 1
            if 0 <= indice < len(arquivos_cnab):
                arquivo_escolhido = arquivos_cnab[indice]
                break
            else:
                print(f"❌ Número inválido. Digite entre 1 e {len(arquivos_cnab)}")
        except ValueError:
            print("❌ Digite um número válido ou 'q' para sair.")
    
    print(f"\n📄 Arquivo selecionado: {arquivo_escolhido}")
    print("📊 Carregando arquivo...")
    
    try:
        # Criar instância do processador
        processador = CNABBradesco(arquivo_escolhido)
        
        # Carregar arquivo
        sucesso = processador.ler_arquivo()
        
        if not sucesso:
            print("❌ Erro ao carregar o arquivo CNAB.")
            return
        
        print(f"✅ Arquivo carregado com sucesso!")
        print(f"📊 {len(processador.detalhes)} registros encontrados")
        
        # Mostrar informações básicas
        print("\n📋 RESUMO DO ARQUIVO:")
        print("-" * 50)
        
        if len(processador.detalhes) > 0:
            total_valor = sum(d.get('valor_titulo', 0) for d in processador.detalhes)
            print(f"💰 Valor total dos títulos: {processador.formatar_moeda(total_valor)}")
            print(f"📅 Primeiro vencimento: {processador.detalhes[0].get('data_vencimento', 'N/A')}")
            if len(processador.detalhes) > 1:
                print(f"📅 Último vencimento: {processador.detalhes[-1].get('data_vencimento', 'N/A')}")
        
        print("-" * 50)
        
        # Explicar funcionalidades
        print("\n🔧 FUNCIONALIDADES DO EDITOR INTERATIVO:")
        print("1. 📋 Listar e visualizar todos os registros")
        print("2. 🔍 Buscar registros por nosso número ou seu número")
        print("3. ✏️  Editar campos individuais de qualquer registro")
        print("4. 💰 Aplicar alterações em lote (valores, percentuais)")
        print("5. 📅 Modificar datas em massa (vencimento, crédito)")
        print("6. 📊 Acompanhar resumo das alterações feitas")
        print("7. 💾 Salvar um novo arquivo CNAB com as modificações")
        
        print("\n🎯 CASOS DE USO PRÁTICOS:")
        print("• Corrigir valores de títulos específicos")
        print("• Aplicar reajustes percentuais em massa")
        print("• Postergar vencimentos por X dias")
        print("• Zerar juros/multa de todos os títulos")
        print("• Alterar datas de crédito para nova data")
        print("• Buscar e corrigir registros específicos")
        
        # Iniciar editor
        print("\n" + "=" * 50)
        input("⏸  Pressione Enter para iniciar o Editor Interativo...")
        print("=" * 50)
        
        # Executar editor interativo
        resultado = processador.editor_interativo()
        
        if resultado:
            print("\n✅ Editor concluído com sucesso!")
            print("📄 Um novo arquivo CNAB foi gerado com suas alterações.")
        else:
            print("\n📝 Editor encerrado sem salvar alterações.")
        
        print("\n" + "=" * 80)
        print("🎉 DEMONSTRAÇÃO CONCLUÍDA")
        print("=" * 80)
        print("O Editor Interativo permite fazer alterações pontuais")
        print("de forma rápida e segura, mantendo o formato CNAB.")
        print("=" * 80)
        
    except Exception as e:
        print(f"❌ Erro durante a demonstração: {str(e)}")
        import traceback
        print(f"🔍 Detalhes do erro: {traceback.format_exc()}")

def mostrar_dicas():
    """Mostra dicas de uso do editor"""
    print("\n💡 DICAS PARA USAR O EDITOR INTERATIVO:")
    print("-" * 60)
    print("🔸 Use a busca (opção 2) para encontrar registros específicos")
    print("🔸 As edições em lote (opção 4 e 5) são úteis para mudanças globais")
    print("🔸 Sempre verifique o resumo (opção 7) antes de salvar")
    print("🔸 O arquivo original nunca é modificado - sempre gera novo arquivo")
    print("🔸 Valores podem ser digitados com R$, pontos e vírgulas")
    print("🔸 Datas devem seguir o formato DD/MM/AAAA")
    print("🔸 Registros alterados são marcados com status 'Alterado'")
    print("-" * 60)

if __name__ == "__main__":
    try:
        mostrar_dicas()
        demonstrar_editor_interativo()
    except KeyboardInterrupt:
        print("\n\n👋 Demonstração interrompida pelo usuário.")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {str(e)}") 