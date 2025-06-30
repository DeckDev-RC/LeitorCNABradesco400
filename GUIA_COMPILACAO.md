# 🚀 Guia Rápido de Compilação - Sistema CNAB Bradesco

## ⚡ Compilação Express (1 Minuto)

### Windows
```bash
# 1. Instalar dependências
build.bat deps

# 2. Compilar aplicativo
build.bat
```

### Linha de Comando
```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Compilar aplicativo
python build.py
```

## 📋 Pré-requisitos

- ✅ **Python 3.8+** instalado
- ✅ **pip** funcionando
- ✅ **4GB RAM** disponível
- ✅ **2GB espaço** em disco
- ✅ **Windows 10/11** (recomendado)

## 🎯 Opções de Build

### 🔧 Build Completo (Recomendado)
```bash
python build.py
# ou
build.bat
```
**Gera:** Interface gráfica + Console + Pacote completo

### 🎨 Apenas Interface Gráfica
```bash
python build.py --gui-only
# ou
build.bat gui
```
**Gera:** `Sistema CNAB Bradesco.exe`

### 💻 Apenas Versão Console
```bash
python build.py --console-only
# ou
build.bat console
```
**Gera:** `CNAB Bradesco Console.exe`

## 📁 Estrutura de Saída

```
dist/
├── Sistema CNAB Bradesco.exe      # Interface gráfica (80-120MB)
└── CNAB Bradesco Console.exe      # Versão console (60-90MB)

CNAB_Bradesco_v1.2.0/              # Pacote de distribuição
├── Sistema CNAB Bradesco.exe
├── CNAB Bradesco Console.exe
├── exemplos/
├── README.md
├── LICENSE
├── CHANGELOG.md
└── LEIA-ME.txt
```

## ⚙️ Configurações Avançadas

### 🧹 Limpeza de Builds
```bash
python build.py --clean
# ou
build.bat clean
```

### 🔧 Compilação Manual com PyInstaller
```bash
# Interface gráfica
pyinstaller app.spec

# Console
pyinstaller cnab_console.spec
```

## 📊 Métricas Esperadas

| Métrica | Valor |
|---------|-------|
| **Tamanho GUI** | 80-120MB |
| **Tamanho Console** | 60-90MB |
| **Tempo de Build** | 2-5 minutos |
| **Tempo de Inicialização** | 2-4 segundos |
| **RAM em Execução** | 150-300MB |

## 🔍 Solução de Problemas

### ❌ "Module not found"
```bash
# Instalar dependência específica
pip install nome_do_modulo

# Ou reinstalar todas
pip install -r requirements.txt --force-reinstall
```

### ❌ "PyInstaller not found"
```bash
pip install pyinstaller>=6.0.0
```

### ❌ Executável muito grande
- ✅ Normal: 80-120MB
- ⚠️ Atenção: >150MB
- ❌ Problema: >200MB

### ❌ Erro de DLL no Windows
```bash
# Baixar Visual C++ Redistributable
# https://aka.ms/vs/16/release/vc_redist.x64.exe
```

## 🧪 Testes Pós-Compilação

### ✅ Checklist Básico
- [ ] Executável inicia sem erro
- [ ] Interface gráfica carrega
- [ ] Menu principal funciona
- [ ] Processamento CNAB operacional
- [ ] Exportação Excel funciona
- [ ] Tamanho do arquivo aceitável

### 🔍 Testes Avançados
```bash
# Teste de inicialização rápida
Sistema\ CNAB\ Bradesco.exe --version

# Teste de processamento
# (usar arquivo exemplo da pasta exemplos/)
```

## 🚀 Distribuição

### 📦 Pacote Pronto para Distribuição
- Localização: `CNAB_Bradesco_v1.2.0/`
- Conteúdo: Executáveis + Documentação + Exemplos
- Pronto para: Upload, compartilhamento, instalação

### 🌐 Publicação
```bash
# Compactar para distribuição
zip -r CNAB_Bradesco_v1.2.0.zip CNAB_Bradesco_v1.2.0/

# Ou usar WinRAR/7zip no Windows
```

## 📞 Suporte

### 🆘 Problemas de Build
1. Verificar Python e pip
2. Reinstalar dependências
3. Limpar builds anteriores
4. Verificar espaço em disco

### 📧 Contato
- **Issues:** GitHub Issues
- **Documentação:** `docs/`
- **Exemplos:** `exemplos/`

---

**🎉 Pronto! Seu aplicativo CNAB Bradesco está compilado e pronto para uso!** 