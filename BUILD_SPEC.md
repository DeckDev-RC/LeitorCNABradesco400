# 🔨 Especificação de Build - Sistema CNAB Bradesco v1.2.0

## 📋 Análise Profunda do Projeto

### 🏗️ Arquitetura da Aplicação
```
cnab-bradesco/
├── 🎯 Pontos de Entrada
│   ├── main.py                    # Entrada GUI direta
│   ├── iniciar.py                 # Menu interativo principal
│   └── cnab_bradesco_gui.py       # Interface gráfica standalone
├── 🧠 Core Logic
│   ├── cnab_bradesco.py           # Processador principal (1558 linhas)
│   ├── cnab_processor.py          # Processador base
│   └── processar_lote.py          # Processamento em lote
├── 🎨 Interface
│   └── cnab_bradesco_gui.py       # GUI PyQt5 (2745 linhas)
├── 📊 Assets
│   ├── icon.ico                   # Ícone da aplicação
│   └── exemplos/                  # Templates e exemplos
└── 📖 Documentação
    └── docs/                      # Documentação técnica
```

### 🔍 Dependências Críticas Identificadas

#### Core Dependencies
- **PyQt5** (5.15.9+) - Interface gráfica completa
- **pandas** (2.0.3+) - Manipulação de dados CNAB
- **openpyxl** (3.1.2+) - Exportação Excel
- **tabulate** (0.9.0+) - Formatação de tabelas

#### Hidden Imports Necessários
```python
# PyQt5 Modules
'PyQt5.QtCore',
'PyQt5.QtGui', 
'PyQt5.QtWidgets',
'PyQt5.QtPrintSupport',

# Pandas Dependencies
'pandas._libs.tslibs.timedeltas',
'pandas._libs.tslibs.np_datetime',
'pandas._libs.tslibs.nattype',
'pandas._libs.reduction',
'pandas.io.formats.style',

# OpenPyXL Dependencies
'openpyxl.cell',
'openpyxl.styles',
'openpyxl.workbook',
'openpyxl.worksheet',

# System Dependencies
'encodings.utf_8',
'encodings.cp1252',
'locale',
'datetime',
'decimal'
```

### 🎯 Estratégias de Build

## 📦 Configurações de Build

### 🔧 Build Principal - Interface Gráfica (Recomendado)

```python
# cnab_bradesco_gui.spec
# -*- mode: python ; coding: utf-8 -*-

import sys
from pathlib import Path

# Configurações do projeto
PROJECT_NAME = "Sistema CNAB Bradesco"
VERSION = "1.2.0"
MAIN_SCRIPT = "main.py"
ICON_PATH = "icon.ico"

# Dados adicionais para incluir
added_files = [
    ('exemplos/*.txt', 'exemplos'),
    ('docs/*.md', 'docs'),
    ('icon.ico', '.'),
]

# Imports ocultos necessários
hidden_imports = [
    # PyQt5 Core
    'PyQt5.QtCore',
    'PyQt5.QtGui',
    'PyQt5.QtWidgets',
    'PyQt5.QtPrintSupport',
    
    # Pandas e dependências
    'pandas',
    'pandas._libs.tslibs.timedeltas',
    'pandas._libs.tslibs.np_datetime', 
    'pandas._libs.tslibs.nattype',
    'pandas._libs.reduction',
    'pandas.io.formats.style',
    'pandas.io.common',
    'pandas.plotting',
    
    # OpenPyXL
    'openpyxl',
    'openpyxl.cell',
    'openpyxl.styles',
    'openpyxl.workbook',
    'openpyxl.worksheet',
    'openpyxl.drawing',
    
    # Tabulate
    'tabulate',
    
    # Sistema
    'encodings.utf_8',
    'encodings.cp1252',
    'locale',
    'datetime',
    'decimal',
    'sqlite3',
    
    # Módulos do projeto
    'cnab_bradesco',
    'cnab_processor',
    'processar_lote',
]

# Exclusões para reduzir tamanho
excludes = [
    'tkinter',
    'matplotlib',
    'numpy.random._examples',
    'test',
    'unittest',
    'distutils',
    'setuptools',
]

block_cipher = None

a = Analysis(
    [MAIN_SCRIPT],
    pathex=['.'],
    binaries=[],
    datas=added_files,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Remover duplicatas
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name=PROJECT_NAME,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=ICON_PATH,
    version='file_version_info.txt'
)
```

