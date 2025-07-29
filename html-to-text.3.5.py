import csv
import re
import html
import sys 

try:
    max_int = sys.maxsize
    while True:
        try:
            csv.field_size_limit(max_int)
            break
        except OverflowError:
            max_int = int(max_int / 10)
except:
    csv.field_size_limit(1000000) # Define um fallback de 1MB



def limpar_tags_html_css(texto_html):
    """Remove tags HTML, CSS e decodifica entidades HTML comuns de uma string."""
    if texto_html is None:
        return ""

    # 1. Decodificar entidades HTML primeiro
    texto_decodificado = html.unescape(texto_html)

    # 2. Remover tags HTML
    texto_sem_html = re.sub(r'<[^>]+>', '', texto_decodificado)
    
    # 3. Remover estilos CSS dentro de tags style
    texto_limpo = re.sub(r'<style.*?</style>', '', texto_sem_html, flags=re.DOTALL | re.IGNORECASE)
    
    # 4. Remove comentários HTML (CORRIGIDO)
    texto_limpo = re.sub(r'', '', texto_limpo, flags=re.DOTALL)

    # 5. Substituir o caractere de espaço não quebrável (\xa0) por um espaço normal.
    texto_limpo = texto_limpo.replace('\xa0', ' ')

    # 6. Remover espaços em branco extras resultantes da limpeza
    texto_limpo = ' '.join(texto_limpo.split())
    
    return texto_limpo

def processar_csv(arquivo_entrada, arquivo_saida, nome_coluna_html='html'):
    """
    Lê um arquivo CSV, limpa tags HTML/CSS e entidades de uma coluna específica
    e salva o resultado em um novo arquivo CSV.
    """
    try:
        with open(arquivo_entrada, 'r', newline='', encoding='utf-8') as csv_entrada, \
             open(arquivo_saida, 'w', newline='', encoding='utf-8') as csv_saida:

            leitor_csv = csv.reader(csv_entrada, delimiter=',')
            escritor_csv = csv.writer(csv_saida, delimiter=',')

            cabecalho = next(leitor_csv, None)
            if not cabecalho:
                print("Erro: O arquivo CSV de entrada está vazio.")
                return

            escritor_csv.writerow(cabecalho)

            try:
                indice_coluna_html = cabecalho.index(nome_coluna_html)
            except ValueError:
                print(f"Erro: A coluna '{nome_coluna_html}' não foi encontrada no cabeçalho: {cabecalho}")
                print("Colunas disponíveis:", cabecalho)
                return

            for i, linha in enumerate(leitor_csv):
                if not linha:
                    continue 
                
                linha_modificada = list(linha) 

                if len(linha_modificada) > indice_coluna_html:
                    conteudo_original = linha_modificada[indice_coluna_html]
                    linha_modificada[indice_coluna_html] = limpar_tags_html_css(conteudo_original)

                escritor_csv.writerow(linha_modificada)
        
        print(f" Arquivo processado com sucesso! Saída salva em: {arquivo_saida}")

    except FileNotFoundError:
        print(f"Erro: O arquivo de entrada '{arquivo_entrada}' não foi encontrado.")
    except csv.Error as e:
        print(f"Erro ao processar o arquivo CSV na linha {leitor_csv.line_num}: {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
    arquivo_csv_entrada = input("Digite o nome do arquivo CSV de entrada (ex: dados.csv): ")
    arquivo_csv_saida = input("Digite o nome do arquivo CSV de saída (ex: dados_limpos.csv): ")
    coluna_para_limpar = input("Digite o nome da coluna que contém o HTML (pressione Enter para usar 'html' como padrão): ")

    if not coluna_para_limpar:
        coluna_para_limpar = 'html'

    processar_csv(arquivo_csv_entrada, arquivo_csv_saida, coluna_para_limpar)