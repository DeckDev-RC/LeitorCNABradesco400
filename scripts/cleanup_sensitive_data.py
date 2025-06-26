#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de limpeza de dados sensíveis
Remove arquivos e dados sensíveis antes de commits no Git
"""

import os
import shutil
import glob
import re
from pathlib import Path

def limpar_arquivos_sensíveis():
    """Remove arquivos com dados sensíveis"""
    
    print("🧹 Iniciando limpeza de dados sensíveis...")
    
    # Padrões de arquivos sensíveis
    padroes_sensíveis = [
        "*.TXT",
        "*.txt", 
        "*AMR*COMERCIO*",
        "*MEDICAMENTOS*",
        "*PERFUMARIA*",
        "*.xlsx",
        "*.xls",
        "*_retorno.*",
        "*_editado.*",
        "*_sem_juros.*",
        "*_processado.*"
    ]
    
    # Exceções (arquivos que podem ser mantidos)
    excecoes = [
        "exemplo_*.txt",
        "template_*.txt",
        "exemplo_*.xlsx",
        "template_*.xlsx"
    ]
    
    arquivos_removidos = 0
    
    # Procurar e remover arquivos sensíveis
    for padrao in padroes_sensíveis:
        for arquivo in glob.glob(padrao, recursive=True):
            # Verificar se não é uma exceção
            eh_excecao = any(
                re.match(exc.replace("*", ".*"), os.path.basename(arquivo))
                for exc in excecoes
            )
            
            if not eh_excecao and os.path.exists(arquivo):
                try:
                    os.remove(arquivo)
                    print(f"   ❌ Removido: {arquivo}")
                    arquivos_removidos += 1
                except Exception as e:
                    print(f"   ⚠️  Erro ao remover {arquivo}: {e}")
    
    # Remover pastas específicas
    pastas_sensíveis = [
        "__pycache__",
        "build",
        "dist",
        ".pytest_cache",
        "*.egg-info"
    ]
    
    for padrao in pastas_sensíveis:
        for pasta in glob.glob(padrao, recursive=True):
            if os.path.isdir(pasta):
                try:
                    shutil.rmtree(pasta)
                    print(f"   📁 Pasta removida: {pasta}")
                    arquivos_removidos += 1
                except Exception as e:
                    print(f"   ⚠️  Erro ao remover pasta {pasta}: {e}")
    
    print(f"\n✅ Limpeza concluída! {arquivos_removidos} item(s) removido(s)")

def verificar_dados_sensíveis_codigo():
    """Verifica se há dados sensíveis no código"""
    
    print("\n🔍 Verificando dados sensíveis no código...")
    
    # Padrões sensíveis no código
    padroes_codigo = [
        r'\d{14}',  # CNPJs (14 dígitos)
        r'AMR.*COMERCIO.*MEDICAMENTOS',  # Nome da empresa
        r'PERFUMARIA',
        r'50670573000109',  # CNPJ específico
        r'37448359000136'   # Outro CNPJ
    ]
    
    # Arquivos de código para verificar
    arquivos_codigo = [
        "*.py",
        "*.md",
        "*.txt"
    ]
    
    problemas_encontrados = 0
    
    for padrao_arquivo in arquivos_codigo:
        for arquivo in glob.glob(padrao_arquivo, recursive=True):
            # Pular arquivos de exemplo
            if "exemplo_" in arquivo or "template_" in arquivo:
                continue
            
            try:
                with open(arquivo, 'r', encoding='utf-8') as f:
                    conteudo = f.read()
                    
                for i, linha in enumerate(conteudo.split('\n'), 1):
                    for padrao in padroes_codigo:
                        if re.search(padrao, linha, re.IGNORECASE):
                            print(f"   ⚠️  {arquivo}:{i} - Possível dado sensível: {linha.strip()[:50]}...")
                            problemas_encontrados += 1
                            
            except Exception as e:
                print(f"   ❌ Erro ao ler {arquivo}: {e}")
    
    if problemas_encontrados == 0:
        print("   ✅ Nenhum dado sensível encontrado no código!")
    else:
        print(f"\n   ⚠️  {problemas_encontrados} possível(is) problema(s) encontrado(s)")

def criar_gitignore_adicional():
    """Adiciona entradas extras ao .gitignore se necessário"""
    
    print("\n📝 Verificando .gitignore...")
    
    entradas_extras = [
        "# Dados específicos do projeto",
        "**/dados_reais/",
        "**/*_backup.*",
        "**/*_temp.*",
        "# Logs específicos",
        "**/*.log.*",
        "# Configurações locais",
        "local_config.py",
        "config_local.ini"
    ]
    
    if os.path.exists('.gitignore'):
        with open('.gitignore', 'r', encoding='utf-8') as f:
            conteudo_atual = f.read()
        
        entradas_faltando = [
            entrada for entrada in entradas_extras 
            if entrada not in conteudo_atual and not entrada.startswith('#')
        ]
        
        if entradas_faltando:
            with open('.gitignore', 'a', encoding='utf-8') as f:
                f.write('\n# Entradas adicionais de segurança\n')
                for entrada in entradas_faltando:
                    f.write(f"{entrada}\n")
            print(f"   ✅ {len(entradas_faltando)} entrada(s) adicionada(s) ao .gitignore")
        else:
            print("   ✅ .gitignore já está atualizado")
    else:
        print("   ⚠️  .gitignore não encontrado!")

def main():
    """Função principal"""
    print("🔒 SCRIPT DE LIMPEZA DE DADOS SENSÍVEIS")
    print("=" * 50)
    
    # Verificar se estamos no diretório correto
    if not os.path.exists('cnab_bradesco.py'):
        print("❌ Execute este script no diretório raiz do projeto!")
        return
    
    try:
        limpar_arquivos_sensíveis()
        verificar_dados_sensíveis_codigo()
        criar_gitignore_adicional()
        
        print("\n" + "=" * 50)
        print("✅ Limpeza de segurança concluída!")
        print("📋 Próximos passos:")
        print("   1. Revise as alterações")
        print("   2. Execute 'git add .' ")
        print("   3. Execute 'git commit -m \"Preparação para GitHub\"'")
        print("   4. Execute 'git push'")
        
    except Exception as e:
        print(f"\n❌ Erro durante a limpeza: {e}")

if __name__ == "__main__":
    main() 