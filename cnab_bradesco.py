import pandas as pd
from tabulate import tabulate
import os
import re
from datetime import datetime
import locale

class CNABBradesco:
    def __init__(self, arquivo):
        self.arquivo = arquivo
        self.header = None
        self.detalhes = []
        self.trailer = None
        self.linhas_originais = []
        
    def ler_arquivo(self):
        """Lê o arquivo CNAB 400 do Bradesco"""
        try:
            with open(self.arquivo, 'r', encoding='utf-8') as file:
                self.linhas_originais = file.readlines()
                
            if not self.linhas_originais:
                print("Arquivo vazio.")
                return False
                
            # Processa o header (registro tipo 0)
            for linha in self.linhas_originais:
                # Remover quebras de linha e garantir que a linha tenha pelo menos 1 caractere
                linha = linha.strip()
                if not linha:
                    continue
                    
                if linha.startswith('0'):
                    self.header = self._processar_header(linha)
                elif linha.startswith('1'):
                    self.detalhes.append(self._processar_detalhe(linha))
                elif linha.startswith('9'):
                    self.trailer = self._processar_trailer(linha)
                    
            return True
        except Exception as e:
            print(f"Erro ao ler o arquivo: {str(e)}")
            return False
            
    def _processar_header(self, linha):
        """Processa a linha de header (tipo 0)"""
        # Garantir que a linha seja tratada mesmo se não tiver o tamanho padrão
        sequencial = linha[394:400] if len(linha) >= 400 else ""
        data_credito = linha[379:385] if len(linha) >= 385 else ""
        
        return {
            'tipo_registro': linha[0:1],
            'codigo_retorno': linha[1:2],
            'literal_retorno': linha[2:9],
            'codigo_servico': linha[9:11],
            'literal_servico': linha[11:26],
            'codigo_empresa': linha[26:46],
            'nome_empresa': linha[46:76],
            'codigo_banco': linha[76:79],
            'nome_banco': linha[79:94],
            'data_geracao': linha[94:100],
            'densidade': linha[100:108] if len(linha) >= 108 else "",
            'numero_aviso_bancario': linha[108:113] if len(linha) >= 113 else "",
            'data_credito': data_credito,
            'sequencial': sequencial,
            'linha_original': linha
        }
        
    def _processar_detalhe(self, linha):
        """Processa as linhas de detalhe (tipo 1)"""
        # Verificar se a linha tem tamanho suficiente para cada campo
        # Para campos obrigatórios, usar um valor padrão se não existir
        
        data_ocorrencia = linha[110:116] if len(linha) >= 116 else ""
        data_vencimento = linha[146:152] if len(linha) >= 152 else ""
        data_credito = linha[295:301] if len(linha) >= 301 else ""
        sequencial = linha[394:400] if len(linha) >= 400 else ""
        
        # Calcular o valor do título de forma segura
        if len(linha) >= 165:
            try:
                valor_titulo = float(linha[152:165]) / 100
            except ValueError:
                valor_titulo = 0.0
        else:
            valor_titulo = 0.0
        
        # Valores adicionais de forma segura
        valor_tarifa = float(linha[175:188]) / 100 if len(linha) >= 188 else 0.0
        valor_iof = float(linha[188:201]) / 100 if len(linha) >= 201 else 0.0
        valor_abatimento = float(linha[227:240]) / 100 if len(linha) >= 240 else 0.0
        descontos = float(linha[240:253]) / 100 if len(linha) >= 253 else 0.0
        outros_creditos = float(linha[279:292]) / 100 if len(linha) >= 292 else 0.0
        
        return {
            'tipo_registro': linha[0:1],
            'codigo_inscricao': linha[1:3] if len(linha) >= 3 else "",
            'numero_inscricao': linha[3:17] if len(linha) >= 17 else "",
            'codigo_empresa': linha[20:37] if len(linha) >= 37 else "",
            'nosso_numero': linha[70:82] if len(linha) >= 82 else "",
            'carteira': linha[107:109] if len(linha) >= 109 else "",
            'data_ocorrencia': self._formatar_data(data_ocorrencia) if data_ocorrencia.strip() else "",
            'seu_numero': linha[116:126] if len(linha) >= 126 else "",
            'data_vencimento': self._formatar_data(data_vencimento) if data_vencimento.strip() else "",
            'valor_titulo': valor_titulo,
            'banco_cobrador': linha[165:168] if len(linha) >= 168 else "",
            'agencia_cobradora': linha[168:173] if len(linha) >= 173 else "",
            'especie': linha[173:175] if len(linha) >= 175 else "",
            'valor_tarifa': valor_tarifa,
            'valor_iof': valor_iof,
            'valor_abatimento': valor_abatimento,
            'descontos': descontos,
            'valor_principal': valor_titulo,  # Usando o mesmo valor do título
            'juros_mora_multa': 0.0,  # Juros zerados conforme solicitado
            'outros_creditos': outros_creditos,
            'data_credito': self._formatar_data(data_credito) if data_credito.strip() else "",
            'motivo_ocorrencia': linha[318:328] if len(linha) >= 328 else "",
            'sequencial': sequencial,
            'linha_original': linha
        }
        
    def _processar_trailer(self, linha):
        """Processa a linha de trailer (tipo 9)"""
        # Valores tratados de forma segura
        sequencial = linha[394:400] if len(linha) >= 400 else ""
        
        # Verificar se os campos numéricos existem
        try:
            valor_total_simples = float(linha[25:39]) / 100 if len(linha) >= 39 else 0.0
        except ValueError:
            valor_total_simples = 0.0
            
        try:
            valor_total_vinculado = float(linha[47:61]) / 100 if len(linha) >= 61 else 0.0
        except ValueError:
            valor_total_vinculado = 0.0
            
        try:
            valor_total_caucao = float(linha[69:83]) / 100 if len(linha) >= 83 else 0.0
        except ValueError:
            valor_total_caucao = 0.0
            
        try:
            valor_total_descontado = float(linha[91:105]) / 100 if len(linha) >= 105 else 0.0
        except ValueError:
            valor_total_descontado = 0.0
        
        return {
            'tipo_registro': linha[0:1],
            'retorno': linha[1:2] if len(linha) >= 2 else "",
            'tipo_registro_1': linha[2:4] if len(linha) >= 4 else "",
            'qtd_titulos_simples': linha[17:25] if len(linha) >= 25 else "0",
            'valor_total_simples': valor_total_simples,
            'qtd_titulos_vinculado': linha[39:47] if len(linha) >= 47 else "0",
            'valor_total_vinculado': valor_total_vinculado,
            'qtd_titulos_caucao': linha[61:69] if len(linha) >= 69 else "0",
            'valor_total_caucao': valor_total_caucao,
            'qtd_titulos_descontado': linha[83:91] if len(linha) >= 91 else "0",
            'valor_total_descontado': valor_total_descontado,
            'sequencial': sequencial,
            'linha_original': linha
        }

    def _formatar_data(self, data_str):
        """Converte a data do formato DDMMAA para DD/MM/AAAA"""
        if not data_str or data_str.strip() == '':
            return ""
        try:
            data = datetime.strptime(data_str, '%d%m%y')
            return data.strftime('%d/%m/%Y')
        except ValueError:
            return data_str
            
    def formatar_moeda(self, valor):
        """Formata um valor para o padrão monetário brasileiro"""
        try:
            return f"R$ {valor:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
        except (ValueError, TypeError):
            return "R$ 0,00"
        
    def gerar_cnab_retorno(self, caminho_saida):
        """Gera um novo arquivo CNAB sem juros/multa para retorno ao banco (método seguro)"""
        try:
            # Usar método seguro que apenas zera juros sem alterar resto do arquivo
            return self._zerar_juros_arquivo_completo(caminho_saida)
        except Exception as e:
            return False, f"Erro ao gerar arquivo CNAB: {str(e)}"

    def _zerar_juros_arquivo_completo(self, caminho_saida):
        """
        Zera juros/multa em todo o arquivo de forma segura, como um editor de texto.
        Altera apenas as posições 266-279 de cada linha de detalhe.
        """
        try:
            # Ler o arquivo original como texto, preservando encoding
            with open(self.arquivo, 'r', encoding='utf-8', newline='') as arquivo_original:
                linhas_originais = arquivo_original.readlines()
            
            # Criar lista de linhas editadas
            linhas_editadas = []
            linhas_processadas = 0
            
            for linha in linhas_originais:
                linha_editada = linha
                
                # Verificar se é uma linha de detalhe (tipo 1) e zerar juros
                if linha.strip() and linha[0] == '1':
                    linha_editada = self._zerar_juros_pontual(linha)
                    linhas_processadas += 1
                
                linhas_editadas.append(linha_editada)
            
            # Salvar arquivo editado preservando formato original
            with open(caminho_saida, 'w', encoding='utf-8', newline='') as arquivo_saida:
                arquivo_saida.writelines(linhas_editadas)
            
            return True, f"Arquivo CNAB gerado com sucesso: {caminho_saida}\nJuros/multa zerados em {linhas_processadas} registro(s)"
            
        except Exception as e:
            return False, f"Erro ao gerar arquivo CNAB: {str(e)}"

    def exportar_para_excel(self, caminho_saida):
        """Exporta os dados para um arquivo Excel"""
        try:
            # Criar DataFrame com os detalhes
            df = pd.DataFrame(self.detalhes)
            
            # Remover colunas que não precisam ser exportadas
            if 'linha_original' in df.columns:
                df = df.drop('linha_original', axis=1)
            
            # Definir o escritor Excel
            writer = pd.ExcelWriter(caminho_saida, engine='openpyxl')
            
            # Salvar a planilha principal
            df.to_excel(writer, sheet_name='Detalhes', index=False)
            
            # Criar uma planilha de resumo
            resumo_data = {
                'Informação': [
                    'Banco',
                    'Empresa',
                    'Data de Geração',
                    'Data de Crédito',
                    'Total de Títulos',
                    'Valor Total'
                ],
                'Valor': [
                    f"{self.header['codigo_banco']} - {self.header['nome_banco']}",
                    self.header['nome_empresa'].strip(),
                    self._formatar_data(self.header['data_geracao']),
                    self._formatar_data(self.header['data_credito']) if self.header['data_credito'].strip() else "",
                    len(self.detalhes),
                    self.formatar_moeda(sum(detalhe['valor_principal'] for detalhe in self.detalhes))
                ]
            }
            
            df_resumo = pd.DataFrame(resumo_data)
            df_resumo.to_excel(writer, sheet_name='Resumo', index=False)
            
            # Salvar o arquivo
            writer.close()
            
            return True, f"Dados exportados para Excel: {caminho_saida}"
        except Exception as e:
            return False, f"Erro ao exportar para Excel: {str(e)}"

    def gerar_relatorio(self):
        """Gera um relatório baseado nos dados processados"""
        if not self.header or not self.detalhes:
            print("Não há dados para gerar relatório. Execute ler_arquivo() primeiro.")
            return
            
        # Criar DataFrame com os detalhes
        df = pd.DataFrame(self.detalhes)
        
        # Informações do header
        print("\n===== INFORMAÇÕES DO ARQUIVO =====")
        print(f"Banco: {self.header['codigo_banco']} - {self.header['nome_banco']}")
        print(f"Empresa: {self.header['nome_empresa']}")
        print(f"Data de Geração: {self._formatar_data(self.header['data_geracao'])}")
        if self.header['data_credito'].strip():
            print(f"Data de Crédito: {self._formatar_data(self.header['data_credito'])}")
        
        # Resumo dos detalhes
        print("\n===== RESUMO DE TÍTULOS =====")
        print(f"Total de títulos: {len(self.detalhes)}")
        
        valor_total = sum(detalhe['valor_principal'] for detalhe in self.detalhes)
        print(f"Valor total dos títulos: {self.formatar_moeda(valor_total)}")
        
        # Detalhes dos títulos
        print("\n===== DETALHES DOS TÍTULOS =====")
        colunas_exibir = ['nosso_numero', 'seu_numero', 'data_ocorrencia', 
                         'data_vencimento', 'valor_titulo', 'valor_principal', 
                         'juros_mora_multa', 'data_credito']
                         
        if not df.empty:
            # Formatar colunas monetárias antes de exibir
            for col in ['valor_titulo', 'valor_principal', 'juros_mora_multa']:
                if col in df.columns:
                    df[col] = df[col].apply(lambda x: self.formatar_moeda(x) if pd.notnull(x) else "")
            
            df_exibir = df[colunas_exibir]
            print(tabulate(df_exibir, headers='keys', tablefmt='psql', showindex=False))
            
            # Salvar em CSV e Excel
            nome_arquivo = os.path.basename(self.arquivo)
            nome_base = re.sub(r'\.TXT$', '', nome_arquivo, flags=re.IGNORECASE)
            
            # Para o CSV, usamos os valores originais (não formatados)
            df_original = pd.DataFrame(self.detalhes)
            if 'linha_original' in df_original.columns:
                df_original = df_original.drop('linha_original', axis=1)
                
            df_original.to_csv(f"{nome_base}_processado.csv", index=False, sep=';')
            print(f"\nDados exportados para {nome_base}_processado.csv")
            
            # Exportar para Excel
            caminho_excel = f"{nome_base}_processado.xlsx"
            sucesso, mensagem = self.exportar_para_excel(caminho_excel)
            if sucesso:
                print(mensagem)
        
        # Informações do trailer
        if self.trailer:
            print("\n===== TOTAIS DO ARQUIVO =====")
            print(f"Quantidade de títulos simples: {int(self.trailer['qtd_titulos_simples'])}")
            print(f"Valor total simples: {self.formatar_moeda(self.trailer['valor_total_simples'])}")

    def _eh_linha_valida(self, linha, tipo_registro):
        """Verifica se a linha é válida para o tipo de registro especificado"""
        # Verificar se a linha tem pelo menos o tipo de registro
        if not linha or len(linha) < 1:
            return False
            
        # Verificar se o tipo de registro corresponde
        if linha[0] != tipo_registro:
            return False
            
        return True

    def _converter_moeda_para_centavos(self, valor_str):
        """Converte valor monetário string para centavos (inteiro)"""
        if valor_str is None or pd.isna(valor_str):
            return 0
        
        # Se já é um número (int ou float), converte diretamente
        if isinstance(valor_str, (int, float)):
            return int(valor_str * 100)
        
        # Converte para string se não for
        valor_str = str(valor_str)
        
        if not valor_str or valor_str.strip() == '':
            return 0
        
        try:
            # Remove símbolos monetários e espaços
            valor_limpo = valor_str.replace('R$', '').replace(' ', '').strip()
            
            # Se contém apenas dígitos, pontos e vírgulas
            if valor_limpo.replace('.', '').replace(',', '').replace('-', '').isdigit():
                # Trata diferentes formatos: 1.234,56 ou 1234.56
                if ',' in valor_limpo and '.' in valor_limpo:
                    # Formato brasileiro: 1.234,56
                    valor_limpo = valor_limpo.replace('.', '').replace(',', '.')
                elif ',' in valor_limpo and valor_limpo.count(',') == 1:
                    # Formato com vírgula decimal: 1234,56
                    valor_limpo = valor_limpo.replace(',', '.')
                
                valor_float = float(valor_limpo)
                return int(valor_float * 100)
            
            return 0
        except (ValueError, TypeError):
            return 0
    
    def _converter_data_para_ddmmaa(self, data_str):
        """Converte data DD/MM/YYYY para DDMMAA"""
        if data_str is None or pd.isna(data_str):
            return '000000'
        
        # Converte para string se não for
        data_str = str(data_str)
        
        if not data_str or data_str.strip() == '':
            return '000000'
        
        try:
            data_str = data_str.strip()
            
            # Formato DD/MM/YYYY
            if '/' in data_str and len(data_str) == 10:
                partes = data_str.split('/')
                if len(partes) == 3:
                    dia = partes[0].zfill(2)
                    mes = partes[1].zfill(2)
                    ano = partes[2][-2:]  # Pega os 2 últimos dígitos do ano
                    return f"{dia}{mes}{ano}"
            
            # Se já está no formato DDMMAA
            if len(data_str) == 6 and data_str.isdigit():
                return data_str
            
            return '000000'
        except (ValueError, TypeError, IndexError):
            return '000000'
    
    def _criar_header_padrao(self, nome_empresa="TC SECURITIZADORA S.A.", codigo_empresa="00000000000005725675"):
        """Cria um header padrão para arquivo CNAB 400"""
        linha = ' ' * 400  # Linha de 400 caracteres
        
        # Tipo de registro (posição 1)
        linha = '0' + linha[1:]
        
        # Código de retorno (posição 2)
        linha = linha[:1] + '2' + linha[2:]
        
        # Literal "RETORNO" (posições 3-9)
        linha = linha[:2] + 'RETORNO' + linha[9:]
        
        # Código de serviço (posições 10-11)
        linha = linha[:9] + '01' + linha[11:]
        
        # Literal "COBRANCA" (posições 12-19)
        linha = linha[:11] + 'COBRANCA' + linha[19:]
        
        # Código da empresa (posições 27-46)
        linha = linha[:26] + codigo_empresa.ljust(20)[:20] + linha[46:]
        
        # Nome da empresa (posições 47-76)
        linha = linha[:46] + nome_empresa.ljust(30)[:30] + linha[76:]
        
        # Código do banco (posições 77-79)
        linha = linha[:76] + '237' + linha[79:]
        
        # Nome do banco (posições 80-94)
        linha = linha[:79] + 'BRADESCO'.ljust(15) + linha[94:]
        
        # Data de geração (posições 95-100) - data atual
        data_atual = datetime.now().strftime('%d%m%y')
        linha = linha[:94] + data_atual + linha[100:]
        
        # Densidade (posição 101)
        linha = linha[:100] + '0' + linha[101:]
        
        # Unidade de densidade (posições 102-108)
        linha = linha[:101] + '1600000' + linha[108:]
        
        # Sequencial do header (posições 395-400)
        linha = linha[:394] + '000001'
        
        return linha + '\n'
    
    def _criar_trailer_padrao(self, qtd_registros, valor_total):
        """Cria um trailer padrão para arquivo CNAB 400"""
        linha = ' ' * 400  # Linha de 400 caracteres
        
        # Tipo de registro (posição 1)
        linha = '9' + linha[1:]
        
        # Código de retorno (posições 2-3)
        linha = linha[:1] + '01' + linha[3:]
        
        # Código do banco (posições 4-6)
        linha = linha[:3] + '237' + linha[6:]
        
        # Quantidade de títulos (posições 18-25)
        qtd_str = str(qtd_registros).zfill(8)
        linha = linha[:17] + qtd_str + linha[25:]
        
        # Valor total em centavos (posições 26-39)
        valor_centavos = int(valor_total * 100)
        valor_str = str(valor_centavos).zfill(14)
        linha = linha[:25] + valor_str + linha[39:]
        
        # Sequencial do trailer (posições 395-400)
        sequencial_trailer = str(qtd_registros + 2).zfill(6)  # +2 para header e trailer
        linha = linha[:394] + sequencial_trailer
        
        return linha + '\n'
    
    def excel_para_cnab(self, arquivo_excel, arquivo_cnab_saida, arquivo_cnab_referencia=None):
        """Converte arquivo Excel de volta para formato CNAB 400"""
        try:
            # Ler arquivo Excel
            df = pd.read_excel(arquivo_excel)
            
            if df.empty:
                return False, "Arquivo Excel está vazio"
            
            # Verificar colunas obrigatórias
            colunas_obrigatorias = ['nosso_numero', 'valor_titulo']
            for col in colunas_obrigatorias:
                if col not in df.columns:
                    return False, f"Coluna obrigatória '{col}' não encontrada no Excel"
            
            # Se arquivo de referência fornecido, usar header/trailer originais
            header_linha = None
            trailer_linha = None
            cnpj_empresa = '12345678000123'  # CNPJ exemplo
            codigo_empresa = '00000090368400035'
            
            if arquivo_cnab_referencia and os.path.exists(arquivo_cnab_referencia):
                try:
                    with open(arquivo_cnab_referencia, 'r', encoding='utf-8') as ref_file:
                        linhas_ref = ref_file.readlines()
                        if linhas_ref:
                            header_linha = linhas_ref[0]
                            if len(linhas_ref) > 1:
                                trailer_linha = linhas_ref[-1]
                            
                            # Extrair informações do header de referência
                            if len(linhas_ref) > 1:
                                primeira_linha_detalhe = linhas_ref[1]
                                if len(primeira_linha_detalhe) >= 37:
                                    cnpj_empresa = primeira_linha_detalhe[3:17]
                                    codigo_empresa = primeira_linha_detalhe[20:37]
                except Exception:
                    pass  # Se der erro, usa padrão
            
            # Criar arquivo CNAB
            with open(arquivo_cnab_saida, 'w', encoding='utf-8') as arquivo_saida:
                
                # Escrever header
                if header_linha:
                    arquivo_saida.write(header_linha)
                else:
                    header = self._criar_header_padrao()
                    arquivo_saida.write(header)
                
                # Processar cada linha do Excel
                valor_total = 0
                sequencial = 2  # Começa em 2 (header é 1)
                
                for index, row in df.iterrows():
                    # Criar linha CNAB de 400 caracteres preenchida com espaços
                    linha = ' ' * 400
                    
                    # Tipo de registro (posição 1)
                    tipo_registro = row.get('tipo_registro', '1')
                    linha = str(tipo_registro)[0] + linha[1:]
                    
                    # Código de inscrição (posições 2-3)
                    codigo_inscricao = row.get('codigo_inscricao', '02')
                    if pd.isna(codigo_inscricao):
                        codigo_inscricao = '02'
                    linha = linha[:1] + str(codigo_inscricao).zfill(2)[:2] + linha[3:]
                    
                    # Número de inscrição/CNPJ (posições 4-17)
                    numero_inscricao = row.get('numero_inscricao', cnpj_empresa)
                    if pd.isna(numero_inscricao):
                        numero_inscricao = cnpj_empresa
                    linha = linha[:3] + str(numero_inscricao).ljust(14)[:14] + linha[17:]
                    
                    # Código da empresa (posições 21-37)
                    codigo_emp = row.get('codigo_empresa', codigo_empresa)
                    if pd.isna(codigo_emp):
                        codigo_emp = codigo_empresa
                    linha = linha[:20] + str(codigo_emp).ljust(17)[:17] + linha[37:]
                    
                    # Nosso número (posições 71-82)
                    nosso_numero_raw = row.get('nosso_numero', '')
                    if pd.isna(nosso_numero_raw):
                        nosso_numero = ''
                    else:
                        nosso_numero = str(nosso_numero_raw).strip()
                    
                    if nosso_numero:
                        nosso_numero = nosso_numero.zfill(12)[:12]
                        linha = linha[:70] + nosso_numero + linha[82:]
                    
                    # Carteira (posições 108-109)
                    carteira_raw = row.get('carteira', '09')
                    if pd.isna(carteira_raw):
                        carteira = '09'
                    else:
                        carteira = str(carteira_raw).strip()[:2]
                    linha = linha[:107] + carteira.zfill(2) + linha[109:]
                    
                    # Data de ocorrência (posições 111-116)
                    data_ocorrencia = self._converter_data_para_ddmmaa(row.get('data_ocorrencia', ''))
                    linha = linha[:110] + data_ocorrencia + linha[116:]
                    
                    # Seu número (posições 117-126)
                    seu_numero_raw = row.get('seu_numero', '')
                    if pd.isna(seu_numero_raw):
                        seu_numero = ''
                    else:
                        seu_numero = str(seu_numero_raw).strip()[:10]
                    linha = linha[:116] + seu_numero.ljust(10) + linha[126:]
                    
                    # Data de vencimento (posições 147-152)
                    data_vencimento = self._converter_data_para_ddmmaa(row.get('data_vencimento', ''))
                    linha = linha[:146] + data_vencimento + linha[152:]
                    
                    # Valor do título (posições 153-165)
                    valor_titulo = row.get('valor_titulo', 0)
                    if pd.isna(valor_titulo):
                        valor_titulo = 0
                    
                    valor_centavos = self._converter_moeda_para_centavos(valor_titulo)
                    valor_str = str(valor_centavos).zfill(13)
                    linha = linha[:152] + valor_str + linha[165:]
                    valor_total += valor_centavos / 100
                    
                    # Banco cobrador (posições 166-168)
                    banco_cobrador = row.get('banco_cobrador', '237')
                    if pd.isna(banco_cobrador):
                        banco_cobrador = '237'
                    linha = linha[:165] + str(banco_cobrador)[:3].ljust(3) + linha[168:]
                    
                    # Agência cobradora (posições 169-173)
                    agencia_cobradora = row.get('agencia_cobradora', '06254')
                    if pd.isna(agencia_cobradora):
                        agencia_cobradora = '06254'
                    linha = linha[:168] + str(agencia_cobradora)[:5].ljust(5) + linha[173:]
                    
                    # Espécie (posições 174-175)
                    especie = row.get('especie', '01')
                    if pd.isna(especie):
                        especie = '01'
                    linha = linha[:173] + str(especie)[:2].ljust(2) + linha[175:]
                    
                    # Valor tarifa (posições 176-188)
                    valor_tarifa = row.get('valor_tarifa', 0)
                    if pd.isna(valor_tarifa):
                        valor_tarifa = 0
                    tarifa_centavos = self._converter_moeda_para_centavos(valor_tarifa)
                    linha = linha[:175] + str(tarifa_centavos).zfill(13) + linha[188:]
                    
                    # Valor IOF (posições 189-201)
                    valor_iof = row.get('valor_iof', 0)
                    if pd.isna(valor_iof):
                        valor_iof = 0
                    iof_centavos = self._converter_moeda_para_centavos(valor_iof)
                    linha = linha[:188] + str(iof_centavos).zfill(13) + linha[201:]
                    
                    # Valor abatimento (posições 228-240)
                    valor_abatimento = row.get('valor_abatimento', 0)
                    if pd.isna(valor_abatimento):
                        valor_abatimento = 0
                    abatimento_centavos = self._converter_moeda_para_centavos(valor_abatimento)
                    linha = linha[:227] + str(abatimento_centavos).zfill(13) + linha[240:]
                    
                    # Descontos (posições 241-253)
                    descontos = row.get('descontos', 0)
                    if pd.isna(descontos):
                        descontos = 0
                    desconto_centavos = self._converter_moeda_para_centavos(descontos)
                    linha = linha[:240] + str(desconto_centavos).zfill(13) + linha[253:]
                    
                    # Valor pago (posições 254-266) - usar valor do Excel se disponível
                    valor_pago = row.get('valor_principal', valor_titulo)
                    if pd.isna(valor_pago):
                        valor_pago = valor_titulo
                    pago_centavos = self._converter_moeda_para_centavos(valor_pago)
                    linha = linha[:253] + str(pago_centavos).zfill(13) + linha[266:]
                    
                    # Juros mora multa (posições 267-279)
                    juros_mora_multa = row.get('juros_mora_multa', 0)
                    if pd.isna(juros_mora_multa):
                        juros_mora_multa = 0
                    juros_centavos = self._converter_moeda_para_centavos(juros_mora_multa)
                    linha = linha[:266] + str(juros_centavos).zfill(13) + linha[279:]
                    
                    # Outros créditos (posições 280-292)
                    outros_creditos = row.get('outros_creditos', 0)
                    if pd.isna(outros_creditos):
                        outros_creditos = 0
                    creditos_centavos = self._converter_moeda_para_centavos(outros_creditos)
                    linha = linha[:279] + str(creditos_centavos).zfill(13) + linha[292:]
                    
                    # Data de crédito (posições 296-301)
                    data_credito = self._converter_data_para_ddmmaa(row.get('data_credito', ''))
                    linha = linha[:295] + data_credito + linha[301:]
                    
                    # Motivo ocorrência (posições 319-328)
                    motivo_ocorrencia = row.get('motivo_ocorrencia', '')
                    if pd.isna(motivo_ocorrencia):
                        motivo_ocorrencia = ''
                    linha = linha[:318] + str(motivo_ocorrencia)[:10].ljust(10) + linha[328:]
                    
                    # Sequencial (posições 395-400) - usar do Excel se disponível
                    sequencial_excel = row.get('sequencial', sequencial)
                    if pd.isna(sequencial_excel):
                        sequencial_final = sequencial
                    else:
                        try:
                            sequencial_final = int(str(sequencial_excel).strip())
                        except (ValueError, TypeError):
                            sequencial_final = sequencial
                    
                    sequencial_str = str(sequencial_final).zfill(6)
                    linha = linha[:394] + sequencial_str
                    
                    # Escrever linha
                    arquivo_saida.write(linha + '\n')
                    sequencial += 1
                
                # Escrever trailer
                if trailer_linha:
                    # Atualizar sequencial no trailer original
                    trailer_modificado = trailer_linha[:394] + str(sequencial).zfill(6)
                    if not trailer_modificado.endswith('\n'):
                        trailer_modificado += '\n'
                    arquivo_saida.write(trailer_modificado)
                else:
                    trailer = self._criar_trailer_padrao(len(df), valor_total)
                    arquivo_saida.write(trailer)
            
            return True, f"Arquivo CNAB gerado com sucesso: {arquivo_cnab_saida}"
            
        except Exception as e:
            return False, f"Erro ao converter Excel para CNAB: {str(e)}"

    def editor_interativo(self):
        """Editor interativo para alterações pontuais no CNAB"""
        if not self.header or not self.detalhes:
            print("❌ Erro: Arquivo CNAB não foi carregado. Execute ler_arquivo() primeiro.")
            return False
        
        print("\n" + "=" * 80)
        print("🔧 EDITOR INTERATIVO DE CNAB")
        print("=" * 80)
        print(f"📄 Arquivo: {os.path.basename(self.arquivo)}")
        print(f"📊 Total de registros: {len(self.detalhes)}")
        print("=" * 80)
        
        while True:
            print("\n📋 MENU DE OPÇÕES:")
            print("1. 📋 Listar todos os registros")
            print("2. 🔍 Buscar registro específico")
            print("3. ✏️  Editar registro")
            print("4. 💰 Editar valores em lote")
            print("5. 📅 Alterar datas em lote")
            print("6. 💾 Salvar alterações em novo CNAB")
            print("7. 📊 Mostrar resumo das alterações")
            print("8. ❌ Sair sem salvar")
            
            opcao = input("\n🎯 Escolha uma opção (1-8): ").strip()
            
            if opcao == '1':
                self._listar_registros()
            elif opcao == '2':
                self._buscar_registro()
            elif opcao == '3':
                self._editar_registro()
            elif opcao == '4':
                self._editar_valores_lote()
            elif opcao == '5':
                self._alterar_datas_lote()
            elif opcao == '6':
                return self._salvar_alteracoes()
            elif opcao == '7':
                self._mostrar_resumo_alteracoes()
            elif opcao == '8':
                print("\n❌ Saindo sem salvar alterações...")
                return False
            else:
                print("❌ Opção inválida! Escolha entre 1-8.")
    
    def _listar_registros(self):
        """Lista todos os registros com informações principais"""
        print(f"\n📋 LISTA DE REGISTROS ({len(self.detalhes)} registros)")
        print("-" * 120)
        print(f"{'#':<4} {'Nosso Número':<15} {'Seu Número':<15} {'Valor Título':<15} {'Data Venc.':<12} {'Status':<10}")
        print("-" * 120)
        
        for i, detalhe in enumerate(self.detalhes, 1):
            nosso_num = detalhe.get('nosso_numero', '')[:12]
            seu_num = detalhe.get('seu_numero', '')[:12]
            valor = self.formatar_moeda(detalhe.get('valor_titulo', 0))
            data_venc = detalhe.get('data_vencimento', '')
            status = "Alterado" if detalhe.get('_alterado', False) else "Original"
            
            print(f"{i:<4} {nosso_num:<15} {seu_num:<15} {valor:<15} {data_venc:<12} {status:<10}")
        
        print("-" * 120)
        
        # Paginação para muitos registros
        if len(self.detalhes) > 20:
            input("\n⏸  Pressione Enter para continuar...")
    
    def _buscar_registro(self):
        """Busca registro por nosso número ou seu número"""
        print("\n🔍 BUSCAR REGISTRO")
        termo = input("Digite o nosso número ou seu número para buscar: ").strip()
        
        if not termo:
            print("❌ Termo de busca não pode ser vazio.")
            return
        
        encontrados = []
        for i, detalhe in enumerate(self.detalhes):
            nosso_num = str(detalhe.get('nosso_numero', '')).strip()
            seu_num = str(detalhe.get('seu_numero', '')).strip()
            
            if termo.lower() in nosso_num.lower() or termo.lower() in seu_num.lower():
                encontrados.append((i, detalhe))
        
        if not encontrados:
            print(f"❌ Nenhum registro encontrado com '{termo}'")
            return
        
        print(f"\n✅ {len(encontrados)} registro(s) encontrado(s):")
        print("-" * 100)
        
        for i, (indice, detalhe) in enumerate(encontrados, 1):
            print(f"\n📋 Resultado {i} (Registro #{indice + 1}):")
            self._mostrar_detalhes_registro(detalhe, indice)
        
        if len(encontrados) == 1:
            editar = input(f"\n✏️  Deseja editar este registro? (s/N): ").strip().lower()
            if editar == 's':
                self._editar_registro_especifico(encontrados[0][1], encontrados[0][0])
    
    def _mostrar_detalhes_registro(self, detalhe, indice):
        """Mostra detalhes completos de um registro"""
        campos_principais = [
            ('Nosso Número', detalhe.get('nosso_numero', '')),
            ('Seu Número', detalhe.get('seu_numero', '')),
            ('Valor Título', self.formatar_moeda(detalhe.get('valor_titulo', 0))),
            ('Valor Principal', self.formatar_moeda(detalhe.get('valor_principal', 0))),
            ('Juros/Multa', self.formatar_moeda(detalhe.get('juros_mora_multa', 0))),
            ('Data Vencimento', detalhe.get('data_vencimento', '')),
            ('Data Crédito', detalhe.get('data_credito', '')),
            ('Carteira', detalhe.get('carteira', '')),
            ('Status', 'Alterado' if detalhe.get('_alterado', False) else 'Original')
        ]
        
        for campo, valor in campos_principais:
            print(f"  {campo:<20}: {valor}")
    
    def _editar_registro(self):
        """Edita um registro específico"""
        if len(self.detalhes) == 0:
            print("❌ Nenhum registro disponível para edição.")
            return
        
        print(f"\n✏️  EDITAR REGISTRO")
        print(f"Digite o número do registro (1-{len(self.detalhes)}) ou 'b' para buscar:")
        
        escolha = input("🎯 Opção: ").strip().lower()
        
        if escolha == 'b':
            self._buscar_registro()
            return
        
        try:
            indice = int(escolha) - 1
            if 0 <= indice < len(self.detalhes):
                self._editar_registro_especifico(self.detalhes[indice], indice)
            else:
                print(f"❌ Número inválido. Digite entre 1 e {len(self.detalhes)}")
        except ValueError:
            print("❌ Digite um número válido ou 'b' para buscar.")
    
    def _editar_registro_especifico(self, detalhe, indice):
        """Edita campos específicos de um registro"""
        print(f"\n✏️  EDITANDO REGISTRO #{indice + 1}")
        print("-" * 60)
        self._mostrar_detalhes_registro(detalhe, indice)
        print("-" * 60)
        
        campos_editaveis = [
            ('valor_titulo', 'Valor do Título', 'moeda'),
            ('valor_principal', 'Valor Principal', 'moeda'),
            ('juros_mora_multa', 'Juros/Mora/Multa', 'moeda'),
            ('data_vencimento', 'Data de Vencimento', 'data'),
            ('data_credito', 'Data de Crédito', 'data'),
            ('seu_numero', 'Seu Número', 'texto'),
            ('carteira', 'Carteira', 'texto'),
            ('valor_abatimento', 'Valor Abatimento', 'moeda'),
            ('descontos', 'Descontos', 'moeda'),
            ('outros_creditos', 'Outros Créditos', 'moeda')
        ]
        
        print("\n📝 CAMPOS DISPONÍVEIS PARA EDIÇÃO:")
        for i, (campo, nome, tipo) in enumerate(campos_editaveis, 1):
            valor_atual = detalhe.get(campo, '')
            if tipo == 'moeda' and isinstance(valor_atual, (int, float)):
                valor_atual = self.formatar_moeda(valor_atual)
            print(f"{i:2d}. {nome:<20}: {valor_atual}")
        
        while True:
            try:
                opcao = input(f"\n🎯 Escolha o campo para editar (1-{len(campos_editaveis)}) ou 'q' para voltar: ").strip()
                
                if opcao.lower() == 'q':
                    break
                
                indice_campo = int(opcao) - 1
                if 0 <= indice_campo < len(campos_editaveis):
                    campo, nome, tipo = campos_editaveis[indice_campo]
                    self._editar_campo(detalhe, campo, nome, tipo)
                else:
                    print(f"❌ Opção inválida. Digite entre 1 e {len(campos_editaveis)}")
                    
            except ValueError:
                print("❌ Digite um número válido ou 'q' para voltar.")
    
    def _editar_campo(self, detalhe, campo, nome, tipo):
        """Edita um campo específico"""
        valor_atual = detalhe.get(campo, '')
        if tipo == 'moeda' and isinstance(valor_atual, (int, float)):
            valor_atual = self.formatar_moeda(valor_atual)
        
        print(f"\n✏️  Editando: {nome}")
        print(f"Valor atual: {valor_atual}")
        
        if tipo == 'moeda':
            print("💡 Digite valores como: 1234.56 ou 1234,56 ou R$ 1.234,56")
        elif tipo == 'data':
            print("💡 Digite datas como: DD/MM/AAAA (ex: 31/12/2024)")
        
        novo_valor = input(f"🎯 Novo valor (Enter para manter atual): ").strip()
        
        if not novo_valor:
            print("✅ Valor mantido sem alteração.")
            return
        
        # Validar e converter o valor
        try:
            if tipo == 'moeda':
                valor_convertido = self._converter_moeda_para_float(novo_valor)
                detalhe[campo] = valor_convertido
                print(f"✅ {nome} alterado para: {self.formatar_moeda(valor_convertido)}")
            elif tipo == 'data':
                if self._validar_data(novo_valor):
                    detalhe[campo] = novo_valor
                    print(f"✅ {nome} alterado para: {novo_valor}")
                else:
                    print("❌ Data inválida. Use o formato DD/MM/AAAA")
                    return
            else:  # texto
                detalhe[campo] = novo_valor[:10]  # Limitar tamanho
                print(f"✅ {nome} alterado para: {novo_valor[:10]}")
            
            # Marcar como alterado
            detalhe['_alterado'] = True
            
        except Exception as e:
            print(f"❌ Erro ao converter valor: {str(e)}")
    
    def _converter_moeda_para_float(self, valor_str):
        """Converte string monetária para float"""
        if not valor_str:
            return 0.0
        
        # Remove símbolos e espaços
        valor_limpo = str(valor_str).replace('R$', '').replace(' ', '').strip()
        
        # Trata formatos brasileiros
        if ',' in valor_limpo and '.' in valor_limpo:
            # Formato: 1.234,56
            valor_limpo = valor_limpo.replace('.', '').replace(',', '.')
        elif ',' in valor_limpo:
            # Formato: 1234,56
            valor_limpo = valor_limpo.replace(',', '.')
        
        return float(valor_limpo)
    
    def _validar_data(self, data_str):
        """Valida formato de data DD/MM/AAAA"""
        try:
            if len(data_str) != 10 or data_str.count('/') != 2:
                return False
            
            partes = data_str.split('/')
            dia, mes, ano = int(partes[0]), int(partes[1]), int(partes[2])
            
            if not (1 <= dia <= 31 and 1 <= mes <= 12 and 1900 <= ano <= 2100):
                return False
            
            # Verificação básica de data válida
            datetime.strptime(data_str, '%d/%m/%Y')
            return True
        except:
            return False
    
    def _editar_valores_lote(self):
        """Edita valores em lote com filtros"""
        print("\n💰 EDIÇÃO DE VALORES EM LOTE")
        print("1. Adicionar percentual a todos os títulos")
        print("2. Adicionar valor fixo a todos os títulos")
        print("3. Zerar juros/multa de todos os títulos")
        print("4. Aplicar desconto percentual")
        
        opcao = input("🎯 Escolha (1-4): ").strip()
        
        if opcao == '1':
            try:
                percentual = float(input("Digite o percentual (ex: 10 para 10%): "))
                confirmacao = input(f"Confirma adicionar {percentual}% a todos os valores? (s/N): ")
                if confirmacao.lower() == 's':
                    for detalhe in self.detalhes:
                        valor_atual = detalhe.get('valor_titulo', 0)
                        novo_valor = valor_atual * (1 + percentual / 100)
                        detalhe['valor_titulo'] = novo_valor
                        detalhe['valor_principal'] = novo_valor
                        detalhe['_alterado'] = True
                    print(f"✅ {percentual}% adicionado a {len(self.detalhes)} registros")
            except ValueError:
                print("❌ Percentual inválido")
        
        elif opcao == '2':
            try:
                valor_fixo = self._converter_moeda_para_float(input("Digite o valor a adicionar: "))
                confirmacao = input(f"Confirma adicionar {self.formatar_moeda(valor_fixo)} a todos? (s/N): ")
                if confirmacao.lower() == 's':
                    for detalhe in self.detalhes:
                        detalhe['valor_titulo'] += valor_fixo
                        detalhe['valor_principal'] += valor_fixo
                        detalhe['_alterado'] = True
                    print(f"✅ {self.formatar_moeda(valor_fixo)} adicionado a {len(self.detalhes)} registros")
            except ValueError:
                print("❌ Valor inválido")
        
        elif opcao == '3':
            confirmacao = input("Confirma zerar juros/multa de todos os títulos? (s/N): ")
            if confirmacao.lower() == 's':
                for detalhe in self.detalhes:
                    detalhe['juros_mora_multa'] = 0.0
                    detalhe['_alterado'] = True
                print(f"✅ Juros/multa zerados em {len(self.detalhes)} registros")
        
        elif opcao == '4':
            try:
                desconto = float(input("Digite o desconto percentual (ex: 5 para 5%): "))
                confirmacao = input(f"Confirma aplicar {desconto}% de desconto? (s/N): ")
                if confirmacao.lower() == 's':
                    for detalhe in self.detalhes:
                        valor_atual = detalhe.get('valor_titulo', 0)
                        novo_valor = valor_atual * (1 - desconto / 100)
                        detalhe['valor_titulo'] = novo_valor
                        detalhe['valor_principal'] = novo_valor
                        detalhe['_alterado'] = True
                    print(f"✅ {desconto}% de desconto aplicado a {len(self.detalhes)} registros")
            except ValueError:
                print("❌ Percentual inválido")
    
    def _alterar_datas_lote(self):
        """Altera datas em lote"""
        print("\n📅 ALTERAÇÃO DE DATAS EM LOTE")
        print("1. Alterar data de crédito de todos os registros")
        print("2. Postergar vencimento por X dias")
        print("3. Definir nova data de vencimento para todos")
        
        opcao = input("🎯 Escolha (1-3): ").strip()
        
        if opcao == '1':
            nova_data = input("Digite a nova data de crédito (DD/MM/AAAA): ")
            if self._validar_data(nova_data):
                confirmacao = input(f"Confirma alterar data de crédito para {nova_data}? (s/N): ")
                if confirmacao.lower() == 's':
                    for detalhe in self.detalhes:
                        detalhe['data_credito'] = nova_data
                        detalhe['_alterado'] = True
                    print(f"✅ Data de crédito alterada para {nova_data} em {len(self.detalhes)} registros")
            else:
                print("❌ Data inválida")
        
        elif opcao == '2':
            try:
                dias = int(input("Digite quantos dias postergar: "))
                confirmacao = input(f"Confirma postergar vencimento por {dias} dias? (s/N): ")
                if confirmacao.lower() == 's':
                    alterados = 0
                    for detalhe in self.detalhes:
                        data_atual = detalhe.get('data_vencimento', '')
                        if data_atual:
                            try:
                                data_obj = datetime.strptime(data_atual, '%d/%m/%Y')
                                nova_data_obj = data_obj + pd.Timedelta(days=dias)
                                nova_data = nova_data_obj.strftime('%d/%m/%Y')
                                detalhe['data_vencimento'] = nova_data
                                detalhe['_alterado'] = True
                                alterados += 1
                            except:
                                continue
                    print(f"✅ {alterados} registros tiveram vencimento postergado por {dias} dias")
            except ValueError:
                print("❌ Número de dias inválido")
        
        elif opcao == '3':
            nova_data = input("Digite a nova data de vencimento (DD/MM/AAAA): ")
            if self._validar_data(nova_data):
                confirmacao = input(f"Confirma definir {nova_data} como vencimento para todos? (s/N): ")
                if confirmacao.lower() == 's':
                    for detalhe in self.detalhes:
                        detalhe['data_vencimento'] = nova_data
                        detalhe['_alterado'] = True
                    print(f"✅ Data de vencimento alterada para {nova_data} em {len(self.detalhes)} registros")
            else:
                print("❌ Data inválida")
    
    def _mostrar_resumo_alteracoes(self):
        """Mostra resumo das alterações feitas"""
        alterados = [d for d in self.detalhes if d.get('_alterado', False)]
        
        if not alterados:
            print("\n📊 RESUMO: Nenhuma alteração foi feita ainda.")
            return
        
        print(f"\n📊 RESUMO DAS ALTERAÇÕES")
        print(f"📝 Total de registros alterados: {len(alterados)}")
        print(f"📝 Total de registros: {len(self.detalhes)}")
        print(f"📝 Percentual alterado: {len(alterados)/len(self.detalhes)*100:.1f}%")
        
        print(f"\n📋 REGISTROS ALTERADOS:")
        print("-" * 80)
        for i, detalhe in enumerate(alterados, 1):
            nosso_num = detalhe.get('nosso_numero', '')[:12]
            valor = self.formatar_moeda(detalhe.get('valor_titulo', 0))
            print(f"{i:3d}. {nosso_num:<15} - Valor: {valor}")
            if i >= 10:
                print(f"    ... e mais {len(alterados) - 10} registros")
                break
        print("-" * 80)
    
    def _salvar_alteracoes(self):
        """Salva as alterações em um novo arquivo CNAB"""
        alterados = [d for d in self.detalhes if d.get('_alterado', False)]
        
        if not alterados:
            print("\n❌ Nenhuma alteração foi feita. Nada para salvar.")
            return False
        
        print(f"\n💾 SALVAR ALTERAÇÕES")
        print(f"📝 {len(alterados)} registro(s) foram alterados")
        
        # Sugerir nome do arquivo
        nome_original = os.path.basename(self.arquivo)
        nome_base = os.path.splitext(nome_original)[0]
        nome_sugerido = f"{nome_base}_editado.TXT"
        
        nome_arquivo = input(f"📄 Nome do arquivo (Enter para '{nome_sugerido}'): ").strip()
        if not nome_arquivo:
            nome_arquivo = nome_sugerido
        
        if not nome_arquivo.upper().endswith('.TXT'):
            nome_arquivo += '.TXT'
        
        confirmacao = input(f"💾 Confirma salvar alterações em '{nome_arquivo}'? (s/N): ")
        if confirmacao.lower() != 's':
            print("❌ Salvamento cancelado.")
            return False
        
        try:
            # Gerar o novo arquivo CNAB com alterações
            with open(nome_arquivo, 'w', encoding='utf-8') as arquivo_saida:
                # Escrever header original
                if hasattr(self, 'header') and isinstance(self.header, dict) and 'linha_original' in self.header:
                    arquivo_saida.write(self.header['linha_original'])
                else:
                    # Criar header padrão se não existir
                    header_padrao = self._criar_header_padrao()
                    arquivo_saida.write(header_padrao)
                
                # Escrever detalhes (alterados e originais)
                for i, detalhe in enumerate(self.detalhes, 2):
                    if detalhe.get('_alterado', False):
                        # Reconstruir linha com alterações
                        linha = self._reconstruir_linha_cnab(detalhe, i)
                    else:
                        # Usar linha original
                        linha = detalhe.get('linha_original', '')
                        if not linha.endswith('\n'):
                            linha += '\n'
                    
                    arquivo_saida.write(linha)
                
                # Escrever trailer original (ou atualizado)
                if hasattr(self, 'trailer') and isinstance(self.trailer, dict) and 'linha_original' in self.trailer:
                    trailer_linha = self.trailer['linha_original']
                    # Atualizar sequencial no trailer
                    sequencial = len(self.detalhes) + 2
                    trailer_linha = trailer_linha[:394] + str(sequencial).zfill(6)
                    if not trailer_linha.endswith('\n'):
                        trailer_linha += '\n'
                    arquivo_saida.write(trailer_linha)
                else:
                    # Criar trailer padrão se não existir
                    valor_total = sum(d.get('valor_titulo', 0) for d in self.detalhes)
                    trailer_padrao = self._criar_trailer_padrao(len(self.detalhes), valor_total)
                    arquivo_saida.write(trailer_padrao)
            
            print(f"✅ Arquivo salvo com sucesso: {nome_arquivo}")
            print(f"📊 {len(alterados)} alterações aplicadas")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao salvar arquivo: {str(e)}")
            return False
    
    def _reconstruir_linha_cnab(self, detalhe, sequencial):
        """Reconstrói uma linha CNAB com base nos dados alterados"""
        linha = ' ' * 400
        
        # Usar método existente de conversão Excel para CNAB
        # Criar DataFrame temporário com um registro
        df_temp = pd.DataFrame([detalhe])
        
        # Usar lógica similar ao excel_para_cnab mas para uma linha
        # Tipo de registro
        linha = '1' + linha[1:]
        
        # Código de inscrição
        codigo_inscricao = detalhe.get('codigo_inscricao', '02')
        linha = linha[:1] + str(codigo_inscricao).zfill(2)[:2] + linha[3:]
        
        # CNPJ
        numero_inscricao = detalhe.get('numero_inscricao', '12345678000123')
        linha = linha[:3] + str(numero_inscricao).ljust(14)[:14] + linha[17:]
        
        # Código da empresa
        codigo_empresa = detalhe.get('codigo_empresa', '00000090368400035')
        linha = linha[:20] + str(codigo_empresa).ljust(17)[:17] + linha[37:]
        
        # Nosso número
        nosso_numero = str(detalhe.get('nosso_numero', '')).strip().zfill(12)[:12]
        linha = linha[:70] + nosso_numero + linha[82:]
        
        # Carteira
        carteira = str(detalhe.get('carteira', '09')).strip()[:2].zfill(2)
        linha = linha[:107] + carteira + linha[109:]
        
        # Data de ocorrência
        data_ocorrencia = self._converter_data_para_ddmmaa(detalhe.get('data_ocorrencia', ''))
        linha = linha[:110] + data_ocorrencia + linha[116:]
        
        # Seu número
        seu_numero = str(detalhe.get('seu_numero', '')).strip()[:10].ljust(10)
        linha = linha[:116] + seu_numero + linha[126:]
        
        # Data de vencimento
        data_vencimento = self._converter_data_para_ddmmaa(detalhe.get('data_vencimento', ''))
        linha = linha[:146] + data_vencimento + linha[152:]
        
        # Valor do título
        valor_titulo = detalhe.get('valor_titulo', 0)
        valor_centavos = int(valor_titulo * 100) if valor_titulo else 0
        linha = linha[:152] + str(valor_centavos).zfill(13) + linha[165:]
        
        # Banco e agência
        linha = linha[:165] + '237' + linha[168:]  # Banco
        linha = linha[:168] + '06254' + linha[173:]  # Agência
        
        # Valores diversos
        campos_monetarios = [
            ('valor_tarifa', 175, 188),
            ('valor_iof', 188, 201),
            ('valor_abatimento', 227, 240),
            ('descontos', 240, 253),
            ('valor_principal', 253, 266),
            ('juros_mora_multa', 266, 279),
            ('outros_creditos', 279, 292)
        ]
        
        for campo, inicio, fim in campos_monetarios:
            valor = detalhe.get(campo, 0)
            valor_centavos = int(valor * 100) if valor else 0
            linha = linha[:inicio] + str(valor_centavos).zfill(fim - inicio) + linha[fim:]
        
        # Data de crédito
        data_credito = self._converter_data_para_ddmmaa(detalhe.get('data_credito', ''))
        linha = linha[:295] + data_credito + linha[301:]
        
        # Sequencial
        linha = linha[:394] + str(sequencial).zfill(6)
        
        return linha + '\n'



    def gerar_cnab_editado_sem_juros(self, caminho_saida):
        """Gera um novo arquivo CNAB com as alterações do editor gráfico E sem juros/multa"""
        try:
            # Usar método seguro de edição (estilo editor de texto)
            return self._editar_cnab_seguro(caminho_saida, zerar_juros=True)
            
        except Exception as e:
            return False, f"Erro ao gerar arquivo CNAB: {str(e)}"

    def gerar_cnab_editado(self, caminho_saida):
        """Gera um novo arquivo CNAB com as alterações feitas no editor gráfico (método seguro)"""
        try:
            # Usar método seguro de edição (estilo editor de texto)
            return self._editar_cnab_seguro(caminho_saida, zerar_juros=False)
            
        except Exception as e:
            return False, f"Erro ao salvar arquivo: {str(e)}"

    def _editar_cnab_seguro(self, caminho_saida, zerar_juros=False):
        """
        Edita o arquivo CNAB de forma segura, como um editor de texto.
        Altera apenas os campos específicos sem reconstruir o arquivo inteiro.
        """
        try:
            # Verificar se há alterações
            alterados = [d for d in self.detalhes if d.get('_alterado', False)]
            
            # Ler o arquivo original como texto, preservando encoding
            with open(self.arquivo, 'r', encoding='utf-8', newline='') as arquivo_original:
                linhas_originais = arquivo_original.readlines()
            
            # Criar lista de linhas editadas
            linhas_editadas = []
            contador_detalhes = 0
            alteracoes_realizadas = 0
            header_alterado = False
            
            for linha in linhas_originais:
                linha_editada = linha
                
                # Verificar se é uma linha de header (tipo 0) e alterar código da empresa
                if linha.strip() and linha[0] == '0':
                    linha_editada = self._alterar_header_codigo_empresa(linha)
                    header_alterado = True
                
                # Verificar se é uma linha de detalhe (tipo 1)
                elif linha.strip() and linha[0] == '1':
                    if contador_detalhes < len(self.detalhes):
                        detalhe = self.detalhes[contador_detalhes]
                        
                        # Se o registro foi alterado, aplicar edições pontuais
                        if detalhe.get('_alterado', False):
                            linha_editada = self._aplicar_edicoes_pontuais(linha, detalhe)
                            alteracoes_realizadas += 1
                        
                        # Se deve zerar juros, aplicar zeramento pontual
                        if zerar_juros:
                            linha_editada = self._zerar_juros_pontual(linha_editada)
                    
                    contador_detalhes += 1
                
                linhas_editadas.append(linha_editada)
            
            # Salvar arquivo editado preservando formato original
            with open(caminho_saida, 'w', encoding='utf-8', newline='') as arquivo_saida:
                arquivo_saida.writelines(linhas_editadas)
            
            # Preparar mensagem de retorno
            mensagem_partes = []
            
            if header_alterado:
                mensagem_partes.append("Cabeçalho atualizado com código da empresa TC")
            
            if zerar_juros and alteracoes_realizadas > 0:
                mensagem_partes.append(f"{alteracoes_realizadas} alterações aplicadas e juros/multa zerados")
            elif zerar_juros:
                mensagem_partes.append("Juros/multa zerados em todos os registros")
            elif alteracoes_realizadas > 0:
                mensagem_partes.append(f"{alteracoes_realizadas} alterações aplicadas")
            
            if not mensagem_partes:
                mensagem_partes.append("Arquivo processado")
            
            mensagem = f"Arquivo CNAB gerado com sucesso: {caminho_saida}\n" + "\n".join(mensagem_partes)
            
            return True, mensagem
            
        except Exception as e:
            return False, f"Erro ao editar arquivo CNAB: {str(e)}"

    def _alterar_header_codigo_empresa(self, linha_header):
        """
        Altera o código da empresa no header de forma pontual.
        Aplica o código específico "00000000036846335521TC" nas posições 27-46 (20 caracteres).
        """
        linha_editada = linha_header.rstrip('\n\r')  # Remove quebras de linha temporariamente
        
        # Garantir que a linha tenha pelo menos 400 caracteres
        if len(linha_editada) < 400:
            linha_editada = linha_editada.ljust(400)
        
        # Código da empresa específico para TC SECURITIZADORA
        codigo_empresa_tc = "00000000036846335521TC"
        
        # Alterar código da empresa (posições 26-46, 20 caracteres - baseado no _criar_header_padrao)
        if len(linha_editada) >= 46:
            codigo_ajustado = codigo_empresa_tc.ljust(20)[:20]  # Ajustar para 20 caracteres
            linha_editada = linha_editada[:26] + codigo_ajustado + linha_editada[46:]
        
        # Restaurar quebra de linha original
        return linha_editada + '\n'

    def _aplicar_edicoes_pontuais(self, linha, detalhe):
        """
        Aplica edições pontuais em campos específicos, como um editor de texto.
        Altera apenas as posições exatas dos campos editados.
        """
        linha_editada = linha.rstrip('\n\r')  # Remove quebras de linha temporariamente
        
        # Garantir que a linha tenha pelo menos 400 caracteres
        if len(linha_editada) < 400:
            linha_editada = linha_editada.ljust(400)
        
        # Editar NOSSO_NUMERO (posições 70-82, 12 caracteres)
        if 'nosso_numero' in detalhe and detalhe.get('_alterado', False):
            novo_nosso_numero = str(detalhe['nosso_numero']).strip()
            if novo_nosso_numero:
                # Ajustar para 12 caracteres (preencher com zeros à esquerda ou truncar)
                novo_nosso_numero = novo_nosso_numero.zfill(12)[:12]
                linha_editada = linha_editada[:70] + novo_nosso_numero + linha_editada[82:]
        
        # Editar CODIGO_EMPRESA (posições 20-37, 17 caracteres)
        if 'codigo_empresa' in detalhe and detalhe.get('_alterado', False):
            novo_codigo_empresa = str(detalhe['codigo_empresa']).strip()
            if novo_codigo_empresa:
                # Ajustar para 17 caracteres (preencher com espaços à direita ou truncar)
                novo_codigo_empresa = novo_codigo_empresa.ljust(17)[:17]
                linha_editada = linha_editada[:20] + novo_codigo_empresa + linha_editada[37:]
        
        # Restaurar quebra de linha original
        return linha_editada + '\n'

    def _zerar_juros_pontual(self, linha):
        """
        Zera os juros/multa de forma pontual, alterando apenas as posições específicas.
        Posições 266-279 (13 caracteres) = juros/mora/multa
        """
        linha_editada = linha.rstrip('\n\r')  # Remove quebras de linha temporariamente
        
        # Garantir que a linha tenha pelo menos 400 caracteres
        if len(linha_editada) < 400:
            linha_editada = linha_editada.ljust(400)
        
        # Zerar juros/multa (posições 266-279)
        if len(linha_editada) >= 279:
            linha_editada = linha_editada[:266] + '0000000000000' + linha_editada[279:]
        
        # Restaurar quebra de linha original
        return linha_editada + '\n'

    def _reconstruir_linha_cnab_sem_juros(self, detalhe, sequencial):
        """Reconstrói uma linha CNAB com base nos dados alterados e zera juros/multa"""
        linha = ' ' * 400
        
        # Usar método existente de conversão Excel para CNAB
        # Criar DataFrame temporário com um registro
        df_temp = pd.DataFrame([detalhe])
        
        # Usar lógica similar ao excel_para_cnab mas para uma linha
        # Tipo de registro
        linha = '1' + linha[1:]
        
        # Código de inscrição
        codigo_inscricao = detalhe.get('codigo_inscricao', '02')
        linha = linha[:1] + str(codigo_inscricao).zfill(2)[:2] + linha[3:]
        
        # CNPJ
        numero_inscricao = detalhe.get('numero_inscricao', '12345678000123')
        linha = linha[:3] + str(numero_inscricao).ljust(14)[:14] + linha[17:]
        
        # Código da empresa
        codigo_empresa = detalhe.get('codigo_empresa', '00000090368400035')
        linha = linha[:20] + str(codigo_empresa).ljust(17)[:17] + linha[37:]
        
        # Nosso número
        nosso_numero = str(detalhe.get('nosso_numero', '')).strip().zfill(12)[:12]
        linha = linha[:70] + nosso_numero + linha[82:]
        
        # Carteira
        carteira = str(detalhe.get('carteira', '09')).strip()[:2].zfill(2)
        linha = linha[:107] + carteira + linha[109:]
        
        # Data de ocorrência
        data_ocorrencia = self._converter_data_para_ddmmaa(detalhe.get('data_ocorrencia', ''))
        linha = linha[:110] + data_ocorrencia + linha[116:]
        
        # Seu número
        seu_numero = str(detalhe.get('seu_numero', '')).strip()[:10].ljust(10)
        linha = linha[:116] + seu_numero + linha[126:]
        
        # Data de vencimento
        data_vencimento = self._converter_data_para_ddmmaa(detalhe.get('data_vencimento', ''))
        linha = linha[:146] + data_vencimento + linha[152:]
        
        # Valor do título
        valor_titulo = detalhe.get('valor_titulo', 0)
        valor_centavos = int(valor_titulo * 100) if valor_titulo else 0
        linha = linha[:152] + str(valor_centavos).zfill(13) + linha[165:]
        
        # Banco e agência
        linha = linha[:165] + '237' + linha[168:]  # Banco
        linha = linha[:168] + '06254' + linha[173:]  # Agência
        
        # Valores diversos (incluindo zeramento de juros)
        campos_monetarios = [
            ('valor_tarifa', 175, 188),
            ('valor_iof', 188, 201),
            ('valor_abatimento', 227, 240),
            ('descontos', 240, 253),
            ('valor_principal', 253, 266),
            ('juros_mora_multa', 266, 279, True),  # Marcar para zerar
            ('outros_creditos', 279, 292)
        ]
        
        for campo_info in campos_monetarios:
            if len(campo_info) == 4:  # Campo marcado para zerar
                campo, inicio, fim, zerar = campo_info
                if zerar:
                    valor_centavos = 0  # Forçar zero para juros/multa
                else:
                    valor = detalhe.get(campo, 0)
                    valor_centavos = int(valor * 100) if valor else 0
            else:
                campo, inicio, fim = campo_info
                valor = detalhe.get(campo, 0)
                valor_centavos = int(valor * 100) if valor else 0
            
            linha = linha[:inicio] + str(valor_centavos).zfill(fim - inicio) + linha[fim:]
        
        # Data de crédito
        data_credito = self._converter_data_para_ddmmaa(detalhe.get('data_credito', ''))
        linha = linha[:295] + data_credito + linha[301:]
        
        # Sequencial
        linha = linha[:394] + str(sequencial).zfill(6)
        
        return linha + '\n'


def main():
    print("=" * 50)
    print("LEITOR DE ARQUIVO CNAB 400 - BRADESCO (237)")
    print("=" * 50)
    
    # Solicitar o nome do arquivo
    arquivo = input("Digite o caminho do arquivo CNAB: ")
        
    if not os.path.exists(arquivo):
        print(f"Arquivo não encontrado: {arquivo}")
        return
    
    # Processar o arquivo
    processador = CNABBradesco(arquivo)
    if processador.ler_arquivo():
        processador.gerar_relatorio()
        
        # Perguntar se deseja gerar arquivo CNAB de retorno
        gerar_cnab = input("\nDeseja gerar arquivo CNAB de retorno sem juros? (s/n): ")
        if gerar_cnab.lower() == 's':
            nome_arquivo = os.path.basename(arquivo)
            nome_base = re.sub(r'\.TXT$', '', nome_arquivo, flags=re.IGNORECASE)
            caminho_saida = f"{nome_base}_retorno.TXT"
            
            sucesso, mensagem = processador.gerar_cnab_retorno(caminho_saida)
            print(mensagem)
    else:
        print("Falha ao processar o arquivo.")


if __name__ == "__main__":
    main() 