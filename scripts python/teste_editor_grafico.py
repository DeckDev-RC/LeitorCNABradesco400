#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de demonstração do Editor Gráfico de CNAB
Permite edição visual dos campos NOSSO_NUMERO e CODIGO_EMPRESA
"""

import sys
import os

# Adicionar o diretório pai ao path para importar o módulo
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5.QtWidgets import QApplication
from cnab_bradesco_gui import CNABBradescoGUI

def demonstrar_editor_grafico():
    """Demonstra o uso do editor gráfico"""
    print("=" * 80)
    print("🎨 DEMONSTRAÇÃO DO EDITOR GRÁFICO DE CNAB")
    print("=" * 80)
    print("Este script abre a interface gráfica principal do sistema")
    print("onde você poderá testar o novo Editor Gráfico.")
    print("=" * 80)
    
    print("\n🔧 FUNCIONALIDADES DO EDITOR GRÁFICO:")
    print("1. ✏️  Interface visual moderna e intuitiva")
    print("2. 📋 Tabela com todos os registros CNAB")
    print("3. 🔍 Filtros de busca por Nosso Número e Código da Empresa")
    print("4. ✨ Edição direta na tabela (duplo clique)")
    print("5. 🔧 Edição em lote para aplicar valores a múltiplos registros")
    print("6. ✅ Validação automática dos dados inseridos")
    print("7. 🎨 Destaque visual dos registros alterados")
    print("8. 💾 Salvamento em novo arquivo CNAB")
    
    print("\n🎯 CAMPOS EDITÁVEIS:")
    print("• NOSSO_NUMERO - Número do título no banco (máx. 12 dígitos)")
    print("• CODIGO_EMPRESA - Código da empresa no banco (máx. 17 caracteres)")
    
    print("\n📝 COMO USAR:")
    print("1. Carregue um arquivo CNAB na interface principal")
    print("2. Clique no botão '✏️ Editor Gráfico' (verde)")
    print("3. Use a tabela para visualizar e editar os campos")
    print("4. Use os filtros para encontrar registros específicos")
    print("5. Use a edição em lote para alterações em massa")
    print("6. Salve as alterações em um novo arquivo")
    
    print("\n🔍 VALIDAÇÕES IMPLEMENTADAS:")
    print("• Nosso Número: Apenas números, máximo 12 dígitos")
    print("• Código Empresa: Alfanumérico, máximo 17 caracteres")
    print("• Campos obrigatórios não podem ficar vazios")
    print("• Confirmação antes de aplicar alterações em lote")
    
    print("\n💡 DICAS DE USO:")
    print("• Duplo clique nas células para editar")
    print("• Use os filtros para trabalhar com subconjuntos")
    print("• Registros alterados ficam destacados em azul")
    print("• O contador mostra quantos registros foram alterados")
    print("• O arquivo original nunca é modificado")
    
    print("\n" + "=" * 80)
    print("🚀 INICIANDO INTERFACE GRÁFICA...")
    print("=" * 80)
    
    # Verificar se existem arquivos CNAB para teste
    arquivos_cnab = [f for f in os.listdir('..') if f.upper().endswith('.TXT')]
    
    if arquivos_cnab:
        print(f"\n📁 {len(arquivos_cnab)} arquivo(s) CNAB encontrado(s) no diretório:")
        for arquivo in arquivos_cnab[:5]:  # Mostrar apenas os primeiros 5
            print(f"  • {arquivo}")
        if len(arquivos_cnab) > 5:
            print(f"  • ... e mais {len(arquivos_cnab) - 5} arquivo(s)")
    else:
        print("\n⚠️  Nenhum arquivo CNAB (.TXT) encontrado no diretório pai.")
        print("💡 Coloque um arquivo CNAB na pasta do projeto para testar.")
    
    print("\n✨ A interface gráfica será aberta em uma nova janela...")
    print("🎯 Procure pelo botão '✏️ Editor Gráfico' (verde) após carregar um arquivo CNAB!")

def main():
    """Função principal"""
    try:
        # Mostrar informações sobre o editor gráfico
        demonstrar_editor_grafico()
        
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