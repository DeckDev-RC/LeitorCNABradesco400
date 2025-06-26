# 🔒 Política de Segurança

## 🛡️ Versões Suportadas

Mantemos suporte de segurança para as seguintes versões:

| Versão | Suporte de Segurança |
| ------- | -------------------- |
| 1.2.x   | ✅ Suportada        |
| 1.1.x   | ✅ Suportada        |
| 1.0.x   | ⚠️ Suporte limitado  |
| < 1.0   | ❌ Não suportada    |

## 🚨 Relatando Vulnerabilidades

### Como Reportar
Se você descobrir uma vulnerabilidade de segurança, por favor:

1. **NÃO** abra uma issue pública
2. Envie um email para: `seguranca@exemplo.com`
3. Inclua detalhes completos da vulnerabilidade
4. Aguarde nossa resposta em até 48 horas

### Informações Necessárias
- Descrição detalhada da vulnerabilidade
- Passos para reproduzir o problema
- Versão afetada do software
- Impacto potencial da vulnerabilidade
- Sugestões de correção (se houver)

### Processo de Resposta
1. **Confirmação** - Resposta inicial em 48 horas
2. **Avaliação** - Análise completa em até 7 dias
3. **Correção** - Desenvolvimento da correção
4. **Teste** - Validação da correção
5. **Lançamento** - Publicação da versão corrigida
6. **Divulgação** - Comunicação pública após correção

## 🔐 Práticas de Segurança

### Para Usuários
- Mantenha sempre a versão mais recente instalada
- Não compartilhe arquivos CNAB com dados reais publicamente
- Use ambientes virtuais Python isolados
- Valide sempre a origem dos arquivos CNAB

### Para Desenvolvedores
- Nunca commite dados sensíveis (CNPJs, nomes reais, etc.)
- Use `.gitignore` para arquivos de dados
- Valide todas as entradas de usuário
- Mantenha dependências atualizadas

## 📊 Dados Sensíveis

### Tipos de Dados Protegidos
- CNPJs de empresas reais
- Nomes de empresas reais
- Valores monetários reais
- Números de documentos reais
- Informações bancárias reais

### Medidas de Proteção
- Anonimização automática em exemplos
- `.gitignore` configurado para arquivos sensíveis
- Documentação sobre manuseio seguro de dados
- Templates com dados fictícios

## 🔄 Atualizações de Segurança

### Notificações
- Vulnerabilidades críticas: Notificação imediata
- Vulnerabilidades altas: Notificação em 24 horas
- Vulnerabilidades médias: Incluídas em releases regulares

### Canais de Comunicação
- GitHub Security Advisories
- Release Notes no CHANGELOG.md
- Documentação atualizada

## 🏆 Reconhecimentos

Agradecemos a todos que contribuem para a segurança do projeto:
- Pesquisadores de segurança responsáveis
- Usuários que reportam problemas
- Desenvolvedores que implementam correções

## 📞 Contato

Para questões de segurança:
- Email: `seguranca@exemplo.com`
- PGP Key: [Disponível mediante solicitação]

Para outras questões:
- GitHub Issues: [Issues do Projeto](https://github.com/seu-usuario/cnab-bradesco/issues)
- Discussões: [GitHub Discussions](https://github.com/seu-usuario/cnab-bradesco/discussions) 