# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [1.2.0] - 2024-12-19

### Adicionado
- **🆕 Alteração Automática de Cabeçalho**: Editor gráfico agora atualiza automaticamente o cabeçalho com código específico da TC SECURITIZADORA
- **🔧 Edição Segura Aprimorada**: Método `_alterar_header_codigo_empresa` para modificação pontual do header
- **📋 Mensagens Melhoradas**: Feedback detalhado sobre alterações no cabeçalho durante salvamento

### Alterado
- **🔄 Método `_editar_cnab_seguro`**: Agora processa e altera headers automaticamente
- **💾 Fluxo de Salvamento**: Integração da alteração de cabeçalho no processo de salvamento do editor gráfico

### Corrigido
- **🛡️ Dados Sensíveis**: Substituição de CNPJs reais por valores exemplo no código
- **📁 Estrutura de Projeto**: Remoção de referências a arquivos com dados reais

### Segurança
- **🔒 Proteção de Dados**: Anonimização de informações sensíveis no código fonte
- **📊 .gitignore**: Configuração abrangente para evitar commit de dados sensíveis

## [1.1.0] - 2024-11-15

### Adicionado
- **🎨 Interface Horizontal**: Redesign completo do editor gráfico com layout otimizado
- **📊 Importação de Planilhas**: Funcionalidade para aplicar mapeamentos em lote via Excel
- **🔄 CNAB sem Juros**: Geração de arquivos CNAB com juros zerados diretamente do editor
- **💾 Edição Segura**: Tecnologia de preservação 100% da integridade do arquivo original

### Alterado
- **🖥️ Layout do Editor**: Interface horizontal otimizada para telas widescreen
- **📋 Organização de Controles**: Divisão em painéis esquerdo (70%) e direito (30%)
- **🎯 Experiência do Usuário**: Melhor aproveitamento do espaço da tela

## [1.0.0] - 2024-10-01

### Adicionado
- **📄 Processamento CNAB 400**: Leitura e interpretação de arquivos CNAB Bradesco
- **🎨 Interface Gráfica**: Interface moderna em PyQt5
- **📊 Exportação**: Suporte para CSV e Excel (XLSX)
- **✏️ Editor Gráfico**: Edição visual de campos NOSSO_NUMERO e CODIGO_EMPRESA
- **📈 Relatórios**: Geração de relatórios detalhados
- **⚡ Processamento em Lote**: Processamento de múltiplos arquivos
- **💰 Formatação Monetária**: Padrão brasileiro (R$ 1.234,56)
- **🔧 Editor Interativo**: Interface de linha de comando para edições pontuais

### Funcionalidades Principais
- Leitura de arquivos CNAB 400 de retorno do Bradesco
- Extração de dados de header, detalhes e trailer
- Interface gráfica intuitiva
- Exportação para múltiplos formatos
- Geração de arquivos CNAB de retorno
- Tratamento robusto de arquivos não padrão

## Tipos de Mudanças
- `Adicionado` para novas funcionalidades
- `Alterado` para mudanças em funcionalidades existentes
- `Descontinuado` para funcionalidades que serão removidas em breve
- `Removido` para funcionalidades removidas
- `Corrigido` para correções de bugs
- `Segurança` para vulnerabilidades corrigidas 