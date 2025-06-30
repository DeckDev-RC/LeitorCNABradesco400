#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script automatizado de compilação para o Sistema CNAB Bradesco
Autor: Sistema CNAB Bradesco
Versão: 1.2.0
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
import time
import argparse

class CNABBuilder:
    def __init__(self):
        self.project_root = Path.cwd()
        self.build_dir = self.project_root / "build"
        self.dist_dir = self.project_root / "dist"
        self.version = "1.2.0"
        
    def clean_previous_builds(self):
        """Remove builds anteriores"""
        print("🧹 Limpando builds anteriores...")
        
        for dir_path in [self.build_dir, self.dist_dir]:
            if dir_path.exists():
                shutil.rmtree(dir_path)
                print(f"   ✅ Removido: {dir_path}")
        
        # Remove arquivos .spec antigos (exceto os principais)
        for spec_file in self.project_root.glob("*.spec"):
            if spec_file.name not in ["cnab_bradesco_gui.spec", "cnab_console.spec"]:
                spec_file.unlink()
                print(f"   ✅ Removido: {spec_file}")
        
        # Remove arquivos temporários
        temp_files = ["file_version_info.txt", "*.pyc"]
        for pattern in temp_files:
            for temp_file in self.project_root.glob(pattern):
                if temp_file.exists():
                    temp_file.unlink()
                    print(f"   ✅ Removido: {temp_file}")
    
    def verify_dependencies(self):
        """Verifica dependências necessárias"""
        print("🔍 Verificando dependências...")
        
        required_modules = [
            'PyQt5', 'pandas', 'openpyxl', 'tabulate', 'pyinstaller'
        ]
        
        missing = []
        for module in required_modules:
            try:
                __import__(module)
                print(f"   ✅ {module}")
            except ImportError:
                missing.append(module)
                print(f"   ❌ {module}")
        
        if missing:
            print(f"\n❌ Dependências faltando: {', '.join(missing)}")
            print("Execute: pip install -r requirements.txt")
            return False
        
        return True
    
    def create_version_info(self):
        """Cria arquivo de informações de versão para Windows"""
        print("📝 Criando informações de versão...")
        
        version_parts = self.version.split('.')
        version_info = f'''VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=({version_parts[0]}, {version_parts[1]}, {version_parts[2]}, 0),
    prodvers=({version_parts[0]}, {version_parts[1]}, {version_parts[2]}, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
        StringTable(
          u'040904B0',
          [
            StringStruct(u'CompanyName', u'Sistema CNAB Bradesco'),
            StringStruct(u'FileDescription', u'Processador de Arquivos CNAB 400 - Bradesco'),
            StringStruct(u'FileVersion', u'{self.version}'),
            StringStruct(u'InternalName', u'cnab_bradesco'),
            StringStruct(u'LegalCopyright', u'Copyright © 2024'),
            StringStruct(u'OriginalFilename', u'Sistema CNAB Bradesco.exe'),
            StringStruct(u'ProductName', u'Sistema CNAB Bradesco'),
            StringStruct(u'ProductVersion', u'{self.version}')
          ]
        )
      ]
    ),
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)'''
        
        with open('file_version_info.txt', 'w', encoding='utf-8') as f:
            f.write(version_info)
        
        print("   ✅ file_version_info.txt criado")
    
    def build_gui_version(self):
        """Compila versão GUI"""
        print("🎨 Compilando versão GUI...")
        
        cmd = [
            'pyinstaller',
            '--clean',
            '--onefile',
            '--windowed',
            '--name=Sistema CNAB Bradesco',
            '--icon=icon.ico',
            '--version-file=file_version_info.txt',
            '--add-data=exemplos;exemplos',
            '--add-data=docs;docs',
            '--hidden-import=PyQt5.QtCore',
            '--hidden-import=PyQt5.QtGui',
            '--hidden-import=PyQt5.QtWidgets',
            '--hidden-import=PyQt5.QtPrintSupport',
            '--hidden-import=pandas._libs.tslibs.timedeltas',
            '--hidden-import=pandas._libs.tslibs.np_datetime',
            '--hidden-import=pandas._libs.tslibs.nattype',
            '--hidden-import=pandas._libs.reduction',
            '--hidden-import=pandas.io.formats.style',
            '--hidden-import=openpyxl.cell',
            '--hidden-import=openpyxl.styles',
            '--hidden-import=openpyxl.workbook',
            '--hidden-import=openpyxl.worksheet',
            '--hidden-import=tabulate',
            '--hidden-import=cnab_bradesco',
            '--hidden-import=cnab_processor',
            '--hidden-import=processar_lote',
            '--exclude-module=tkinter',
            '--exclude-module=matplotlib',
            '--exclude-module=test',
            '--exclude-module=unittest',
            '--exclude-module=distutils',
            'main.py'
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            print("   ✅ Build GUI concluído com sucesso!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Erro no build GUI:")
            print(f"   Stdout: {e.stdout}")
            print(f"   Stderr: {e.stderr}")
            return False
    
    def build_console_version(self):
        """Compila versão console"""
        print("💻 Compilando versão console...")
        
        cmd = [
            'pyinstaller',
            '--clean',
            '--onefile',
            '--console',
            '--name=CNAB Bradesco Console',
            '--icon=icon.ico',
            '--version-file=file_version_info.txt',
            '--add-data=exemplos;exemplos',
            '--hidden-import=PyQt5.QtCore',
            '--hidden-import=PyQt5.QtGui', 
            '--hidden-import=PyQt5.QtWidgets',
            '--hidden-import=pandas._libs.tslibs.timedeltas',
            '--hidden-import=openpyxl.cell',
            '--hidden-import=cnab_bradesco',
            '--hidden-import=cnab_processor',
            '--hidden-import=processar_lote',
            '--exclude-module=matplotlib',
            '--exclude-module=test',
            'iniciar.py'
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            print("   ✅ Build console concluído com sucesso!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Erro no build console:")
            print(f"   Stdout: {e.stdout}")
            print(f"   Stderr: {e.stderr}")
            return False
    
    def create_installer_package(self):
        """Cria pacote de instalação"""
        print("📦 Criando pacote de distribuição...")
        
        package_dir = self.project_root / f"CNAB_Bradesco_v{self.version}"
        if package_dir.exists():
            shutil.rmtree(package_dir)
        package_dir.mkdir(exist_ok=True)
        
        # Copiar executáveis
        gui_exe = self.dist_dir / "Sistema CNAB Bradesco.exe"
        console_exe = self.dist_dir / "CNAB Bradesco Console.exe"
        
        if gui_exe.exists():
            shutil.copy2(gui_exe, package_dir)
            print("   ✅ GUI executável copiado")
        
        if console_exe.exists():
            shutil.copy2(console_exe, package_dir)
            print("   ✅ Console executável copiado")
        
        # Copiar documentação
        docs_to_copy = ["README.md", "LICENSE", "CHANGELOG.md"]
        for doc in docs_to_copy:
            if Path(doc).exists():
                shutil.copy2(doc, package_dir)
                print(f"   ✅ {doc} copiado")
        
        # Copiar exemplos
        if (self.project_root / "exemplos").exists():
            shutil.copytree("exemplos", package_dir / "exemplos", dirs_exist_ok=True)
            print("   ✅ Exemplos copiados")
        
        # Criar README de instalação
        install_readme = f'''# Sistema CNAB Bradesco v{self.version}

## 📦 Conteúdo do Pacote

- `Sistema CNAB Bradesco.exe` - Interface gráfica principal
- `CNAB Bradesco Console.exe` - Interface de linha de comando  
- `exemplos/` - Arquivos de exemplo para teste
- `README.md` - Documentação completa
- `LICENSE` - Licença MIT
- `CHANGELOG.md` - Histórico de versões

## 🚀 Como Usar

### Interface Gráfica (Recomendado)
1. Execute `Sistema CNAB Bradesco.exe`
2. Use a interface visual para processar arquivos CNAB

### Interface Console
1. Execute `CNAB Bradesco Console.exe`
2. Escolha as opções do menu interativo

## ⚠️ Requisitos
- Windows 10/11
- 4GB RAM mínimo
- 500MB espaço em disco

## 📞 Suporte
- GitHub: https://github.com/seu-usuario/cnab-bradesco
- Issues: https://github.com/seu-usuario/cnab-bradesco/issues

## 🔧 Solução de Problemas

### Erro de DLL ou biblioteca
- Instale o Visual C++ Redistributable 2019+
- Baixe em: https://aka.ms/vs/16/release/vc_redist.x64.exe

### Antivírus bloqueando
- Adicione os executáveis à lista de exceções
- O software é seguro e open source

### Performance lenta
- Feche outros programas pesados
- Certifique-se de ter pelo menos 4GB RAM disponível
'''
        
        with open(package_dir / "LEIA-ME.txt", 'w', encoding='utf-8') as f:
            f.write(install_readme)
        
        print(f"   ✅ Pacote criado em: {package_dir}")
        return package_dir
    
    def run_tests(self):
        """Executa testes básicos nos executáveis"""
        print("🧪 Executando testes básicos...")
        
        gui_exe = self.dist_dir / "Sistema CNAB Bradesco.exe"
        console_exe = self.dist_dir / "CNAB Bradesco Console.exe"
        
        # Teste GUI
        if gui_exe.exists():
            print("   🔍 Testando executável GUI...")
            file_size = gui_exe.stat().st_size / (1024 * 1024)  # MB
            print(f"   📏 Tamanho: {file_size:.1f}MB")
            
            if file_size > 200:
                print("   ⚠️  Executável muito grande (>200MB)")
            else:
                print("   ✅ Tamanho adequado")
        
        # Teste Console
        if console_exe.exists():
            print("   🔍 Testando executável Console...")
            file_size = console_exe.stat().st_size / (1024 * 1024)  # MB
            print(f"   📏 Tamanho: {file_size:.1f}MB")
        
        return True
    
    def build_all(self):
        """Executa build completo"""
        start_time = time.time()
        
        print("🔨 INICIANDO BUILD COMPLETO DO SISTEMA CNAB BRADESCO")
        print("=" * 60)
        
        steps = [
            ("Limpeza", self.clean_previous_builds),
            ("Verificação", self.verify_dependencies),
            ("Versão", self.create_version_info),
            ("Build GUI", self.build_gui_version),
            ("Build Console", self.build_console_version),
            ("Pacote", self.create_installer_package),
            ("Testes", self.run_tests),
        ]
        
        failed_steps = []
        
        for step_name, step_func in steps:
            print(f"\n📋 Etapa: {step_name}")
            try:
                result = step_func()
                if result is False:
                    print(f"❌ Falha na etapa: {step_name}")
                    failed_steps.append(step_name)
            except Exception as e:
                print(f"❌ Erro na etapa {step_name}: {str(e)}")
                failed_steps.append(step_name)
        
        elapsed = time.time() - start_time
        print("\n" + "=" * 60)
        
        if failed_steps:
            print(f"⚠️  BUILD CONCLUÍDO COM PROBLEMAS!")
            print(f"❌ Etapas com falha: {', '.join(failed_steps)}")
        else:
            print(f"✅ BUILD CONCLUÍDO COM SUCESSO!")
        
        print(f"⏱️  Tempo total: {elapsed:.1f} segundos")
        print(f"📦 Arquivos gerados em: {self.dist_dir}")
        print("=" * 60)
        
        return len(failed_steps) == 0

def main():
    parser = argparse.ArgumentParser(description='Build Sistema CNAB Bradesco')
    parser.add_argument('--gui-only', action='store_true', help='Compilar apenas versão GUI')
    parser.add_argument('--console-only', action='store_true', help='Compilar apenas versão console')
    parser.add_argument('--no-clean', action='store_true', help='Não limpar builds anteriores')
    
    args = parser.parse_args()
    
    builder = CNABBuilder()
    
    if args.gui_only:
        print("🎨 Compilando apenas versão GUI...")
        if not args.no_clean:
            builder.clean_previous_builds()
        builder.verify_dependencies()
        builder.create_version_info()
        success = builder.build_gui_version()
    elif args.console_only:
        print("💻 Compilando apenas versão console...")
        if not args.no_clean:
            builder.clean_previous_builds()
        builder.verify_dependencies()
        builder.create_version_info()
        success = builder.build_console_version()
    else:
        success = builder.build_all()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 