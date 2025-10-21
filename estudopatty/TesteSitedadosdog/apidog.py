import feedparser
import csv

# URL do feed RSS do G1 para a seção Brasil
rss_url = "https://g1.globo.com/rss/g1/brasil/"

# Faz o parse do feed
feed = feedparser.parse(rss_url)

# Verifica se houve erro no parse do feed
if feed.bozo:
    print("Erro ao fazer parse do feed RSS:", feed.bozo_exception)
    exit()

# Define a palavra-chave para filtrar as notícias (buscando "pitbull", sem diferenciar maiúsculas/minúsculas)
keyword = "pitbull"
filtered_entries = [
    entry for entry in feed.entries
    if keyword.lower() in entry.title.lower() or 
       ('summary' in entry and keyword.lower() in entry.summary.lower())
]

# Processa as entradas filtradas para extrair dia, mês e ano usando 'published_parsed'
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

# Gera o arquivo CSV com o relatório, se houver notícias encontradas
if report_data:
    nome_arquivo = "relatorio_site.csv"
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
    print("Nenhuma notícia contendo 'pitbull' foi encontrada no feed.")
