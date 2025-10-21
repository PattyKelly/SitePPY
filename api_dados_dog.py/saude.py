import requests
import json
import urllib3

# Desabilita avisos de conexão insegura
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_swagger(url):
    """
    Busca o JSON do Swagger a partir da URL.
    Retorna o dicionário Python ou None em caso de erro.
    """
    try:
        response = requests.get(url, verify=False)
        if response.status_code == 200:
            return response.json()
        else:
            print("Erro ao buscar o swagger.json. Status code:", response.status_code)
            return None
    except Exception as e:
        print("Erro durante a requisição:", e)
        return None

def display_api_info(swagger_data):
    """Exibe informações gerais da API."""
    info = swagger_data.get("info", {})
    print("=== Informações Gerais da API ===")
    print("Título      :", info.get("title", "N/A"))
    print("Descrição   :", info.get("description", "N/A"))
    print("Versão      :", info.get("version", "N/A"))
    if "contact" in info:
        print("Contato     :", info.get("contact"))
    if "termsOfService" in info:
        print("Termos de Serviço:", info.get("termsOfService"))
    print("=" * 60)

def display_paths(swagger_data):
    """Lista os endpoints (paths) com seus métodos e detalhes."""
    paths = swagger_data.get("paths", {})
    if not paths:
        print("Nenhum endpoint encontrado.")
        return

    print("=== Endpoints da API ===")
    for path in sorted(paths.keys()):
        print(f"\nEndpoint: {path}")
        methods = paths[path]
        for method in sorted(methods.keys()):
            details = methods[method]
            print(f"  Método: {method.upper()}")
            if details.get("summary"):
                print("    Sumário    :", details["summary"])
            if details.get("description"):
                print("    Descrição  :", details["description"])
            if details.get("parameters"):
                print("    Parâmetros:")
                for param in details["parameters"]:
                    name = param.get("name", "N/A")
                    param_in = param.get("in", "N/A")
                    desc = param.get("description", "Sem descrição")
                    print(f"      - {name} (in: {param_in}): {desc}")
            print("  " + "-" * 40)
    print("=" * 60)

def display_definitions(swagger_data):
    """Exibe os modelos (definitions) presentes na API."""
    definitions = swagger_data.get("definitions", {})
    if definitions:
        print("=== Modelos (Definitions) da API ===")
        for model_name in sorted(definitions.keys()):
            print(f"\nModelo: {model_name}")
            print(json.dumps(definitions[model_name], indent=4, ensure_ascii=False))
            print("-" * 40)
    else:
        print("Nenhuma definição (model) encontrada.")
    print("=" * 60)

def display_swagger_structure(url):
    """Executa a busca e exibe os dados de forma macro-organizada."""
    swagger_data = fetch_swagger(url)
    if swagger_data:
        display_api_info(swagger_data)
        display_paths(swagger_data)
        display_definitions(swagger_data)
    else:
        print("Não foi possível obter os dados da API.")

if __name__ == "__main__":
    swagger_url = "https://apidadosabertos.saude.gov.br/static/swagger.json"
    display_swagger_structure(swagger_url)
