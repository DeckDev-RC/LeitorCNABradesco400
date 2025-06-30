# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [1.2.2] - 2024-12-19

### Melhorado
- **🔤 Validação Alfanumérica**: Sistema agora aceita valores como "49635C" (número + letra)
- **📊 Exemplos Práticos**: Planilha de exemplo focada em casos reais de uso
- **🎯 Casos Específicos**: Documentação para acréscimo de letras (49635 → 49635C)
- **🔧 Mapeamento Robusto**: Correção na aplicação de mapeamentos da planilha
- **✅ Suporte Completo**: Aceita qualquer combinação alfanumérica (ABC123, 12345Z, etc.)

### Adicionado
- **📝 Exemplos de Transformação**: Casos específicos como 49635 → 49635C
- **🔤 Documentação Alfanumérica**: Guia para valores número+letra
- **✨ Casos de Uso Reais**: Exemplos baseados em necessidades práticas

## [1.2.1] - 2024-12-19

### Adicionado
- **✏️ Editor Gráfico**: Adicionada edição do campo SEU_NUMERO (parte antes da barra)
- **🔍 Filtros Avançados**: Filtro de busca por Seu Número no editor gráfico
- **🔧 Edição em Lote**: Aplicação em massa para parte antes da barra do Seu Número
- **✅ Validação Inteligente**: Preservação automática da parte após a barra (/)
- **📊 Mapeamento SEU_NUMERO**: Importação via planilha com colunas simplificadas
- **🔤 Suporte Alfanumérico**: Aceita números + letras (ex: 49635C, ABC123)

### Alterado
- **📋 Interface do Editor**: Título e descrições atualizados para incluir SEU_NUMERO
- **🎯 Funcionalidade Expandida**: Editor gráfico agora suporta 3 campos editáveis

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