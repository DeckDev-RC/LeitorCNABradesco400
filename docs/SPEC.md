# Especificação de Compilação - Processador CNAB Bradesco

## 1. Visão Geral do Projeto
O projeto é um processador de arquivos CNAB do Bradesco com interface gráfica em PyQt5, que permite processar arquivos de retorno bancário e gerar relatórios em Excel.

## 2. Estrutura do Projeto
```
.
├── cnab_bradesco_gui.py    # Interface gráfica principal
├── cnab_bradesco.py        # Lógica de processamento CNAB
├── cnab_processor.py       # Processador base CNAB
├── iniciar.py             # Ponto de entrada da aplicação
├── processar_lote.py      # Processamento em lote
├── icon.ico               # Ícone do aplicativo
└── requirements.txt       # Dependências do projeto
```

## 3. Requisitos de Sistema

### 3.1. Requisitos de Software
- Python 3.8 ou superior
- Sistema Operacional: Windows 10/11
- Memória RAM: 4GB mínimo
- Espaço em Disco: 500MB mínimo

### 3.2. Dependências Python
- pandas==2.0.3
- tabulate==0.9.0
- PyQt5==5.15.9
- openpyxl==3.1.2
- pyinstaller==6.3.0 (apenas para compilação)

## 4. Processo de Compilação

### 4.1. Preparação do Ambiente
```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
.\venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt
pip install pyinstaller==6.3.0
```

### 4.2. Configuração do PyInstaller
Criar arquivo `app.spec`:

```python
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['iniciar.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'pandas',
        'PyQt5',
        'openpyxl',
        'tabulate'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    name='Processador CNAB Bradesco',
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
    icon='icon.ico'
)
```

### 4.3. Processo de Build
```bash
# Compilar o aplicativo
pyinstaller app.spec --clean

# O executável será gerado em:
# dist/Processador CNAB Bradesco.exe
```

## 5. Estrutura do Executável
O executável final será um arquivo único (.exe) que incluirá:
- Todas as dependências Python necessárias
- Interface gráfica PyQt5
- Ícone personalizado
- Sem necessidade de console

## 6. Testes Pós-Compilação

### 6.1. Verificações Básicas
- Inicialização do aplicativo
- Carregamento da interface gráfica
- Processamento de arquivo CNAB
- Geração de relatório Excel
- Verificação de memória utilizada

### 6.2. Casos de Teste
1. Processamento de arquivo CNAB válido
2. Tentativa de processamento de arquivo inválido
3. Geração de relatório Excel
4. Processamento em lote
5. Verificação de mensagens de erro

## 7. Distribuição

### 7.1. Estrutura do Pacote de Distribuição
```
Processador CNAB Bradesco/
├── Processador CNAB Bradesco.exe
└── README.txt
```

### 7.2. Requisitos Mínimos para Execução
- Windows 10/11
- 4GB RAM
- 500MB espaço em disco
- Não requer instalação do Python

## 8. Manutenção

### 8.1. Atualizações
- Versionar o executável seguindo SemVer
- Manter changelog de alterações
- Backup do spec e configurações de build

### 8.2. Logs e Diagnóstico
- Logs são salvos em %APPDATA%/Processador CNAB Bradesco/logs
- Incluir data e hora nos logs
- Rotação de logs a cada 7 dias

## 9. Segurança
- Verificação de integridade do arquivo CNAB
- Validação de dados de entrada
- Proteção contra injeção de dados maliciosos
- Tratamento seguro de arquivos temporários

## 10. Performance
- Tempo máximo de inicialização: 3 segundos
- Processamento de arquivo: máximo 5 segundos por 1000 registros
- Uso máximo de memória: 500MB
- Tempo de resposta da interface: máximo 100ms 