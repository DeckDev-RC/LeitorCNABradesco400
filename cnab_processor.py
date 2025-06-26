import os
import pandas as pd
import re
from datetime import datetime

class CNABProcessor:
    def __init__(self):
        self.data = []
        self.header = None
        self.trailer = None
        self.filename = None
        
    def read_cnab(self, filename):
        self.filename = filename
        self.data = []
        
        with open(filename, 'r') as file:
            lines = file.readlines()
            
        if not lines:
            return False
            
        # Processar o cabeçalho (primeira linha)
        if lines and len(lines[0]) > 1:
            self.header = lines[0]
            
        # Processar o trailer (última linha)
        if lines and len(lines) > 1:
            self.trailer = lines[-1]
            
        # Processar registros de detalhe
        for i, line in enumerate(lines):
            if i == 0 or i == len(lines) - 1:
                continue  # Pular cabeçalho e trailer
                
            if len(line.strip()) < 400:  # Verificar se a linha tem o tamanho mínimo
                continue
                
            # Extrair informações relevantes da linha
            registro = {
                'linha_original': line,
                'nosso_numero': line[70:81].strip(),
                'valor_titulo': float(line[152:165]) / 100,  # Converter centavos para reais
                'valor_pago': float(line[253:266]) / 100,    # Converter centavos para reais
                'valor_juros': float(line[266:279]) / 100,   # Converter centavos para reais
                'valor_multa': 0.0,  # Inicialmente zero, calculado abaixo
                'data_pagamento': line[295:301],
                'sequencial': line[-7:].strip()  # Número sequencial no final da linha
            }
            
            # Calcular valor da multa (valor pago - valor título - juros)
            diferenca = registro['valor_pago'] - registro['valor_titulo'] - registro['valor_juros']
            if diferenca > 0:
                registro['valor_multa'] = diferenca
                
            self.data.append(registro)
            
        return True
    
    def to_dataframe(self):
        if not self.data:
            return pd.DataFrame()
            
        df = pd.DataFrame(self.data)
        
        # Converter data de pagamento para formato legível
        df['data_pagamento_formatada'] = df['data_pagamento'].apply(
            lambda x: f"{x[0:2]}/{x[2:4]}/{x[4:6]}" if len(x) == 6 else ""
        )
        
        # Colunas para o DataFrame final
        colunas = [
            'nosso_numero', 
            'valor_titulo', 
            'valor_pago', 
            'valor_juros', 
            'valor_multa',
            'data_pagamento_formatada'
        ]
        
        # Verificar se todas as colunas existem
        colunas_existentes = [col for col in colunas if col in df.columns]
        
        return df[colunas_existentes]
    
    def to_excel(self, output_file):
        df = self.to_dataframe()
        if df.empty:
            return False
            
        df.to_excel(output_file, index=False)
        return True
    
    def to_csv(self, output_file):
        df = self.to_dataframe()
        if df.empty:
            return False
            
        df.to_csv(output_file, index=False, sep=';')
        return True
    
    def gerar_cnab_sem_juros(self, output_file):
        if not self.data or not self.header or not self.trailer:
            return False
            
        with open(output_file, 'w') as file:
            # Escrever o cabeçalho
            file.write(self.header)
            
            # Escrever os registros de detalhe modificados
            for registro in self.data:
                linha = registro['linha_original']
                
                # Atualizar o valor principal para ser igual ao valor do título
                valor_titulo_centavos = int(registro['valor_titulo'] * 100)
                valor_titulo_str = str(valor_titulo_centavos).zfill(13)
                
                # Zerar juros e multas
                zeros = "0".zfill(13)
                
                # Substituir valores na linha
                nova_linha = linha[:152] + valor_titulo_str + linha[165:253] + valor_titulo_str + zeros + zeros + linha[292:]
                
                # Garantir que o número sequencial esteja no final da linha
                if 'sequencial' in registro and registro['sequencial']:
                    sequencial = registro['sequencial'].rjust(7, '0')
                    # Manter o sequencial original na mesma posição
                    # Encontrar a posição correta para o sequencial (últimos 7 caracteres)
                    nova_linha = nova_linha[:-7] + sequencial
                
                file.write(nova_linha)
            
            # Escrever o trailer
            file.write(self.trailer)
            
        return True
    
    @staticmethod
    def formatar_moeda_br(valor):
        return f"R$ {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')


# Função para uso direto pelo terminal
def processar_arquivo(arquivo_entrada, arquivo_saida, formato="xlsx"):
    processor = CNABProcessor()
    if processor.read_cnab(arquivo_entrada):
        if formato.lower() == "csv":
            return processor.to_csv(arquivo_saida)
        else:
            return processor.to_excel(arquivo_saida)
    return False

# Se executado diretamente
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Uso: python cnab_processor.py arquivo_entrada.txt arquivo_saida.xlsx [formato]")
        sys.exit(1)
        
    arquivo_entrada = sys.argv[1]
    arquivo_saida = sys.argv[2]
    formato = sys.argv[3] if len(sys.argv) > 3 else "xlsx"
    
    if processar_arquivo(arquivo_entrada, arquivo_saida, formato):
        print(f"Arquivo processado com sucesso e salvo como {arquivo_saida}")
    else:
        print("Erro ao processar o arquivo.") 