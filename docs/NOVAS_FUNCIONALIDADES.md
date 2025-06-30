# Novas Funcionalidades - Sistema CNAB Bradesco

## Exportação para Excel (XLSX)

### Descrição
A exportação para Excel (XLSX) permite que os dados processados dos arquivos CNAB 400 sejam salvos em um formato mais rico e estruturado que o CSV. Os arquivos Excel gerados contêm:

1. **Planilha de Detalhes**: Contém todos os registros de detalhes (tipo 1) do arquivo CNAB com todas as informações extraídas.
2. **Planilha de Resumo**: Contém informações resumidas como:
   - Banco e código
   - Nome da empresa
   - Data de geração
   - Data de crédito
   - Total de títulos
   - Valor total dos títulos

### Como usar

#### Na Interface Gráfica
1. Carregue um arquivo CNAB 400
2. Clique em "Processar Arquivo"
3. Após o processamento, clique no botão "Exportar para Excel"
4. Escolha o local e nome do arquivo a ser salvo

#### Na Linha de Comando
Ao processar um arquivo CNAB via linha de comando, o arquivo Excel será gerado automaticamente na mesma pasta com o nome do arquivo original acrescido de "_processado.xlsx".

#### No Processamento em Lote
1. Execute o processamento em lote
2. Quando solicitado, responda "s" para "Deseja exportar os dados para Excel?"
3. Os arquivos Excel individuais e um arquivo consolidado serão gerados na pasta de resultados

## Geração de CNAB de Retorno

### Descrição
A funcionalidade de geração de CNAB de retorno permite criar um novo arquivo no formato CNAB 400 com os juros/multa zerados, mantendo a estrutura original do arquivo. Esta funcionalidade é útil para:

1. Gerar arquivos de retorno para o banco sem os valores de juros/multa
2. Preservar a formatação original CNAB 400 exigida pelo banco
3. Zerar automaticamente os campos de juros (posição 266-279)

### Como usar

#### Na Interface Gráfica
1. Carregue um arquivo CNAB 400
2. Clique em "Processar Arquivo"
3. Após o processamento, clique no botão "Gerar CNAB de Retorno"
4. Escolha o local e nome do arquivo a ser salvo

#### Na Linha de Comando
Ao processar um arquivo CNAB via linha de comando, será perguntado se deseja gerar o arquivo CNAB de retorno. Responda "s" para gerar o arquivo na mesma pasta com o nome do arquivo original acrescido de "_retorno.TXT".

#### No Processamento em Lote
1. Execute o processamento em lote
2. Quando solicitado, responda "s" para "Deseja gerar arquivos CNAB de retorno sem juros?"
3. Os arquivos CNAB de retorno serão gerados na pasta de resultados

## 📊 Conversão Excel para CNAB 400

### Descrição
Nova funcionalidade que permite converter arquivos Excel (gerados pelo próprio sistema) de volta para o formato CNAB 400 do Bradesco.

### Como Usar

#### Interface Gráfica
1. Execute `python cnab_bradesco_gui.py`
2. Clique no botão **"Excel → CNAB"**
3. Selecione o arquivo Excel que deseja converter
4. Escolha se quer usar um arquivo CNAB como referência para header/trailer
5. Defina onde salvar o arquivo CNAB gerado

#### Programaticamente
```python
from cnab_bradesco import CNABBradesco

# Criar instância do processador
processador = CNABBradesco("")

# Converter Excel para CNAB
sucesso, mensagem = processador.excel_para_cnab(
    arquivo_excel="dados_processados.xlsx",
    arquivo_cnab_saida="arquivo_convertido.TXT",
    arquivo_cnab_referencia="arquivo_original.TXT"  # Opcional
)

if sucesso:
    print(f"Conversão realizada: {mensagem}")
else:
    print(f"Erro na conversão: {mensagem}")
```

### 🔄 Processo Bidirecional Completo

O sistema agora suporta **processo 100% bidirecional**:

1. **CNAB → Excel**: Extrai TODOS os campos para o Excel
2. **Edição no Excel**: Permite alterações em qualquer campo
3. **Excel → CNAB**: Reconstrói o CNAB preservando TODAS as alterações

### Campos Suportados (Bidirecional)
Todos os campos abaixo podem ser extraídos, editados e reconvertidos:

| Campo Excel | Posição CNAB | Descrição |
|-------------|--------------|-----------|
| `tipo_registro` | 1 | Tipo de registro (1 para detalhe) |
| `codigo_inscricao` | 2-3 | Código de inscrição (01=CPF, 02=CNPJ) |
| `numero_inscricao` | 4-17 | CNPJ/CPF da empresa |
| `codigo_empresa` | 21-37 | Código da empresa no banco |
| `nosso_numero` | 71-82 | Nosso número do título |
| `carteira` | 108-109 | Carteira de cobrança |
| `data_ocorrencia` | 111-116 | Data de ocorrência (DDMMAA) |
| `seu_numero` | 117-126 | Seu número (identificação do cliente) |
| `data_vencimento` | 147-152 | Data de vencimento (DDMMAA) |
| `valor_titulo` | 153-165 | Valor original do título |
| `banco_cobrador` | 166-168 | Código do banco cobrador |
| `agencia_cobradora` | 169-173 | Agência cobradora |
| `especie` | 174-175 | Espécie do documento |
| `valor_tarifa` | 176-188 | Valor da tarifa bancária |
| `valor_iof` | 189-201 | Valor do IOF |
| `valor_abatimento` | 228-240 | Valor de abatimento |
| `descontos` | 241-253 | Valor de descontos |
| `valor_principal` | 254-266 | Valor efetivamente pago |
| `juros_mora_multa` | 267-279 | Juros de mora e multa |
| `outros_creditos` | 280-292 | Outros créditos |
| `data_credito` | 296-301 | Data de crédito (DDMMAA) |
| `motivo_ocorrencia` | 319-328 | Motivo da ocorrência |
| `sequencial` | 395-400 | Número sequencial do registro |

**Total: 23 campos suportados** ✅

