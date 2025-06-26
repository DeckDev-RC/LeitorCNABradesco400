#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de demonstração da nova funcionalidade:
Editor Gráfico com Geração de CNAB sem Juros

Este script demonstra como usar o novo botão "🔄 Gerar CNAB sem Juros"
no editor gráfico, que combina as modificações do editor com o zeramento de juros.
"""

import sys
import os

# Adicionar o diretório pai ao path para importar o módulo
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5.QtWidgets import QApplication
from cnab_bradesco_gui import CNABBradescoGUI

def demonstrar_nova_funcionalidade():
    """Demonstra a nova funcionalidade do editor gráfico"""
    print("=" * 80)
    print("🎨 NOVA FUNCIONALIDADE: EDITOR GRÁFICO COM CNAB SEM JUROS")
    print("=" * 80)
    print("Esta nova funcionalidade combina o melhor dos dois mundos:")
    print("• Edição gráfica de campos NOSSO_NUMERO e CODIGO_EMPRESA")
    print("• Geração de CNAB sem juros/multa")
    print("=" * 80)
    
    print("\n🆕 NOVA FUNCIONALIDADE:")
    print("🔄 Botão 'Gerar CNAB sem Juros' no Editor Gráfico")
    print("   ├─ Aplica TODAS as modificações feitas no editor")
    print("   ├─ Zera automaticamente todos os juros/multa")
    print("   ├─ Gera um novo arquivo CNAB completo")
    print("   └─ Mantém os dados originais intactos")
    
    print("\n🔧 COMO FUNCIONA:")
    print("1. 📁 Carregue um arquivo CNAB na interface principal")
    print("2. ✏️  Abra o Editor Gráfico")
    print("3. 🖊️  Faça as modificações desejadas nos campos:")
    print("   • NOSSO_NUMERO (edição individual ou em lote)")
    print("   • CODIGO_EMPRESA (edição individual ou em lote)")
    print("4. 🔄 Clique no novo botão 'Gerar CNAB sem Juros'")
    print("5. 💾 Escolha onde salvar o arquivo resultado")
    
    print("\n🎯 VANTAGENS DA NOVA FUNCIONALIDADE:")
    print("• ⚡ Processo unificado: edição + zeramento de juros em uma ação")
    print("• 🛡️  Segurança: dados originais nunca são alterados")
    print("• 📊 Relatório completo do que foi feito")
    print("• 🎨 Interface visual intuitiva")
    print("• 🔍 Filtros para localizar registros específicos")
    print("• 🔧 Edição em lote para alterações em massa")
    
    print("\n📋 CENÁRIOS DE USO:")
    print("1. 🔄 Alterar nossos números E zerar juros")
    print("2. 🏢 Alterar códigos de empresa E zerar juros")
    print("3. 💰 Apenas zerar juros (sem modificações)")
    print("4. 📊 Aplicar planilha de mapeamentos E zerar juros")
    
    print("\n🆚 DIFERENÇAS ENTRE OS BOTÕES:")
    print("💾 'Salvar Alterações':")
    print("   ├─ Aplica apenas as modificações do editor")
    print("   ├─ Mantém os juros originais")
    print("   └─ Gera arquivo '_editado.TXT'")
    print("")
    print("🔄 'Gerar CNAB sem Juros' (NOVO):")
    print("   ├─ Aplica as modificações do editor")
    print("   ├─ Zera TODOS os juros/multa")
    print("   └─ Gera arquivo '_editado_sem_juros.TXT' ou '_sem_juros.TXT'")
    
    print("\n🎨 INTERFACE VISUAL:")
    print("• Botão verde com ícone 🔄")
    print("• Posicionado entre 'Cancelar' e 'Salvar Alterações'")
    print("• Tooltip explicativo")
    print("• Confirmação antes da ação")
    print("• Relatório detalhado do resultado")
    
    print("\n💡 DICAS DE USO:")
    print("• O botão funciona mesmo sem modificações (apenas zera juros)")
    print("• Registros alterados ficam destacados na tabela")
    print("• Use os filtros para trabalhar com subconjuntos")
    print("• O arquivo original nunca é modificado")
    print("• Nomes de arquivo são sugeridos automaticamente")
    
    print("\n🔍 VALIDAÇÕES IMPLEMENTADAS:")
    print("• Nosso Número: máximo 12 caracteres alfanuméricos")
    print("• Código Empresa: máximo 17 caracteres")
    print("• Confirmação antes de gerar o arquivo")
    print("• Verificação de dados válidos")
    print("• Tratamento de erros robusto")
    
    print("\n📁 ARQUIVOS GERADOS:")
    print("• Com modificações: 'arquivo_editado_sem_juros.TXT'")
    print("• Sem modificações: 'arquivo_sem_juros.TXT'")
    print("• Estrutura CNAB 400 padrão mantida")
    print("• Sequenciais atualizados corretamente")
    
    print("\n" + "=" * 80)
    print("🚀 INICIANDO DEMONSTRAÇÃO...")
    print("=" * 80)
    
    # Verificar se existem arquivos CNAB para teste
    arquivos_cnab = [f for f in os.listdir('..') if f.upper().endswith('.TXT')]
    
    if arquivos_cnab:
        print(f"\n📁 {len(arquivos_cnab)} arquivo(s) CNAB encontrado(s):")
        for arquivo in arquivos_cnab[:3]:
            print(f"  • {arquivo}")
        if len(arquivos_cnab) > 3:
            print(f"  • ... e mais {len(arquivos_cnab) - 3} arquivo(s)")
    else:
        print("\n⚠️  Nenhum arquivo CNAB (.TXT) encontrado.")
        print("💡 Coloque um arquivo CNAB na pasta do projeto para testar.")
    
    print("\n✨ A interface gráfica será aberta...")
    print("🎯 Siga estes passos para testar a nova funcionalidade:")
    print("   1. Carregue um arquivo CNAB")
    print("   2. Clique em '✏️ Editor Gráfico'")
    print("   3. Faça algumas modificações (opcional)")
    print("   4. Clique no novo botão '🔄 Gerar CNAB sem Juros'")
    print("   5. Observe o resultado!")

def main():
    """Função principal"""
    try:
        # Mostrar informações sobre a nova funcionalidade
        demonstrar_nova_funcionalidade()
        
        # Criar aplicação Qt
        app = QApplication(sys.argv)
        
        # Criar e mostrar a janela principal
        window = CNABBradescoGUI()
        window.show()
        
        # Executar a aplicação
        sys.exit(app.exec_())
        
    except KeyboardInterrupt:
        print("\n\n👋 Demonstração interrompida pelo usuário.")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {str(e)}")
        import traceback
        print(f"🔍 Detalhes: {traceback.format_exc()}")

if __name__ == "__main__":
    main() 