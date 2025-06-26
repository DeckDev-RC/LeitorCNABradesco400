import os
import sys
import pandas as pd
import glob
import re
from datetime import datetime
from cnab_bradesco import CNABBradesco

def formatar_moeda(valor):
    """Formata um valor para o padrão monetário brasileiro"""
    return f"R$ {valor:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')

def processar_lote():
    print("=" * 70)
    print("PROCESSAMENTO EM LOTE DE ARQUIVOS CNAB 400 - BRADESCO (237)")
    print("=" * 70)
    
    # Solicitar pasta dos arquivos
    pasta = input("Digite o caminho da pasta com os arquivos CNAB (ou Enter para pasta atual): ")
    if not pasta.strip():
        pasta = "."
    
    # Verificar se a pasta existe
    if not os.path.isdir(pasta):
        print(f"Pasta não encontrada: {pasta}")
        return
    
    # Buscar arquivos .TXT na pasta
    arquivos = glob.glob(os.path.join(pasta, "*.TXT"))
    
    if not arquivos:
        print(f"Nenhum arquivo .TXT encontrado na pasta: {pasta}")
        return
    
    print(f"Encontrados {len(arquivos)} arquivos para processamento.")
    
    # Perguntar sobre a exportação para Excel
    exportar_excel = input("Deseja exportar os dados para Excel? (s/n): ").lower() == 's'
    
    # Perguntar sobre a geração de arquivos CNAB de retorno
    gerar_cnab = input("Deseja gerar arquivos CNAB de retorno sem juros? (s/n): ").lower() == 's'
    
    # Criar pasta de saída
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pasta_saida = os.path.join(pasta, f"processados_{timestamp}")
    os.makedirs(pasta_saida, exist_ok=True)
    
    # Resultados consolidados
    total_arquivos = len(arquivos)
    arquivos_processados = 0
    total_titulos = 0
    valor_total = 0
    
    # DataFrame consolidado para todos os arquivos
    df_consolidado = pd.DataFrame()
    
    # Processar cada arquivo
    for i, arquivo in enumerate(arquivos, 1):
        nome_arquivo = os.path.basename(arquivo)
        print(f"\n[{i}/{total_arquivos}] Processando: {nome_arquivo}")
        
        # Criar instância do processador CNAB
        processador = CNABBradesco(arquivo)
        
        # Ler e processar o arquivo
        if processador.ler_arquivo():
            arquivos_processados += 1
            qtd_titulos = len(processador.detalhes)
            total_titulos += qtd_titulos
            
            # Calcular valor total
            valor_arquivo = sum(detalhe['valor_principal'] for detalhe in processador.detalhes)
            valor_total += valor_arquivo
            
            print(f"  Títulos processados: {qtd_titulos}")
            print(f"  Valor total: {processador.formatar_moeda(valor_arquivo)}")
            
            # Criar nome base para os arquivos de saída
            nome_base = re.sub(r'\.TXT$', '', nome_arquivo, flags=re.IGNORECASE)
            
            # Exportar para CSV
            df = pd.DataFrame(processador.detalhes)
            if 'linha_original' in df.columns:
                df = df.drop('linha_original', axis=1)
                
            caminho_csv = os.path.join(pasta_saida, f"{nome_base}_processado.csv")
            df.to_csv(caminho_csv, index=False, sep=';')
            print(f"  CSV exportado: {os.path.basename(caminho_csv)}")
            
            # Exportar para Excel se solicitado
            if exportar_excel:
                caminho_excel = os.path.join(pasta_saida, f"{nome_base}_processado.xlsx")
                sucesso, mensagem = processador.exportar_para_excel(caminho_excel)
                if sucesso:
                    print(f"  Excel exportado: {os.path.basename(caminho_excel)}")
                else:
                    print(f"  Erro ao exportar Excel: {mensagem}")
            
            # Gerar arquivo CNAB de retorno se solicitado
            if gerar_cnab:
                caminho_cnab = os.path.join(pasta_saida, f"{nome_base}_retorno.TXT")
                sucesso, mensagem = processador.gerar_cnab_retorno(caminho_cnab)
                if sucesso:
                    print(f"  CNAB de retorno gerado: {os.path.basename(caminho_cnab)}")
                else:
                    print(f"  Erro ao gerar CNAB: {mensagem}")
            
            # Adicionar ao DataFrame consolidado
            df['arquivo_origem'] = nome_arquivo
            df_consolidado = pd.concat([df_consolidado, df], ignore_index=True)
        else:
            print(f"  Erro ao processar o arquivo.")
    
    # Salvar resultados consolidados
    if not df_consolidado.empty:
        # Exportar CSV consolidado
        caminho_consolidado = os.path.join(pasta_saida, f"consolidado_{timestamp}.csv")
        df_consolidado.to_csv(caminho_consolidado, index=False, sep=';')
        
        # Exportar Excel consolidado se solicitado
        if exportar_excel:
            caminho_excel_consolidado = os.path.join(pasta_saida, f"consolidado_{timestamp}.xlsx")
            
            # Criar o escritor Excel
            writer = pd.ExcelWriter(caminho_excel_consolidado, engine='openpyxl')
            
            # Exportar dados detalhados
            df_consolidado.to_excel(writer, sheet_name='Detalhes', index=False)
            
            # Criar resumo por arquivo
            resumo_por_arquivo = df_consolidado.groupby('arquivo_origem').agg(
                qtd_titulos=('nosso_numero', 'count'),
                valor_total=('valor_principal', 'sum')
            ).reset_index()
            
            resumo_por_arquivo.to_excel(writer, sheet_name='Resumo_por_Arquivo', index=False)
            
            # Criar resumo geral
            dados_resumo = {
                'Informação': [
                    'Total de Arquivos Processados',
                    'Total de Títulos',
                    'Valor Total',
                    'Data de Processamento'
                ],
                'Valor': [
                    arquivos_processados,
                    total_titulos,
                    f"R$ {valor_total:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.'),
                    datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                ]
            }
            
            pd.DataFrame(dados_resumo).to_excel(writer, sheet_name='Resumo_Geral', index=False)
            
            # Salvar o arquivo Excel
            writer.close()
            print(f"\nExcel consolidado gerado: {os.path.basename(caminho_excel_consolidado)}")
    
    # Exibir resumo do processamento
    print("\n" + "=" * 70)
    print("RESUMO DO PROCESSAMENTO")
    print("=" * 70)
    print(f"Total de arquivos encontrados: {total_arquivos}")
    print(f"Arquivos processados com sucesso: {arquivos_processados}")
    print(f"Total de títulos processados: {total_titulos}")
    print(f"Valor total dos títulos: R$ {valor_total:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.'))
    print(f"\nArquivos gerados na pasta: {pasta_saida}")
    print("=" * 70)

def main():
    print("=" * 60)
    print("PROCESSADOR EM LOTE DE ARQUIVOS CNAB 400 - BRADESCO")
    print("=" * 60)
    
    if len(sys.argv) > 1:
        diretorio = sys.argv[1]
    else:
        diretorio = input("Digite o caminho do diretório com os arquivos CNAB: ")
        
    if not os.path.isdir(diretorio):
        print(f"Diretório não encontrado: {diretorio}")
        return
    
    padrao = input("Digite o padrão dos arquivos (padrão: *.TXT): ") or "*.TXT"
    processar_lote()


if __name__ == "__main__":
    main() 