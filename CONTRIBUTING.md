# 🤝 Guia de Contribuição

Obrigado pelo interesse em contribuir com o Sistema de Processamento CNAB 400 - Bradesco! Este documento fornece diretrizes para contribuições.

## 📋 Como Contribuir

### 🐛 Reportando Bugs
1. Verifique se o bug já foi reportado nas [Issues](https://github.com/seu-usuario/cnab-bradesco/issues)
2. Crie uma nova issue com:
   - Descrição clara do problema
   - Passos para reproduzir
   - Comportamento esperado vs atual
   - Versão do sistema e Python
   - Screenshots (se aplicável)

### 💡 Sugerindo Funcionalidades
1. Verifique se a funcionalidade já foi sugerida
2. Abra uma issue com o template de feature request
3. Descreva claramente o problema que a funcionalidade resolve
4. Forneça exemplos de uso

### 🔧 Contribuindo com Código

#### Configuração do Ambiente
```bash
# Fork e clone o repositório
git clone https://github.com/seu-usuario/cnab-bradesco.git
cd cnab-bradesco

# Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instale dependências de desenvolvimento
pip install -e .[dev]
```

#### Fluxo de Desenvolvimento
1. **Fork** o repositório
2. **Clone** seu fork localmente
3. **Crie** uma branch para sua feature/correção:
   ```bash
   git checkout -b feature/nova-funcionalidade
   # ou
   git checkout -b fix/correcao-bug
   ```
4. **Desenvolva** e teste suas mudanças
5. **Commit** seguindo o padrão de commits
6. **Push** para seu fork
7. **Abra** um Pull Request

## 📝 Padrões de Código

### Estilo de Código
- Use **Python 3.8+**
- Siga **PEP 8** para formatação
- Use **type hints** quando possível
- Documente funções com **docstrings**

### Exemplo de Código
```python
def processar_arquivo_cnab(caminho: str) -> tuple[bool, str]:
    """
    Processa um arquivo CNAB e retorna o resultado.
    
    Args:
        caminho: Caminho para o arquivo CNAB
        
    Returns:
        Tupla com (sucesso, mensagem)
        
    Raises:
        FileNotFoundError: Se o arquivo não existir
    """
    try:
        # Implementação aqui
        return True, "Arquivo processado com sucesso"
    except Exception as e:
        return False, f"Erro: {str(e)}"
```

### Padrão de Commits
Use o formato: `tipo: [descrição]`

**Tipos:**
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Alterações na documentação
- `style`: Formatação (sem mudança de lógica)
- `refactor`: Refatoração de código
- `test`: Adição/modificação de testes
- `chore`: Tarefas de manutenção

**Exemplos:**
```
feat: [adiciona] validação de CNPJ no processamento
fix: [corrige] erro de encoding em arquivos especiais
docs: [atualiza] guia de instalação no README
```

## 🧪 Testes

### Executando Testes
```bash
# Executar todos os testes
pytest

# Executar com cobertura
pytest --cov=cnab_bradesco

# Executar testes específicos
pytest tests/test_processamento.py
```

### Criando Testes
- Crie testes para novas funcionalidades
- Use dados fictícios (nunca dados reais)
- Teste casos normais e casos extremos
- Mantenha cobertura acima de 80%

## 📊 Dados e Segurança

### ⚠️ IMPORTANTE: Dados Sensíveis
- **NUNCA** commite dados reais (CNPJs, nomes de empresas, etc.)
- Use sempre dados fictícios em testes e exemplos
- Execute `python scripts/cleanup_sensitive_data.py` antes de commits

### Dados para Testes
```python
# ✅ BOM - Dados fictícios
cnpj_teste = "12345678000123"
empresa_teste = "EMPRESA EXEMPLO LTDA"

# ❌ RUIM - Dados reais
cnpj_real = "50670573000109"  # Não faça isso!
```

## 📖 Documentação

### Atualizando Documentação
- Mantenha o README.md atualizado
- Documente novas funcionalidades em `docs/`
- Atualize o CHANGELOG.md
- Use Markdown com emojis para clareza

### Estrutura da Documentação
```
docs/
├── README.md                    # Índice da documentação
├── NOVAS_FUNCIONALIDADES.md    # Funcionalidades detalhadas
├── FORMATACAO_MONETARIA.md     # Formatação específica
└── SPEC.md                     # Especificações técnicas
```

## 🔄 Pull Requests

### Checklist antes do PR
- [ ] Código segue os padrões estabelecidos
- [ ] Testes passam (`pytest`)
- [ ] Documentação atualizada
- [ ] CHANGELOG.md atualizado
- [ ] Sem dados sensíveis
- [ ] Commit messages seguem o padrão

### Template de PR
```markdown
## Descrição
Breve descrição das mudanças

## Tipo de Mudança
- [ ] Bug fix
- [ ] Nova funcionalidade
- [ ] Breaking change
- [ ] Documentação

## Como Testar
1. Passos para testar
2. Dados de exemplo
3. Resultado esperado

## Screenshots (se aplicável)
```

## 🏆 Reconhecimento

Contribuidores são reconhecidos:
- No arquivo AUTHORS.md
- Nas release notes
- Na documentação do projeto

## 📞 Suporte

Precisa de ajuda?
- 💬 [GitHub Discussions](https://github.com/seu-usuario/cnab-bradesco/discussions)
- 📧 Email: `contato@exemplo.com`
- 📋 [Issues](https://github.com/seu-usuario/cnab-bradesco/issues)

## 📜 Código de Conduta

Este projeto segue o [Código de Conduta do Contributor Covenant](https://www.contributor-covenant.org/). Ao participar, você concorda em manter um ambiente respeitoso e inclusivo.

---

**Obrigado por contribuir! 🎉** 