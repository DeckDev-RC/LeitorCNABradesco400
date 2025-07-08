# 📄 Sistema de Processamento CNAB 400 - Bradesco

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyQt5](https://img.shields.io/badge/PyQt5-5.15.9-green.svg)](https://pypi.org/project/PyQt5/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/Version-1.2.0-red.svg)](CHANGELOG.md)

Sistema completo para leitura, processamento e análise de arquivos CNAB 400 de cobrança do Banco Bradesco (código 237). Oferece interface gráfica moderna, edição segura de registros e exportação para múltiplos formatos.

## ✨ Principais Características

- 🛡️ **Edição Segura**: Tecnologia revolucionária que preserva 100% da integridade dos arquivos
- 🎨 **Interface Moderna**: Layout horizontal otimizado para telas widescreen
- ✏️ **Editor Gráfico**: Edição visual intuitiva de campos NOSSO_NUMERO, CODIGO_EMPRESA e SEU_NUMERO (parte antes da barra)
- 📊 **Múltiplos Formatos**: Exportação para CSV, Excel e geração de CNAB
- ⚡ **Processamento em Lote**: Processa múltiplos arquivos simultaneamente
- 💰 **Formatação Brasileira**: Valores monetários no padrão nacional (R$ 1.234,56)

## Funcionalidades
- Leitura e interpretação de arquivos CNAB 400 de retorno
- Extração de dados de header, detalhes e trailer
- Interface gráfica moderna e intuitiva com layout horizontal otimizado
- Exportação para formatos CSV e Excel (XLSX)
- Geração de arquivo CNAB de retorno sem juros/multa
- **🛡️ NOVA: Edição Segura de Arquivos** - Tecnologia revolucionária que preserva 100% da integridade
- Editor gráfico horizontal para edição de campos NOSSO_NUMERO e CODIGO_EMPRESA **com segurança total**
- Geração de CNAB sem juros com modificações do editor gráfico aplicadas **usando edição segura**
- Interface adaptável para telas widescreen e compatível com barra de tarefas
- Processamento em lote de múltiplos arquivos
- Formatação monetária no padrão brasileiro (R$ 1.234,56)
- Tratamento robusto para arquivos CNAB com formato não padrão ou sem sequencial

## 🚀 Instalação

### Pré-requisitos
- Python 3.8 ou superior
- Windows 10/11 (recomendado)
- 4GB RAM mínimo
- 500MB espaço em disco

### Instalação via Git
```bash
# Clonar o repositório
git clone https://github.com/seu-usuario/cnab-bradesco.git
cd cnab-bradesco

# Criar ambiente virtual (recomendado)
python -m venv venv

# Ativar ambiente virtual
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### Instalação Manual
1. Baixe o código fonte
2. Extraia para uma pasta de sua escolha
3. Execute: `pip install -r requirements.txt`

## ⚙️ Configuração
O sistema funciona sem configurações adicionais. Para personalizar:
- Modifique códigos de empresa nos arquivos de configuração
- Ajuste formatos de data/hora conforme necessário

## Uso

### Interface Gráfica
```bash
python iniciar.py
# Ou diretamente:
python cnab_bradesco_gui.py
```

### Processamento via Linha de Comando
```bash
python cnab_bradesco.py
```

### Processamento em Lote
```bash
python processar_lote.py
```

## Exemplos de Uso

### Processamento de um Único Arquivo
1. Execute o sistema via interface gráfica
2. Clique em "Selecionar Arquivo" e escolha um arquivo CNAB 400
3. Clique em "Processar Arquivo"
4. Visualize os dados na tabela
5. Utilize os botões para exportar para CSV, Excel ou gerar CNAB de retorno

### Editor Gráfico
1. Após processar um arquivo CNAB, clique no botão "✏️ Editor Gráfico"
2. Use a interface visual horizontal para editar campos NOSSO_NUMERO e CODIGO_EMPRESA
3. **Painel Esquerdo**: Filtros e tabela de registros (70% da tela)
4. **Painel Direito**: Controles de edição em lote e importação (30% da tela)
5. Aplique filtros para localizar registros específicos
6. Use edição em lote para alterar múltiplos registros
7. Clique em "🔄 Gerar CNAB sem Juros" para criar arquivo com modificações e juros zerados
8. Ou clique em "💾 Salvar Alterações" para gerar arquivo apenas com as modificações

### Processamento em Lote
1. Execute o módulo de processamento em lote
2. Informe o diretório contendo os arquivos CNAB
3. Defina se deseja exportar para Excel e gerar arquivos CNAB de retorno
4. Aguarde o processamento ser concluído
5. Verifique os resultados na pasta de saída gerada

## 📁 Estrutura do Projeto

```
cnab-bradesco/
├── 📄 cnab_bradesco.py              # Classe principal de processamento
├── 🎨 cnab_bradesco_gui.py          # Interface gráfica PyQt5
├── ⚡ processar_lote.py             # Processamento em lote
├── 🚀 iniciar.py                    # Script de inicialização
├── 📋 requirements.txt              # Dependências do projeto
├── 📊 cnab_processor.py             # Processador base CNAB
├── 🎯 main.py                       # Ponto de entrada alternativo
├── 📝 README.md                     # Documentação principal
├── 📈 CHANGELOG.md                  # Histórico de versões
├── ⚖️ LICENSE                       # Licença MIT
├── 🔧 .gitignore                    # Arquivos ignorados pelo Git
├── 📖 docs/                         # Documentação adicional
│   ├── FORMATACAO_MONETARIA.md     # Formatação monetária
│   ├── NOVAS_FUNCIONALIDADES.md    # Novas funcionalidades
│   └── TRATAMENTO_CNAB_SEM_SEQUENCIAL.md
└── 🐍 scripts python/              # Scripts de exemplo e teste
    ├── exemplo_planilha_mapeamentos.py
    ├── teste_edicao_segura.py
    └── ...
```

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Changelog

Veja [CHANGELOG.md](CHANGELOG.md) para histórico de versões e mudanças.

## ⚖️ Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🆘 Suporte

- 📖 Documentação completa em `/docs`
- 🐛 Reporte bugs via [Issues](https://github.com/seu-usuario/cnab-bradesco/issues)
- 💡 Sugestões via [Discussions](https://github.com/seu-usuario/cnab-bradesco/discussions)

## 🏷️ Tags

`cnab` `bradesco` `python` `pyqt5` `processamento-arquivos` `interface-grafica` `banco` `cobranca` `financeiro` 