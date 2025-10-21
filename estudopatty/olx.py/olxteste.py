import requests
from bs4 import BeautifulSoup

# URL da OLX com a palavra-chave "doação" e região "Curitiba, PR"
url = "https://pr.olx.com.br/regiao-de-curitiba-e-paranagua?q=doacao"

# Faça uma solicitação para a página da OLX
response = requests.get(url)

# Verifique se a solicitação foi bem-sucedida
if response.status_code == 200:
    # Analise o conteúdo da página com BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontre os elementos relevantes (pode variar dependendo da estrutura HTML do site)
    anuncios = soup.find_all('div', class_='view')
    
    # Itere sobre os anúncios e imprima os títulos
    for anuncio in anuncios:
        titulo = anuncio.find('h2', class_='OLXad-list-title').text.strip()
        print(titulo)
else:
    print(f"Falha na solicitação. Código de status: {response.status_code}")
