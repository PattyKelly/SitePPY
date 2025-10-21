import os
import random
import datetime

# ===== 1. Lista de temas =====
temas = [
    "chuva", "avião", "vento", "trem", "gato", "cachorro", "mar", "floresta",
    "pássaros", "fogueira", "rio", "neve caindo", "grilos à noite", "campo",
    "cachoeira", "praia", "cidade à noite", "ferramentas de oficina", "relógio"
]
# Sorteia o tema do dia
tema_do_dia = random.choice(temas)

# ===== 2. Monta o caminho organizado =====
hoje = datetime.datetime.now()
nome_dia = f"Day {hoje.day:02d}-{hoje.month:02d}-{hoje.year}"
caminho_pasta = os.path.join(
    r"C:\Users\Patty\Desktop\Videos Automatics PY\Automatic Day",
    nome_dia,
    tema_do_dia
)
os.makedirs(caminho_pasta, exist_ok=True)
print(f"\nPasta criada (ou já existente): {caminho_pasta}")

# ===== 3. Mock do próximo passo: salvar arquivo de log =====
arquivo_log = os.path.join(caminho_pasta, "log.txt")
with open(arquivo_log, "w", encoding="utf-8") as f:
    f.write(f"Tema do dia: {tema_do_dia}\n")
    f.write(f"Data: {hoje.strftime('%d/%m/%Y')}\n")
print(f"Arquivo de log salvo em: {arquivo_log}")

# Aqui você pode colocar os próximos passos, como:
# - Baixar vídeos e músicas do tema do dia para caminho_pasta
# - Concatenar vídeos, montar vídeo final, etc.
