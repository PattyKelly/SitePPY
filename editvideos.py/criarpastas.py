import os
from datetime import datetime, timedelta

def create_folders(base_path, start_date, end_date):
    # Criar pasta do ano
    year = start_date.year
    year_folder = os.path.join(base_path, str(year))
    os.makedirs(year_folder, exist_ok=True)

    current_date = start_date
    while current_date <= end_date:
        # Criar a pasta do dia dentro da pasta do ano (exemplo: 2025/2025-01-07)
        day_folder = os.path.join(year_folder, current_date.strftime("%Y-%m-%d"))
        os.makedirs(day_folder, exist_ok=True)

        # Criar subpastas (Legenda, Music, Video)
        subfolders = ["Legenda", "Music", "Video"]
        for subfolder in subfolders:
            os.makedirs(os.path.join(day_folder, subfolder), exist_ok=True)

        print(f"Pastas criadas para o dia: {current_date.strftime('%Y-%m-%d')}")
        current_date += timedelta(days=1)

    # Criar pasta "Prontos" com a data atual no formato dd-mm-aaaa
    prontos_folder = os.path.join(year_folder, f"Prontos_{datetime.now().strftime('%d-%m-%Y')}")
    os.makedirs(prontos_folder, exist_ok=True)
    print(f"Pasta 'Prontos' criada: {prontos_folder}")

# Exemplo de uso
base_path = r"C:\Users\Patty\Desktop\YT\BEFREE\Automatic"
start_date = datetime(2025, 1, 7)  # Data de início
end_date = datetime(2025, 1, 25)   # Data de término
create_folders(base_path, start_date, end_date)
