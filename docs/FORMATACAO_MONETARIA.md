# Formatação Monetária Brasileira

## Implementação de Formatação de Valores em Padrão Brasileiro

O sistema foi atualizado para exibir valores monetários no formato brasileiro padrão: `R$ 1.234,56` (com separador de milhar por ponto e separador decimal por vírgula).

## Exemplos de Formatação

| Valor | Formato Internacional | Formato Brasileiro |
|-------|------------------------|-------------------|
| 1000 | R$ 1,000.00 | R$ 1.000,00 |
| 1234.56 | R$ 1,234.56 | R$ 1.234,56 |
| 1000000 | R$ 1,000,000.00 | R$ 1.000.000,00 |

## Implementação

A formatação monetária brasileira foi implementada através de uma função auxiliar em cada um dos principais módulos do sistema:

```python
def formatar_moeda(valor):
    """Formata um valor para o padrão monetário brasileiro"""
    return f"R$ {valor:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
```

Esta função realiza os seguintes passos:
1. Formata o valor com separador de milhar e duas casas decimais
2. Substitui temporariamente a vírgula por um underline
3. Substitui o ponto por vírgula
4. Substitui o underline por ponto

## Locais de Aplicação

A formatação monetária foi aplicada consistentemente em todo o sistema:

1. **Interface Gráfica**:
   - Tabela de detalhes dos títulos
   - Resumo de valores
   - Mensagens informativas

2. **Linha de Comando**:
   - Saída do relatório de processamento
   - Totais e subtotais

3. **Processamento em Lote**:
   - Resumo de processamento
   - Totais exibidos no terminal

## Observações Importantes

- Os arquivos CSV exportados mantêm os valores numéricos originais (sem formatação) para garantir compatibilidade com outros sistemas
- A formatação monetária é aplicada apenas na interface visual e relatórios exibidos
- Os cálculos são realizados sempre com os valores numéricos originais para garantir precisão

## Configuração Regional

O sistema tenta configurar o locale para português brasileiro, mas caso não seja possível, utiliza a função personalizada de formatação monetária.

```python
try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil.1252')
    except locale.Error:
        pass  # Se falhar, usaremos nossa própria função de formatação
``` 