### 🖥️ Build Alternativo - Console (Menu Interativo)

```python
# cnab_console.spec
# Para usuários que preferem interface de linha de comando

a = Analysis(
    ['iniciar.py'],
    pathex=['.'],
    binaries=[],
    datas=added_files,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='CNAB Bradesco Console',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Console habilitado
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=ICON_PATH,
)
```

## 🛠️ Processo de Build Automatizado

### 📋 Pré-requisitos
```bash
# 1. Python 3.8+ instalado
python --version

# 2. Ambiente virtual (recomendado)
python -m venv build_env
build_env\Scripts\activate  # Windows
# source build_env/bin/activate  # Linux/Mac

# 3. Dependências de build
pip install --upgrade pip
pip install pyinstaller>=6.0.0
pip install -r requirements.txt
```

### 🚀 Script de Build Automatizado

```python
# build.py - Script automatizado de compilação

import os
import sys
import shutil
import subprocess
from pathlib import Path
import time

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
        
        # Remove arquivos .spec antigos
        for spec_file in self.project_root.glob("*.spec"):
            if spec_file.name not in ["cnab_bradesco_gui.spec", "cnab_console.spec"]:
                spec_file.unlink()
                print(f"   ✅ Removido: {spec_file}")
    
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
        """Cria arquivo de informações de versão"""
        print("📝 Criando informações de versão...")
        
        version_info = f'''
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=({self.version.replace('.', ', ')}, 0),
    prodvers=({self.version.replace('.', ', ')}, 0),
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
)
'''
        
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
            '--hidden-import=pandas._libs.tslibs.timedeltas',
            '--hidden-import=openpyxl.cell',
            '--exclude-module=tkinter',
            '--exclude-module=matplotlib',
            'main.py'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("   ✅ Build GUI concluído com sucesso!")
            return True
        else:
            print(f"   ❌ Erro no build GUI: {result.stderr}")
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
            '--exclude-module=matplotlib',
            'iniciar.py'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("   ✅ Build console concluído com sucesso!")
            return True
        else:
            print(f"   ❌ Erro no build console: {result.stderr}")
            return False
    
    def create_installer_package(self):
        """Cria pacote de instalação"""
        print("📦 Criando pacote de distribuição...")
        
        package_dir = self.project_root / f"CNAB_Bradesco_v{self.version}"
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
        shutil.copy2("README.md", package_dir)
        shutil.copy2("LICENSE", package_dir)
        shutil.copy2("CHANGELOG.md", package_dir)
        
        # Copiar exemplos
        if (self.project_root / "exemplos").exists():
            shutil.copytree("exemplos", package_dir / "exemplos", dirs_exist_ok=True)
            print("   ✅ Exemplos copiados")
        
        # Criar README de instalação
        install_readme = f'''
# Sistema CNAB Bradesco v{self.version}

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
'''
        
        with open(package_dir / "LEIA-ME.txt", 'w', encoding='utf-8') as f:
            f.write(install_readme)
        
        print(f"   ✅ Pacote criado em: {package_dir}")
        return package_dir
    
    def run_tests(self):
        """Executa testes básicos nos executáveis"""
        print("🧪 Executando testes básicos...")
        
        gui_exe = self.dist_dir / "Sistema CNAB Bradesco.exe"
        
        if gui_exe.exists():
            print("   🔍 Testando executável GUI...")
            # Teste básico: verificar se o executável inicia
            result = subprocess.run([str(gui_exe), '--version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print("   ✅ Executável GUI funcional")
            else:
                print("   ⚠️  Executável GUI pode ter problemas")
        
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
        
        for step_name, step_func in steps:
            print(f"\n📋 Etapa: {step_name}")
            try:
                result = step_func()
                if result is False:
                    print(f"❌ Falha na etapa: {step_name}")
                    return False
            except Exception as e:
                print(f"❌ Erro na etapa {step_name}: {str(e)}")
                return False
        
        elapsed = time.time() - start_time
        print("\n" + "=" * 60)
        print(f"✅ BUILD CONCLUÍDO COM SUCESSO!")
        print(f"⏱️  Tempo total: {elapsed:.1f} segundos")
        print(f"📦 Arquivos gerados em: {self.dist_dir}")
        print("=" * 60)
        
        return True

if __name__ == "__main__":
    builder = CNABBuilder()
    success = builder.build_all()
    sys.exit(0 if success else 1)
```