### Funcionalidades Técnicas

#### Conversão de Formatos
- **Valores Monetários**: Converte "R$ 1.234,56" para centavos (123456)
- **Datas**: Converte "DD/MM/YYYY" para "DDMMAA"
- **Sequencial**: Gera automaticamente números sequenciais

#### Header e Trailer
- **Modo Padrão**: Cria header/trailer padrão com dados básicos
- **Modo Referência**: Usa header/trailer de arquivo CNAB existente

#### Validações
- Verifica colunas obrigatórias (`nosso_numero`, `valor_titulo`)
- Valida formato dos dados
- Trata campos vazios ou inválidos

### Exemplo de Uso

#### 1. Criando Excel de Teste
```python
import pandas as pd

dados = [
    {
        'nosso_numero': '12345678901',
        'seu_numero': 'TESTE001',
        'valor_titulo': 1500.50,
        'data_ocorrencia': '15/12/2024',
        'data_vencimento': '20/12/2024',
        'data_credito': '15/12/2024',
        'carteira': '09'
    }
]

df = pd.DataFrame(dados)
df.to_excel('exemplo.xlsx', index=False)
```

#### 2. Convertendo para CNAB
```python
from cnab_bradesco import CNABBradesco

processador = CNABBradesco("")
sucesso, msg = processador.excel_para_cnab(
    'exemplo.xlsx', 
    'convertido.TXT'
)
```

### Script de Teste
Execute o script de teste para ver a funcionalidade em ação:

```bash
cd "scripts python"
python teste_excel_para_cnab.py
```

### 🚀 Workflow Bidirecional

#### **Cenário 1: Correção de Dados**
```
CNAB Original → Excel → Editar no Excel → CNAB Corrigido
```
1. Processa arquivo CNAB do banco
2. Exporta para Excel com todos os campos
3. Edita valores, datas, juros no Excel
4. Gera novo CNAB com as correções

#### **Cenário 2: Análise e Ajustes**
```
CNAB → Excel → Análise/Relatórios → Ajustes → CNAB Final
```
1. Converte CNAB para Excel
2. Faz análises e relatórios
3. Aplica ajustes baseados na análise
4. Reconverte para CNAB preservando tudo

#### **Cenário 3: Integração com Outros Sistemas**
```
Sistema A → Excel → CNAB → Banco
```
1. Exporta dados de qualquer sistema para Excel
2. Formata colunas conforme especificação
3. Converte Excel para CNAB válido
4. Envia para o banco

### Casos de Uso

1. **✏️ Correção de Dados**: Editar valores, datas, juros no Excel
2. **📊 Análise Financeira**: Usar Excel para análises e depois regenerar CNAB
3. **🔄 Integração**: Converter dados de outros sistemas via Excel
4. **💾 Backup Editável**: Manter dados em formato editável
5. **🎯 Workflow Completo**: CNAB → Análise → Edição → CNAB

### Limitações

- Requer colunas obrigatórias no Excel
- Formatos de data devem seguir padrão DD/MM/YYYY
- Valores monetários podem estar em formato brasileiro ou decimal
- Arquivo gerado segue especificação CNAB 400 Bradesco

### Benefícios

✅ **Flexibilidade**: Editar dados facilmente no Excel  
✅ **Integração**: Trabalhar com dados de múltiplas fontes  
✅ **Correção**: Corrigir erros sem reprocessar arquivo original  
✅ **Automação**: Integrar com outros sistemas via Excel  
✅ **Backup**: Manter dados em formato editável  

### Correções Implementadas

#### ✅ **Correção v1.1 - Tratamento de Tipos de Dados**
- **Problema**: Erro `'float' object has no attribute 'strip'`
- **Solução**: Tratamento robusto de diferentes tipos de dados do pandas
- **Melhorias**:
  - Detecção automática de tipos (int, float, string, None, NaN)
  - Conversão segura antes de operações de string
  - Tratamento de valores nulos e vazios
  - Suporte a diferentes formatos monetários

```python
# Agora funciona com qualquer tipo de dado:
dados = [
    {'nosso_numero': 12345678901},      # int
    {'nosso_numero': '12345678902'},    # string  
    {'valor_titulo': 1500.50},          # float
    {'valor_titulo': 'R$ 1.234,56'},    # string formatada
    {'seu_numero': None},               # None
    {'carteira': np.nan}                # NaN
]
```

#### ✅ **Correção v1.2 - Formato CNAB Correto**
- **Problema**: Arquivo gerado não seguia exatamente o formato do modelo
- **Solução**: Análise detalhada do arquivo modelo e correção de posições
- **Melhorias**:
  - Header com estrutura completa CNAB 400 Bradesco
  - Campos de detalhe posicionados corretamente
  - CNPJ e código da empresa extraídos do arquivo de referência
  - Banco cobrador (237) e agência preenchidos automaticamente
  - Valor pago igual ao valor do título
  - Trailer com códigos e estrutura corretos

### Scripts de Teste Atualizados
```bash
cd "scripts python"
# Teste básico de tipos de dados
python teste_excel_para_cnab_corrigido.py

# Teste de formato correto
python teste_excel_cnab_formato_correto.py

# Demonstração do processo bidirecional completo
python teste_processo_bidirecional.py
```

### Próximos Passos

- [ ] Suporte a mais campos opcionais
- [ ] Validação avançada de dados
- [ ] Templates de Excel pré-formatados
- [ ] Conversão em lote de múltiplos arquivos

---

*Funcionalidade implementada em dezembro de 2024*  
*Correção v1.1 - dezembro de 2024*

## Destaques das Melhorias

- **Exportação Avançada**: Além do formato CSV, agora os dados podem ser exportados para Excel com múltiplas planilhas e formatação adequada.
- **Formatação Monetária**: Todos os valores monetários são formatados no padrão brasileiro (R$ 1.234,56).
- **Múltiplas Planilhas**: Os arquivos Excel contêm planilhas separadas para detalhes e resumo.
- **Arquivo Consolidado**: No processamento em lote, é gerado um arquivo Excel consolidado com todos os registros e resumos por arquivo.
- **Integridade do CNAB**: A geração de arquivos CNAB de retorno preserva a estrutura original, alterando apenas os campos de juros.

