# Tratamento de Arquivos CNAB sem Sequencial

## Descrição do Problema

Alguns arquivos CNAB 400 do Bradesco podem vir sem o campo sequencial (posição 395-400) ou com o tamanho da linha menor que o padrão de 400 caracteres. Isso pode acontecer devido a:

1. Diferentes versões do layout CNAB implementadas pelo banco
2. Sistemas legados que geram os arquivos com formato ligeiramente diferente
3. Truncamento de linhas durante a transmissão ou processamento
4. Omissão proposital de campos considerados opcionais

## Solução Implementada

O sistema foi adaptado para lidar com essas variações, garantindo que os arquivos CNAB possam ser processados corretamente mesmo quando não seguem rigorosamente o padrão de 400 caracteres ou não possuem o campo sequencial.

### Principais Melhorias

1. **Verificação de Tamanho de Linha**
   - Antes de tentar acessar qualquer posição, o sistema verifica se a linha tem o tamanho necessário
   - Para cada campo, é feita uma verificação de segurança: `linha[x:y] if len(linha) >= y else ""`

2. **Tratamento de Valores Monetários**
   - Conversão segura de valores monetários com tratamento de exceções
   - Valor padrão (0.0) para campos que não existem ou contêm dados inválidos

3. **Geração de CNAB de Retorno**
   - A atualização do sequencial só é realizada se a linha tiver o tamanho adequado
   - Preservação da estrutura original da linha, mesmo que incompleta

4. **Formatação Monetária Robusta**
   - Tratamento de exceções ao formatar valores monetários
   - Valor padrão ("R$ 0,00") para campos inválidos

5. **Limpeza de Linhas**
   - Remoção de quebras de linha e espaços extras
   - Verificação de linhas vazias antes do processamento

## Como Funciona

### Leitura de Campos com Verificação de Tamanho

```python
# Exemplo de leitura segura de campos
data_credito = linha[295:301] if len(linha) >= 301 else ""
sequencial = linha[394:400] if len(linha) >= 400 else ""
```

### Conversão Segura de Valores

```python
# Exemplo de conversão segura de valores monetários
try:
    valor_titulo = float(linha[152:165]) / 100 if len(linha) >= 165 else 0.0
except ValueError:
    valor_titulo = 0.0
```

### Geração de CNAB de Retorno

```python
# Verificação de tamanho antes de modificar o sequencial
if len(linha) >= 400:
    # Atualizar o sequencial se necessário
    if contador_sequencial <= 999999:
        sequencial = f"{contador_sequencial:06d}"
        linha_modificada = linha_modificada[:394] + sequencial
```

## Limitações

1. **Identificação de Registros**
   - O sistema ainda depende dos códigos de registro (0, 1, 9) nas posições iniciais
   - Linhas sem o tipo de registro não podem ser processadas

2. **Campos Obrigatórios**
   - Alguns campos são essenciais para o processamento (tipo_registro, valor_titulo)
   - Arquivos muito truncados podem não ser processados corretamente

3. **Consistência de Dados**
   - Valores zerados podem ser inseridos para campos ausentes
   - Isso pode afetar totalizações ou análises posteriores

## Recomendações

1. **Validação de Arquivos**
   - Sempre validar os arquivos CNAB gerados antes de enviá-los ao banco
   - Verificar se os campos essenciais estão presentes e corretos

2. **Tratamento de Casos Específicos**
   - Alguns casos podem exigir tratamentos adicionais não cobertos pela solução atual
   - Documentar variações específicas de layout encontradas

3. **Monitoramento**
   - Manter um registro de arquivos processados com formato não padrão
   - Avaliar regularmente se ajustes adicionais são necessários 