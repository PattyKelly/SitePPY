import feedparser
import csv
from rapidfuzz import fuzz

# URL do feed RSS do G1 para a seção Brasil
rss_url = "https://g1.globo.com/rss/g1/brasil/"

# Faz o parse do feed RSS
feed = feedparser.parse(rss_url)

# Verifica se ocorreu algum erro durante o parse
if feed.bozo:
    print("Erro ao fazer parse do feed RSS:", feed.bozo_exception)
    exit()

# Lista de palavras-chave para filtrar as notícias
keywords = ["mal subito", "mal - súbito", "desmaio", "acidente súbito"]

# Função que verifica se um texto contém alguma palavra similar
def contains_similar(text, keywords, threshold=70):
    text_lower = text.lower()
    for keyword in keywords:
        # Utiliza o fuzzy matching para checar a similaridade parcial
        if fuzz.partial_ratio(text_lower, keyword.lower()) >= threshold:
            return True
    return False

# Filtra as entradas verificando similaridade no título ou no resumo
filtered_entries = [
    entry for entry in feed.entries
    if contains_similar(entry.title, keywords) or 
       ('summary' in entry and contains_similar(entry.summary, keywords))
]

# Processa as entradas filtradas para extrair dia, mês e ano utilizando 'published_parsed'
report_data = []
for entry in filtered_entries:
    dia = mes = ano = None
    published = entry.get('published_parsed')
    if published:
        try:
            dia = published.tm_mday
            mes = published.tm_mon
            ano = published.tm_year
        except Exception as e:
            print("Erro ao processar data da notícia:", e)
    else:
        print(f"A notícia '{entry.title}' não possui data publicada.")
    
    report_data.append({
        'titulo': entry.title,
        'url': entry.link,
        'dia': dia,
        'mes': mes,
        'ano': ano
    })

# Define o caminho completo para salvar o arquivo CSV
if report_data:
    nome_arquivo = r"C:\Users\Patty\Desktop\PY\relatorio_site.csv"
    try:
        with open(nome_arquivo, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['titulo', 'url', 'dia', 'mes', 'ano']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in report_data:
                writer.writerow(row)
        print(f"Relatório gerado com sucesso: {nome_arquivo}")
    except Exception as e:
        print("Erro ao gerar o arquivo CSV:", e)
else:
    print("Nenhuma notícia contendo as palavras-chave foi encontrada no feed.")