## Requisitos

- Python 3.6 ou superior
- Pandas (para processamento de dados)
- Openpyxl (para geração de arquivos Excel)
- PyQt5 (para interface gráfica)

## Limitações Conhecidas

- Os arquivos CNAB gerados devem ser validados antes do envio ao banco
- A formatação específica do CNAB pode variar conforme atualizações do banco 

## 📋 Índice
1. [Conversão Excel → CNAB (Bidirecional)](#conversão-excel--cnab-bidirecional)
2. [Editor Interativo de CNAB](#editor-interativo-de-cnab)

---

## Conversão Excel → CNAB (Bidirecional)

### Descrição
Funcionalidade que permite converter arquivos Excel de volta para formato CNAB 400, completando o processo bidirecional: CNAB → Excel → CNAB. Isso permite que usuários façam alterações em planilhas Excel e reconvertam para CNAB preservando todas as modificações.

### Como Usar

#### Via Interface Gráfica
1. Carregue um arquivo CNAB primeiro
2. Clique no botão **"Excel → CNAB"**
3. Selecione o arquivo Excel para conversão
4. Escolha onde salvar o novo arquivo CNAB
5. Opcionalmente, use um arquivo CNAB de referência para header/trailer

#### Via Script
```python
from cnab_bradesco import CNABBradesco

# Criar instância
processador = CNABBradesco("")

# Converter Excel para CNAB
sucesso, mensagem = processador.excel_para_cnab(
    "arquivo.xlsx",           # Arquivo Excel fonte
    "novo_arquivo.TXT",       # Arquivo CNAB destino
    "referencia.TXT"          # Arquivo de referência (opcional)
)

if sucesso:
    print("Conversão realizada com sucesso!")
else:
    print(f"Erro: {mensagem}")
```

### Campos Suportados (23 campos bidirecionais)
- **Identificação**: `tipo_registro`, `codigo_inscricao`, `numero_inscricao`
- **Empresa**: `codigo_empresa`, `nosso_numero`, `seu_numero`, `carteira`
- **Datas**: `data_ocorrencia`, `data_vencimento`, `data_credito`
- **Valores**: `valor_titulo`, `valor_principal`, `valor_tarifa`, `valor_iof`
- **Ajustes**: `valor_abatimento`, `descontos`, `juros_mora_multa`, `outros_creditos`
- **Controle**: `banco_cobrador`, `agencia_cobradora`, `especie`, `motivo_ocorrencia`, `sequencial`

### Casos de Uso
- **Correção de Dados**: Editar valores incorretos em planilhas Excel
- **Análise Financeira**: Usar recursos avançados do Excel para análises
- **Integração de Sistemas**: Facilitar troca de dados entre sistemas
- **Backup Editável**: Manter versões editáveis dos dados CNAB

---

## Editor Interativo de CNAB

### Descrição
**🆕 NOVA FUNCIONALIDADE** - Editor interativo que permite fazer alterações pontuais em dados CNAB diretamente no terminal/console, oferecendo uma interface amigável para modificações rápidas sem precisar usar Excel.

### Como Usar

#### Via Interface Gráfica
1. Carregue um arquivo CNAB primeiro
2. Clique no botão **"📝 Editor Interativo"**
3. O editor será aberto no terminal/console
4. Siga as instruções na tela para fazer alterações

#### Via Script
```python
from cnab_bradesco import CNABBradesco

# Carregar arquivo
processador = CNABBradesco("arquivo.TXT")
processador.ler_arquivo()

# Abrir editor interativo
resultado = processador.editor_interativo()

if resultado:
    print("Alterações salvas com sucesso!")
```

### Funcionalidades do Editor

#### 1. Visualização de Registros
- Lista todos os registros com informações principais
- Mostra nosso número, valor, vencimento e status
- Navegação paginada para arquivos grandes

#### 2. Busca de Registros
- Busca por nosso número ou seu número
- Filtros flexíveis (busca parcial)
- Acesso direto para edição do registro encontrado

#### 3. Edição Individual
- Edição campo por campo de qualquer registro
- Validação automática dos valores inseridos
- Preview das alterações antes de confirmar

#### 4. Edição em Lote - Valores
- **Adicionar percentual**: Reajuste proporcional em todos os títulos
- **Adicionar valor fixo**: Acréscimo de valor fixo em todos os títulos
- **Zerar juros/multa**: Remove juros e multas de todos os registros
- **Aplicar desconto**: Desconto percentual em todos os valores

#### 5. Edição em Lote - Datas
- **Alterar data de crédito**: Nova data para todos os registros
- **Postergar vencimento**: Adiciona X dias a todos os vencimentos
- **Nova data de vencimento**: Define data única para todos

#### 6. Resumo e Controle
- Acompanha quantos registros foram alterados
- Mostra preview das principais alterações
- Validação antes de salvar

#### 7. Salvamento Seguro
- Gera novo arquivo com sufixo "_editado"
- Preserva arquivo original intacto
- Mantém formato CNAB 400 válido

### Campos Editáveis
- **Financeiros**: `valor_titulo`, `valor_principal`, `juros_mora_multa`, `valor_abatimento`, `descontos`, `outros_creditos`
- **Datas**: `data_vencimento`, `data_credito`
- **Identificação**: `seu_numero`, `carteira`

### Casos de Uso Práticos

#### 📈 Reajustes Financeiros
```
Cenário: Aplicar reajuste de 10% em todos os títulos
1. Usar opção "4 - Editar valores em lote"
2. Escolher "1 - Adicionar percentual"
3. Digitar "10" para 10%
4. Confirmar operação
5. Salvar alterações
```

#### 📅 Prorrogação de Vencimentos
```
Cenário: Postergar todos os vencimentos por 30 dias
1. Usar opção "5 - Alterar datas em lote"
2. Escolher "2 - Postergar vencimento por X dias"
3. Digitar "30" dias
4. Confirmar operação
5. Salvar alterações
```

#### 🔍 Correção Pontual
```
Cenário: Corrigir valor específico de um título
1. Usar opção "2 - Buscar registro específico"
2. Digitar nosso número ou seu número
3. Confirmar edição do registro encontrado
4. Escolher campo "Valor do Título"
5. Digitar novo valor
6. Salvar alterações quando terminar
```

#### 💰 Remoção de Juros
```
Cenário: Zerar juros de todos os títulos
1. Usar opção "4 - Editar valores em lote"
2. Escolher "3 - Zerar juros/multa"
3. Confirmar operação
4. Salvar alterações
```

#### 🔍 Correções Pontuais
```
Cenário: Corrigir registros específicos
1. Usar filtros para localizar registros
2. Duplo clique nas células para editar
3. Inserir valores corretos
4. Observar destaque visual das alterações
5. Salvar quando concluído
```

#### 📊 Mapeamentos via Planilha Excel
```
Cenário: Aplicar múltiplas substituições usando planilha
1. Criar planilha Excel com colunas:
   - NOSSO_NUMERO_ATUAL: números existentes no CNAB
   - NOSSO_NUMERO_CORRIGIDO: novos números desejados
2. Abrir Editor Gráfico
3. Clicar em "📁 Selecionar Planilha"
4. Escolher arquivo Excel
5. Verificar preview dos mapeamentos
6. Clicar em "🔄 Aplicar Mapeamentos"
7. Confirmar operação
8. Salvar arquivo CNAB editado
```

### Formatos Aceitos

#### Valores Monetários
- `1234.56` (formato decimal)
- `1234,56` (formato brasileiro)
- `R$ 1.234,56` (formato completo)
- `1.234,56` (com separadores)

#### Datas
- `DD/MM/AAAA` (formato brasileiro)
- Exemplo: `31/12/2024`
- Validação automática de datas válidas

### Segurança e Backup
- **Arquivo original preservado**: Nunca modifica o arquivo original
- **Novos arquivos**: Sempre gera arquivos com sufixo `_editado`
- **Rastreamento**: Registros alterados são marcados internamente
- **Validação**: Mantém integridade do formato CNAB 400

### Scripts de Demonstração
- `scripts python/teste_editor_interativo.py`: Demonstração completa da funcionalidade

### Vantagens do Editor Interativo
1. **Rapidez**: Alterações pontuais sem precisar de Excel
2. **Facilidade**: Interface simples e intuitiva
3. **Segurança**: Arquivo original sempre preservado
4. **Flexibilidade**: Edição individual ou em lote
5. **Validação**: Verificação automática de dados

---

## Editor Gráfico de Campos

### Descrição
**🆕 NOVA FUNCIONALIDADE** - Interface gráfica moderna e intuitiva para edição específica dos campos `NOSSO_NUMERO`, `CODIGO_EMPRESA` e `SEU_NUMERO` (parte antes da barra) em arquivos CNAB, oferecendo uma experiência visual superior ao editor de terminal.

### Como Usar

#### Via Interface Gráfica
1. Carregue um arquivo CNAB primeiro
2. Clique no botão **"✏️ Editor Gráfico"** (verde)
3. A janela do editor será aberta automaticamente
4. Use a interface visual para fazer alterações
5. Salve as alterações em um novo arquivo

### Funcionalidades do Editor Gráfico

#### 🎨 Interface Visual Moderna
- **Design Responsivo**: Interface adaptável com tema consistente
- **Tabela Interativa**: Visualização clara de todos os registros
- **Cores Temáticas**: Esquema de cores profissional e agradável
- **Ícones Intuitivos**: Elementos visuais que facilitam a navegação

#### 📋 Tabela de Edição Avançada
- **Colunas Visíveis**: Seq, Nosso Número, Código Empresa, Seu Número, Valor, Vencimento
- **Edição Direta**: Duplo clique nas células para editar
- **Campos Protegidos**: Apenas NOSSO_NUMERO e CODIGO_EMPRESA são editáveis
- **Destaque Visual**: Registros alterados ficam destacados em azul
- **Redimensionamento**: Colunas ajustáveis automaticamente

#### 🔍 Sistema de Filtros
- **Filtro por Nosso Número**: Busca rápida por números específicos
- **Filtro por Código da Empresa**: Localização por código
- **Busca Dinâmica**: Filtragem em tempo real conforme digitação
- **Limpeza Rápida**: Botão para remover todos os filtros

#### 🔧 Edição em Lote
- **Nosso Número em Massa**: Aplicar mesmo valor a todos os registros visíveis
- **Código Empresa em Massa**: Alterar código para múltiplos registros
- **Confirmação Obrigatória**: Diálogo de confirmação antes de aplicar
- **Contadores Visuais**: Mostra quantos registros serão afetados

#### 📊 Importação de Mapeamentos via Planilha
- **Seleção de Planilha Excel**: Importar arquivo .xlsx/.xls com mapeamentos
- **Colunas Obrigatórias**: `NOSSO_NUMERO_ATUAL` e `NOSSO_NUMERO_CORRIGIDO`
- **Preview Inteligente**: Mostra quantos registros serão afetados
- **Validação Automática**: Verifica formato e estrutura da planilha
- **Aplicação em Massa**: Substitui múltiplos nossos números de uma vez

#### ✅ Validação Inteligente
- **Nosso Número**: 
  - Letras e números permitidos (alfanumérico)
  - Máximo 12 caracteres
  - Validação em tempo real
- **Código Empresa**:
  - Alfanumérico permitido
  - Máximo 17 caracteres
  - Verificação de formato

#### 💾 Salvamento Seguro
- **Preview das Alterações**: Contador de registros modificados
- **Confirmação Visual**: Diálogo detalhado antes de salvar
- **Arquivo Original Preservado**: Nunca modifica o arquivo original
- **Novo Arquivo**: Gera arquivo com sufixo "_editado"

### Interface Detalhada

#### Cabeçalho Informativo
- **Título**: "Editor Gráfico de Campos"
- **Subtítulo**: "Edição dos campos NOSSO_NUMERO e CODIGO_EMPRESA"
- **Contador**: Total de registros carregados
- **Ícone Visual**: Emoji representativo da funcionalidade

#### Área de Filtros
- **Campo Nosso Número**: Busca com placeholder "Nosso Número..."
- **Campo Código Empresa**: Busca com placeholder "Código da Empresa..."
- **Botão Limpar**: Remove todos os filtros aplicados
- **Design Responsivo**: Layout horizontal otimizado

#### Tabela Principal
- **Coluna 1**: Sequencial (não editável, centralizado)
- **Coluna 2**: Nosso Número (editável, destaque especial)
- **Coluna 3**: Código Empresa (editável, destaque especial)
- **Coluna 4**: Seu Número (apenas visualização)
- **Coluna 5**: Valor (formatado como moeda, apenas visualização)
- **Coluna 6**: Vencimento (formato brasileiro, apenas visualização)

#### Área de Edição em Lote
- **Seção Nosso Número**:
  - Campo de entrada com placeholder
  - Botão "Aplicar a Todos"
  - Validação em tempo real
- **Seção Código Empresa**:
  - Campo de entrada com placeholder
  - Botão "Aplicar a Todos"
  - Verificação de formato
- **Separador Visual**: Linha divisória entre seções

#### Rodapé de Controle
- **Contador de Alterações**: Mostra quantos registros foram modificados
- **Botão Cancelar**: Fecha sem salvar (vermelho)
- **Botão Salvar**: Confirma e salva alterações (azul)
- **Estados Visuais**: Botões habilitados/desabilitados conforme contexto

### Casos de Uso Específicos

#### 🔢 Padronização de Nosso Número
```
Cenário: Padronizar todos os nossos números para um formato específico
1. Abrir Editor Gráfico
2. Usar edição em lote para Nosso Número
3. Digitar o novo padrão (ex: "000000123456")
4. Confirmar aplicação a todos os registros
5. Salvar alterações
```

#### 🏢 Alteração de Código da Empresa
```
Cenário: Migrar todos os registros para nova empresa
1. Abrir Editor Gráfico
2. Usar edição em lote para Código Empresa
3. Digitar o novo código da empresa
4. Confirmar alteração em massa
5. Salvar novo arquivo CNAB
```

#### 🔍 Correções Pontuais
```
Cenário: Corrigir registros específicos
1. Usar filtros para localizar registros
2. Duplo clique nas células para editar
3. Inserir valores corretos
4. Observar destaque visual das alterações
5. Salvar quando concluído
```

#### 📊 Mapeamentos via Planilha Excel
```
Cenário: Aplicar múltiplas substituições usando planilha
1. Criar planilha Excel com colunas:
   - NOSSO_NUMERO_ATUAL: números existentes no CNAB
   - NOSSO_NUMERO_CORRIGIDO: novos números desejados
2. Abrir Editor Gráfico
3. Clicar em "📁 Selecionar Planilha"
4. Escolher arquivo Excel
5. Verificar preview dos mapeamentos
6. Clicar em "🔄 Aplicar Mapeamentos"
7. Confirmar operação
8. Salvar arquivo CNAB editado
```

#### 📊 Revisão e Auditoria
```
Cenário: Revisar e validar dados antes de processar
1. Usar filtros para segmentar dados
2. Verificar valores nas colunas de visualização
3. Fazer correções necessárias nos campos editáveis
4. Usar contador de alterações para controle
5. Gerar arquivo final validado
```

### Vantagens do Editor Gráfico

#### 🎯 Foco Especializado
- **Campos Específicos**: Concentra apenas em NOSSO_NUMERO e CODIGO_EMPRESA
- **Interface Otimizada**: Design pensado especificamente para esses campos
- **Validação Direcionada**: Regras específicas para cada tipo de campo

#### 🚀 Produtividade
- **Edição Rápida**: Interface visual mais rápida que terminal
- **Filtros Dinâmicos**: Localização instantânea de registros
- **Edição em Lote**: Alterações em massa com poucos cliques
- **Feedback Visual**: Destaque imediato das alterações

#### 🛡️ Segurança
- **Validação em Tempo Real**: Erros detectados imediatamente
- **Confirmações**: Diálogos de confirmação para operações críticas
- **Preview**: Visualização das alterações antes de salvar
- **Backup Automático**: Arquivo original sempre preservado

#### 🎨 Experiência do Usuário
- **Interface Intuitiva**: Fácil de usar sem treinamento
- **Design Moderno**: Visual profissional e agradável
- **Responsividade**: Interface que se adapta ao conteúdo
- **Acessibilidade**: Elementos visuais claros e organizados

### Scripts de Demonstração
- `scripts python/teste_editor_grafico.py`: Demonstração completa da funcionalidade
- `scripts python/exemplo_planilha_mapeamentos.py`: Gerador de planilhas de exemplo (suporta alfanumérico)

### Integração com Sistema
- **Compatibilidade Total**: Funciona com todos os arquivos CNAB suportados
- **Preservação de Dados**: Mantém todos os outros campos inalterados
- **Formato CNAB**: Gera arquivos 100% compatíveis com o padrão
- **Sincronização**: Integra perfeitamente com outras funcionalidades do sistema

---

## Resumo das Funcionalidades

### Funcionalidades Disponíveis
1. **✅ Leitura de CNAB 400** - Processamento completo de arquivos de retorno
2. **✅ Exportação para Excel** - Conversão para planilhas editáveis
3. **✅ Exportação para CSV** - Formato universal de dados
4. **✅ Geração de CNAB sem Juros** - Arquivo de retorno zerado
5. **🆕 Excel → CNAB** - Conversão bidirecional completa
6. **🆕 Editor Interativo** - Edição avançada via terminal
7. **🆕 Editor Gráfico** - Interface visual para campos específicos

### Scripts de Teste Disponíveis
- `scripts python/teste_excel_cnab_formato_correto.py`
- `scripts python/teste_excel_para_cnab_corrigido.py`
- `scripts python/teste_processo_bidirecional.py`
- `scripts python/teste_editor_interativo.py`
- `scripts python/teste_editor_grafico.py`

---

## 🔄 Editor Gráfico com Geração de CNAB sem Juros

### Descrição
**🆕 NOVA FUNCIONALIDADE** - Expansão do editor gráfico com um novo botão que combina as modificações do editor com a geração de CNAB sem juros/multa, oferecendo um processo unificado e eficiente.

### Como Usar

#### Via Interface Gráfica
1. Carregue um arquivo CNAB primeiro
2. Clique no botão **"✏️ Editor Gráfico"**
3. Faça as modificações desejadas nos campos:
   - **NOSSO_NUMERO**: Edição individual ou em lote
   - **CODIGO_EMPRESA**: Edição individual ou em lote
4. Clique no novo botão **"🔄 Gerar CNAB sem Juros"** (verde)
5. Escolha onde salvar o arquivo resultado

### Nova Funcionalidade: Botão "🔄 Gerar CNAB sem Juros"

#### O que faz
- ✅ **Aplica TODAS as modificações** feitas no editor gráfico
- ✅ **Zera automaticamente** todos os valores de juros/multa
- ✅ **Gera um novo arquivo CNAB** completo e válido
- ✅ **Mantém os dados originais** intactos

#### Diferenças entre os botões

| Funcionalidade | 💾 Salvar Alterações | 🔄 Gerar CNAB sem Juros (NOVO) |
|----------------|----------------------|--------------------------------|
| Aplica modificações do editor | ✅ | ✅ |
| Mantém juros originais | ✅ | ❌ |
| Zera todos os juros/multa | ❌ | ✅ |
| Nome do arquivo | `_editado.TXT` | `_editado_sem_juros.TXT` |
| Cor do botão | Azul | Verde |

### Cenários de Uso

#### 🔄 Cenário 1: Alterar Nossos Números + Zerar Juros
```
Situação: Empresa mudou numeração e quer zerar juros
1. Abrir Editor Gráfico
2. Usar edição em lote para alterar nossos números
3. Clicar "🔄 Gerar CNAB sem Juros"
4. Resultado: Arquivo com novos números E sem juros
```

#### 🏢 Cenário 2: Alterar Códigos de Empresa + Zerar Juros
```
Situação: Mudança de código da empresa no banco
1. Abrir Editor Gráfico
2. Usar edição em lote para novo código da empresa
3. Clicar "🔄 Gerar CNAB sem Juros"
4. Resultado: Arquivo com novo código E sem juros
```

#### 💰 Cenário 3: Apenas Zerar Juros
```
Situação: Não há modificações, apenas remover juros
1. Abrir Editor Gráfico
2. Não fazer modificações
3. Clicar "🔄 Gerar CNAB sem Juros"
4. Resultado: Arquivo original com juros zerados
```

### Benefícios

✅ **Eficiência**: Processo unificado em 1 clique  
✅ **Flexibilidade**: Funciona com ou sem modificações  
✅ **Segurança**: Dados originais preservados  
✅ **Clareza**: Interface visual intuitiva  
✅ **Completude**: Combina duas funcionalidades essenciais  

### Scripts de Demonstração
- `scripts python/teste_editor_cnab_sem_juros.py`: Demonstração completa da nova funcionalidade
- `scripts python/teste_editor_horizontal.py`: Demonstração da nova interface horizontal

---

## 🖥️ Interface Horizontal do Editor Gráfico

### Descrição
**🆕 MELHORIA DE INTERFACE** - Redesign completo do editor gráfico com layout horizontal otimizado para melhor aproveitamento do espaço da tela e compatibilidade com a barra de tarefas do Windows.

### Problema Resolvido
A interface anterior tinha layout vertical que podia ser cortada pela barra de tarefas do Windows, especialmente em resoluções menores ou quando a barra de tarefas estava visível.

### Solução Implementada

#### Layout Horizontal com Divisão de Painéis
- **Painel Esquerdo (70%)**: Filtros + Tabela de registros
- **Painel Direito (30%)**: Controles de edição em lote + Importação de planilha
- **Divisor Redimensionável**: Permite ajustar proporções conforme necessário

#### Dimensões Otimizadas
- **Antes**: 1000x700px (mais alto que largo)
- **Agora**: 1400x600px (mais largo que alto)
- **Proporção**: Otimizada para telas widescreen modernas

### Melhorias Implementadas

#### 🎨 **Interface Visual**
- Layout horizontal com QSplitter redimensionável
- Scroll area no painel direito para evitar cortes
- Controles compactos e organizados verticalmente
- Melhor aproveitamento do espaço horizontal

#### 📏 **Organização dos Elementos**
- **Cabeçalho**: Mantido no topo com largura total
- **Filtros**: Movidos para o painel esquerdo junto com a tabela
- **Tabela**: Ocupa maior parte do espaço disponível
- **Controles**: Organizados em painel lateral direito
- **Botões**: Mantidos no rodapé com largura total

#### 🔧 **Controles Compactos**
- Edição em lote reorganizada em layout vertical
- Botões menores com fontes ajustadas
- Campos de entrada mais compactos
- Preview de mapeamentos otimizado

### Vantagens da Nova Interface

#### 🖥️ **Compatibilidade com Telas**
- ✅ Telas widescreen: Aproveitamento máximo do espaço
- ✅ Monitores 1920x1080: Interface completa visível
- ✅ Barra de tarefas: Não interfere na visualização
- ✅ Resoluções menores: Interface adaptável

#### 📊 **Melhor Visualização de Dados**
- Tabela com mais espaço horizontal para colunas
- Filtros sempre visíveis junto com os dados
- Controles organizados sem sobreposição
- Scroll inteligente apenas onde necessário

#### ⚡ **Eficiência de Uso**
- Navegação mais fluida entre elementos
- Menos necessidade de scroll vertical
- Divisor ajustável para preferências do usuário
- Interface mais profissional e moderna

### Funcionalidades Preservadas

Todas as funcionalidades existentes foram mantidas:
- ✅ Edição direta na tabela (duplo clique)
- ✅ Filtros de busca por nosso número e código empresa
- ✅ Edição em lote para múltiplos registros
- ✅ Importação de planilha com mapeamentos
- ✅ Validações automáticas
- ✅ Destaque visual das alterações
- ✅ Botão "Gerar CNAB sem Juros"
- ✅ Salvamento de alterações

### Detalhes Técnicos

#### Estrutura do Layout
```
┌─────────────────────────────────────────────────────────┐
│                    CABEÇALHO                            │
├──────────────────────────┬──────────────────────────────┤
│     PAINEL ESQUERDO      │     PAINEL DIREITO           │
│                          │                              │
│  ┌─────────────────────┐ │  ┌─────────────────────────┐ │
│  │     FILTROS         │ │  │   EDIÇÃO EM LOTE        │ │
│  └─────────────────────┘ │  └─────────────────────────┘ │
│                          │                              │
│  ┌─────────────────────┐ │  ┌─────────────────────────┐ │
│  │                     │ │  │ IMPORTAÇÃO PLANILHA     │ │
│  │      TABELA         │ │  └─────────────────────────┘ │
│  │                     │ │                              │
│  │                     │ │        (SCROLL AREA)         │
│  └─────────────────────┘ │                              │
├──────────────────────────┴──────────────────────────────┤
│                    BOTÕES DE AÇÃO                       │
└─────────────────────────────────────────────────────────┘
```

#### Implementação
- **QSplitter**: Divisor horizontal redimensionável
- **QScrollArea**: Scroll automático no painel direito
- **Layouts compactos**: Espaçamento e margens otimizados
- **Fontes reduzidas**: Melhor aproveitamento do espaço

### Compatibilidade

#### Resoluções Testadas
- ✅ 1920x1080 (Full HD) - Ideal
- ✅ 1600x900 (HD+) - Muito boa
- ✅ 1366x768 (HD) - Adequada
- ✅ 1280x720 (HD Ready) - Mínima aceitável

#### Sistemas Operacionais
- ✅ Windows 10/11 com barra de tarefas
- ✅ Diferentes escalas de DPI
- ✅ Múltiplos monitores

### Scripts de Teste
```bash
cd "scripts python"
# Demonstração da nova interface horizontal
python teste_editor_horizontal.py
```

### Próximas Funcionalidades Planejadas
- **Editor Gráfico Completo**: Edição de todos os campos via interface visual
- **Validação Avançada**: Regras de negócio específicas do Bradesco
- **Relatórios Personalizados**: Dashboards e análises automáticas
- **API REST**: Interface programática para integração
- **Processamento em Lote**: Múltiplos arquivos simultaneamente

---

*Funcionalidade implementada em dezembro de 2024*  
*Documentação atualizada em: Dezembro 2024*

## 🛡️ NOVA TECNOLOGIA: Edição Segura de Arquivos CNAB

### Descrição
**🆕 IMPLEMENTAÇÃO REVOLUCIONÁRIA** - Nova abordagem de edição que funciona como um **"editor de texto"**, preservando 100% da integridade do arquivo original e eliminando completamente o risco de perda de caracteres.

### 🔍 Problema Identificado e Solucionado
**❌ Abordagem Anterior (Reconstrução Completa)**
- Risco de perda de caracteres durante reconstrução
- Problemas de codificação e formatação
- Alteração não intencional de campos
- Possível corrupção de dados estruturais

**✅ Nova Abordagem (Edição Pontual)**
- Preservação total da estrutura original
- Edição apenas dos campos específicos necessários
- Manutenção de codificação e formatação originais
- Zero risco de perda de dados

### 🔧 Metodologia Técnica

#### 1. Leitura Preservativa
```python
# Lê arquivo original mantendo codificação e estrutura
with open(arquivo, 'r', encoding='utf-8', newline='') as f:
    linhas_originais = f.readlines()
```

#### 2. Identificação Precisa
```python
# Identifica linhas de detalhe sem alterar outras
if linha.strip() and linha[0] == '1':  # Linha de detalhe
    # Aplica edições pontuais apenas aqui
```

#### 3. Edição Pontual
```python
# Altera apenas posições específicas dos campos editados
linha = linha[:70] + novo_nosso_numero + linha[82:]  # NOSSO_NUMERO
linha = linha[:266] + '0000000000000' + linha[279:]  # Zerar juros
```

#### 4. Salvamento Preservativo
```python
# Salva mantendo estrutura original
with open(arquivo_saida, 'w', encoding='utf-8', newline='') as f:
    f.writelines(linhas_editadas)
```

### 🎯 Campos com Edição Segura Implementada

| Campo | Posições CNAB | Tamanho | Formato | Método |
|-------|---------------|---------|---------|--------|
| **NOSSO_NUMERO** | 70-82 | 12 chars | Zero-padded | `_aplicar_edicoes_pontuais()` |
| **CODIGO_EMPRESA** | 20-37 | 17 chars | Space-padded | `_aplicar_edicoes_pontuais()` |
| **JUROS/MULTA** | 266-279 | 13 chars | Zero-filled | `_zerar_juros_pontual()` |

### 🔄 Métodos Seguros Implementados

#### 1. `_editar_cnab_seguro()`
**Método principal de edição segura**
- Combina edições pontuais com zeramento de juros
- Preserva estrutura original do arquivo
- Conta alterações realizadas
- Valida integridade do resultado

#### 2. `_aplicar_edicoes_pontuais()`
**Edição específica de campos alterados**
- Identifica campos marcados como alterados
- Edita apenas posições exatas necessárias
- Ajusta tamanho com padding correto
- Mantém resto da linha inalterado

#### 3. `_zerar_juros_pontual()`
**Zeramento seguro de juros/multa**
- Altera apenas posições 266-279
- Não afeta outros valores monetários
- Preserva todos os outros campos
- Mantém quebras de linha originais

#### 4. `_zerar_juros_arquivo_completo()`
**Processamento completo de arquivo**
- Processa todas as linhas de detalhe
- Aplica zeramento pontual em cada linha
- Preserva header e trailer intactos
- Conta registros processados

### 🛡️ Funcionalidades Atualizadas com Edição Segura

#### 1. **Salvar Alterações** (Editor Gráfico)
```python
# Agora usa método seguro
def salvar_alteracoes(self):
    sucesso, msg = self.cnab.gerar_cnab_editado(caminho)
    # Internamente chama _editar_cnab_seguro(zerar_juros=False)
```

#### 2. **Gerar CNAB sem Juros** (Editor Gráfico)
```python
# Combina edições + zeramento com segurança total
def gerar_cnab_sem_juros(self):
    sucesso, msg = self.cnab.gerar_cnab_editado_sem_juros(caminho)
    # Internamente chama _editar_cnab_seguro(zerar_juros=True)
```

#### 3. **Gerar CNAB Retorno** (Tela Principal)
```python
# Zera juros de forma pontual em todo arquivo
def gerar_cnab_retorno(self):
    return self._zerar_juros_arquivo_completo(caminho)
```

### 📊 Exemplo Prático de Edição Segura

#### Antes da Edição:
```
1...NOSSO123456...EMPRESA123...outros_dados_preservados...JUROS123...
```

#### Após Edição Segura:
```
1...NOVO654321...NOVAEMPRESA...outros_dados_preservados...000000000...
```

#### Análise das Alterações:
- ✅ **Posições 70-82**: NOSSO_NUMERO alterado para novo valor
- ✅ **Posições 20-37**: CODIGO_EMPRESA alterado para novo valor  
- ✅ **Posições 266-279**: Juros zerados conforme solicitado
- ✅ **Todas as outras posições**: Mantidas exatamente iguais
- ✅ **Estrutura da linha**: Preservada completamente

### 🔍 Validações e Verificações

#### Validações Automáticas
- **Tamanho da linha**: Garante mínimo de 400 caracteres
- **Padding correto**: Aplica zero-padding ou space-padding conforme campo
- **Quebras de linha**: Preserva formatação original
- **Codificação**: Mantém encoding original do arquivo

#### Verificações Recomendadas
- **Tamanho do arquivo**: Deve ser idêntico ao original
- **Campos não editados**: Devem permanecer iguais
- **Header e trailer**: Completamente preservados
- **Estrutura geral**: Mantida sem alterações

### 💡 Comparação Técnica

#### 🔴 Método Anterior (Reconstrução)
```
Arquivo Original → Parsing → Reconstrução → Arquivo Novo
     ↓               ↓           ↓            ↓
  Preservado    Interpretação  Rebuild    Risco de perda
```

#### 🟢 Método Atual (Edição Pontual)
```
Arquivo Original → Identificação → Edição Pontual → Arquivo Novo
     ↓                 ↓               ↓              ↓
  Preservado      Posições exatas  Apenas necessário  Integridade 100%
```

### 🚀 Vantagens da Edição Segura

- ✅ **Zero Perda de Dados**: Nenhum caractere é perdido ou alterado indevidamente
- ✅ **Preservação Total**: Estrutura, codificação e formatação mantidas
- ✅ **Compatibilidade Garantida**: Arquivo 100% válido para processamento bancário
- ✅ **Processo Confiável**: Elimina riscos de corrupção de dados
- ✅ **Eficiência Máxima**: Edita apenas o estritamente necessário
- ✅ **Validação Integrada**: Verifica automaticamente a integridade do resultado
- ✅ **Backup Implícito**: Arquivo original sempre preservado
- ✅ **Rastreabilidade**: Conta e reporta exatamente o que foi alterado

### 🎯 Casos de Uso da Edição Segura

#### 1. **Correções Pontuais**
- Alterar nosso número ou código da empresa
- Manter todos os outros dados intactos
- Garantir que nada mais seja afetado

#### 2. **Zeramento de Juros**
- Remover apenas juros e multas
- Preservar valores principais e outros campos
- Manter estrutura completa do arquivo

#### 3. **Edições Combinadas**
- Aplicar correções + zerar juros simultaneamente
- Processo unificado e seguro
- Uma operação para múltiplas necessidades

#### 4. **Processamento em Lote**
- Aplicar mesmas edições em múltiplos arquivos
- Manter consistência e segurança
- Processo escalável e confiável

### 📝 Script de Demonstração

Execute o script para ver a edição segura em ação:
```bash
cd "scripts python"
python teste_edicao_segura.py
```

### 🔧 Implementação Técnica Detalhada

#### Estrutura dos Métodos Seguros
```python
def _editar_cnab_seguro(self, caminho_saida, zerar_juros=False):
    """Método principal - coordena todo o processo"""
    
def _aplicar_edicoes_pontuais(self, linha, detalhe):
    """Edita campos específicos nas posições exatas"""
    
def _zerar_juros_pontual(self, linha):
    """Zera juros mantendo resto da linha intacto"""
```

#### Fluxo de Processamento
1. **Leitura**: Arquivo lido linha por linha preservando tudo
2. **Identificação**: Localiza apenas linhas de detalhe (tipo 1)
3. **Edição**: Aplica alterações pontuais conforme necessário
4. **Validação**: Verifica integridade de cada linha editada
5. **Salvamento**: Escreve arquivo mantendo estrutura original

### 🎉 Resultado Final

A implementação da **Edição Segura** resolve definitivamente:
- ❌ Perda de caracteres → ✅ Preservação total
- ❌ Problemas de codificação → ✅ Encoding mantido
- ❌ Alterações indesejadas → ✅ Edição apenas do necessário
- ❌ Risco de corrupção → ✅ Integridade garantida
- ❌ Incompatibilidade bancária → ✅ Formato 100% válido

**A nova abordagem oferece confiabilidade total para processamento de arquivos CNAB críticos!**