## 🎯 Comandos de Build Rápidos

### 🚀 Build Completo Automatizado
```bash
# Executar build completo
python build.py
```

### 🔧 Build Manual - GUI
```bash
pyinstaller --clean --onefile --windowed \
    --name="Sistema CNAB Bradesco" \
    --icon=icon.ico \
    --add-data="exemplos;exemplos" \
    --hidden-import=PyQt5.QtCore \
    --hidden-import=PyQt5.QtGui \
    --hidden-import=PyQt5.QtWidgets \
    --exclude-module=tkinter \
    main.py
```

### 💻 Build Manual - Console
```bash
pyinstaller --clean --onefile --console \
    --name="CNAB Bradesco Console" \
    --icon=icon.ico \
    --add-data="exemplos;exemplos" \
    --hidden-import=PyQt5.QtCore \
    iniciar.py
```

## 📊 Otimizações de Performance

### 🔧 Configurações Avançadas
- **UPX Compression**: Reduz tamanho do executável em ~40%
- **Exclude Modules**: Remove módulos desnecessários
- **Hidden Imports**: Garante inclusão de dependências críticas
- **OneFile Mode**: Gera executável único para distribuição

### 📈 Métricas Esperadas
- **Tamanho Final**: ~80-120MB (com UPX)
- **Tempo de Inicialização**: 2-4 segundos
- **Uso de Memória**: 150-300MB em execução
- **Compatibilidade**: Windows 10/11 (64-bit)

## 🔍 Troubleshooting

### ❌ Problemas Comuns

#### "Module not found" durante execução
```bash
# Solução: Adicionar ao hidden imports
--hidden-import=nome_do_modulo
```

#### Executável muito grande
```bash
# Solução: Usar exclusões
--exclude-module=matplotlib
--exclude-module=tkinter
```

#### Erro de DLL no Windows
```bash
# Solução: Incluir Visual C++ Redistributable
# Ou usar --onefile para bundle completo
```

### 🛠️ Debug Mode
```bash
# Para debug de problemas
pyinstaller --debug=all --console main.py
```

## 📋 Checklist Final

### ✅ Antes do Build
- [ ] Dependências instaladas
- [ ] Código testado e funcional
- [ ] Ícone (icon.ico) presente
- [ ] Arquivos de exemplo atualizados
- [ ] Documentação atualizada

### ✅ Após o Build
- [ ] Executável inicia corretamente
- [ ] Interface gráfica carrega
- [ ] Processamento CNAB funcional
- [ ] Exportação para Excel funciona
- [ ] Editor gráfico operacional
- [ ] Tamanho do arquivo aceitável

### ✅ Para Distribuição
- [ ] Testes em máquina limpa
- [ ] Documentação de instalação
- [ ] Arquivo de licença incluído
- [ ] Versão documentada
- [ ] Changelog atualizado

---

**🎉 Especificação completa para build profissional do Sistema CNAB Bradesco!** 