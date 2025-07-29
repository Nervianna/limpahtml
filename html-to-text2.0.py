from bs4 import BeautifulSoup
import pandas as pd

# Espaçamento conforme a estrutura HTML
def preserve_spacing(tag):
    if tag.name in ['p', 'div', 'br']:
        return "\n" + tag.get_text()
    else:
        return tag.get_text()

# Limpa a sintaxe HTML do texto
def remove_html_syntax(input_html):
    # Verificar se o valor é uma string
    if isinstance(input_html, str):
        # Remover a sintaxe HTML
        soup = BeautifulSoup(input_html, 'html.parser')
        formatted_text = ''.join(preserve_spacing(tag) for tag in soup.find_all())
        return formatted_text
    else:
        return input_html  # Se não for uma string, retornar o valor original

# Ler planilha e limpar o HTML
def main():
    planilha = "teste_counter.xlsx"  # Corrigido o nome do arquivo
    aba = "Planilha1"

    df = pd.read_excel(planilha, sheet_name=aba)

    df['texto'] = df['Html'].apply(remove_html_syntax)
    print(df['texto'])

    df.to_excel(planilha, sheet_name=aba, index=False)

main()
