#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de demonstração da nova interface horizontal do Editor Gráfico

Este script demonstra as melhorias na interface do editor gráfico:
- Layout horizontal otimizado
- Melhor aproveitamento do espaço da tela
- Evita problemas com a barra de tarefas do Windows
"""

import sys
import os

# Adicionar o diretório pai ao path para importar o módulo
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5.QtWidgets import QApplication
from cnab_bradesco_gui import CNABBradescoGUI

def demonstrar_interface_horizontal():
    """Demonstra a nova interface horizontal do editor gráfico"""
    print("=" * 80)
    print("🎨 NOVA INTERFACE HORIZONTAL - EDITOR GRÁFICO")
    print("=" * 80)
    print("Interface redesenhada para melhor aproveitamento do espaço da tela")
    print("e evitar problemas com a barra de tarefas do Windows.")
    print("=" * 80)
    
    print("\n🔄 MELHORIAS IMPLEMENTADAS:")
    print("1. 📐 Layout Horizontal:")
    print("   ├─ Painel esquerdo (70%): Filtros + Tabela de registros")
    print("   ├─ Painel direito (30%): Controles de edição")
    print("   └─ Divisor redimensionável entre painéis")
    
    print("\n2. 📏 Dimensões Otimizadas:")
    print("   ├─ Largura mínima: 1400px (mais larga)")
    print("   ├─ Altura mínima: 600px (menos alta)")
    print("   └─ Melhor proporção para telas widescreen")
    
    print("\n3. 🎯 Organização dos Controles:")
    print("   ├─ Filtros: Mantidos no painel esquerdo com a tabela")
    print("   ├─ Edição em lote: Painel direito, layout vertical compacto")
    print("   ├─ Importação de planilha: Painel direito, interface compacta")
    print("   └─ Scroll automático nos controles se necessário")
    
    print("\n4. 🖥️ Compatibilidade com Telas:")
    print("   ├─ Telas widescreen: Aproveitamento máximo do espaço")
    print("   ├─ Monitores 1920x1080: Interface completa visível")
    print("   ├─ Barra de tarefas: Não interfere mais na visualização")
    print("   └─ Redimensionamento: Painéis ajustáveis pelo usuário")
    
    print("\n🎨 DETALHES DA INTERFACE:")
    print("📍 Painel Esquerdo (Tabela):")
    print("   • Filtros de busca no topo")
    print("   • Tabela de registros com scroll")
    print("   • Colunas redimensionáveis")
    print("   • Edição direta por duplo clique")
    
    print("\n📍 Painel Direito (Controles):")
    print("   • Scroll area para evitar cortes")
    print("   • Edição em lote compacta")
    print("   • Importação de planilha otimizada")
    print("   • Botões menores e organizados verticalmente")
    
    print("\n📍 Rodapé (Botões de Ação):")
    print("   • Mantido na parte inferior")
    print("   • Largura total da janela")
    print("   • Contador de alterações à esquerda")
    print("   • Botões de ação à direita")
    
    print("\n🔧 FUNCIONALIDADES PRESERVADAS:")
    print("✅ Todas as funcionalidades existentes mantidas")
    print("✅ Edição direta na tabela")
    print("✅ Filtros de busca")
    print("✅ Edição em lote")
    print("✅ Importação de planilha")
    print("✅ Validações automáticas")
    print("✅ Destaque visual das alterações")
    print("✅ Botão 'Gerar CNAB sem Juros'")
    
    print("\n🎯 VANTAGENS DO NOVO LAYOUT:")
    print("• 🖥️  Melhor uso do espaço horizontal")
    print("• 📊 Tabela mais visível e acessível")
    print("• 🚫 Evita cortes pela barra de tarefas")
    print("• 🎨 Interface mais moderna e profissional")
    print("• ⚡ Navegação mais eficiente")
    print("• 📱 Adaptável a diferentes resoluções")
    
    print("\n💡 DICAS DE USO:")
    print("• Arraste a divisória central para ajustar proporções")
    print("• Use scroll no painel direito se houver muitos controles")
    print("• Redimensione colunas da tabela conforme necessário")
    print("• Filtros ficam sempre visíveis no painel esquerdo")
    
    print("\n🔍 RESOLUÇÃO RECOMENDADA:")
    print("• Mínima: 1400x600 pixels")
    print("• Ideal: 1920x1080 pixels ou superior")
    print("• Suporte: Qualquer resolução widescreen")
    
    print("\n" + "=" * 80)
    print("🚀 INICIANDO DEMONSTRAÇÃO DA NOVA INTERFACE...")
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
    print("🎯 Passos para testar a nova interface:")
    print("   1. Carregue um arquivo CNAB")
    print("   2. Clique em '✏️ Editor Gráfico'")
    print("   3. Observe o novo layout horizontal")
    print("   4. Teste o redimensionamento dos painéis")
    print("   5. Experimente todas as funcionalidades!")
    
    print(f"\n📐 Resolução da tela detectada: {get_screen_resolution()}")
    print("💡 A interface se adaptará automaticamente!")

def get_screen_resolution():
    """Obtém a resolução da tela"""
    try:
        from PyQt5.QtWidgets import QDesktopWidget
        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        
        desktop = QDesktopWidget()
        screen = desktop.screenGeometry()
        return f"{screen.width()}x{screen.height()}"
    except:
        return "Não detectada"

def main():
    """Função principal"""
    try:
        # Mostrar informações sobre a nova interface
        demonstrar_interface_horizontal()
        
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