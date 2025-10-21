# push_with_gh.py
import subprocess
import os
import sys

repo_name = "mais-sabiamente"        # nome no GitHub
visibility = "public"               # 'private' se quiser
commit_msg = "Initial commit from script"

def sh(cmd):
    print("> " + " ".join(cmd))
    subprocess.check_call(cmd)

def main():
    # 1) git init, add, commit
    if not os.path.exists(".git"):
        sh(["git", "init"])
    sh(["git", "add", "--all"])
    sh(["git", "commit", "-m", commit_msg])

    # 2) create remote repo and push via gh (requires gh auth)
    # this will ask GH to create and push
    sh(["gh", "repo", "create", repo_name, "--" + visibility, "--source=.", "--remote=origin", "--push"])

if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as e:
        print("Erro:", e)
        sys.exit(1)
#!/usr/bin/env python3
# scripts/relatorio.py
"""
Gera um relatório CSV local e (opcional) envia para:
 - Google Sheets (cria/atualiza uma planilha)
 - Google Drive (faz upload do CSV para uma pasta específica)
Uso:
  python scripts/relatorio.py --out relatorio_site.csv --sheet-title "Relatorio Pitbull" --drive-folder-id YOUR_FOLDER_ID
Credenciais:
 - Leia GOOGLE_SA_JSON (conteúdo do service account JSON) ou passe path via GOOGLE_SA_FILE
"""
import os
import json
import argparse
import pandas as pd
from datetime import datetime

# libs google:
# pip install gspread google-auth google-api-python-client google-auth-httplib2 google-auth-oauthlib

def load_sa_credentials():
    # 1) prefer env var (raw JSON or base64) -> GOOGLE_SA_JSON
    raw = os.environ.get("GOOGLE_SA_JSON")
    if raw:
        try:
            # se estiver base64, detecta e decodifica
            if raw.strip().startswith("{"):
                info = json.loads(raw)
            else:
                import base64
                info = json.loads(base64.b64decode(raw).decode("utf-8"))
            return info
        except Exception as e:
            raise RuntimeError("Falha ao processar GOOGLE_SA_JSON: " + str(e))

    # 2) fallback para arquivo no disco (GOOGLE_SA_FILE)
    path = os.environ.get("GOOGLE_SA_FILE") or "./google-service-account.json"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    raise RuntimeError("Nenhuma credencial encontrada. Defina GOOGLE_SA_JSON (env) ou GOOGLE_SA_FILE (path)")

def create_sample_df():
    # Substitua pela extração real de dados que você já usa
    now = datetime.utcnow().isoformat(sep=" ", timespec="seconds")
    data = [
        {"id": 1, "evento": "Ataque relatado", "local": "Zona A", "data": now, "fonte": "G1"},
        {"id": 2, "evento": "Ataque relatado", "local": "Zona B", "data": now, "fonte": "G1"}
    ]
    df = pd.DataFrame(data)
    return df

def save_csv(df, out_path):
    df.to_csv(out_path, index=False, encoding="utf-8-sig")
    print("CSV salvo em:", out_path)

def upload_to_gsheet(sa_info, df, sheet_title="Relatorio", share_with_email=None):
    import gspread
    from google.oauth2.service_account import Credentials

    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive.file',
        'https://www.googleapis.com/auth/drive'
    ]
    creds = Credentials.from_service_account_info(sa_info, scopes=scopes)
    gc = gspread.authorize(creds)

    # cria planilha (ou abre se já existir por título)
    try:
        sh = gc.open(sheet_title)
        print("Planilha existente aberta:", sheet_title)
    except gspread.SpreadsheetNotFound:
        sh = gc.create(sheet_title)
        print("Planilha criada:", sheet_title)

    # seleciona primeira worksheet (overwrite)
    try:
        ws = sh.sheet1
        ws.clear()
    except Exception:
        ws = sh.add_worksheet(title="Sheet1", rows="100", cols="20")

    # envia df
    rows = [df.columns.tolist()] + df.values.tolist()
    ws.update(rows, value_input_option="USER_ENTERED")
    print("Dados enviados para planilha:", sheet_title)

    if share_with_email:
        sh.share(share_with_email, perm_type='user', role='reader')
        print("Compartilhado com:", share_with_email)

    return sh.url, sh.id

def upload_file_to_drive(sa_info, file_path, drive_folder_id=None):
    # faz upload de um arquivo para o Drive (pasta opcional)
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    from google.oauth2.service_account import Credentials

    scopes = ['https://www.googleapis.com/auth/drive.file', 'https://www.googleapis.com/auth/drive']
    creds = Credentials.from_service_account_info(sa_info, scopes=scopes)
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {"name": os.path.basename(file_path)}
    if drive_folder_id:
        file_metadata["parents"] = [drive_folder_id]

    media = MediaFileUpload(file_path, mimetype='text/csv', resumable=True)
    created = service.files().create(body=file_metadata, media_body=media, fields='id, webViewLink').execute()
    print("Arquivo enviado ao Drive. id:", created.get("id"))
    return created

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="relatorio_site.csv", help="Caminho do CSV de saída")
    parser.add_argument("--sheet-title", default=None, help="Se setado, cria/atualiza planilha com esse título")
    parser.add_argument("--drive-folder-id", default=None, help="Se setado, faz upload do CSV para essa pasta do Drive")
    args = parser.parse_args()

    # gera df (troque por sua lógica)
    df = create_sample_df()
    save_csv(df, args.out)

    # tentar integrar com Google (se houver credencial)
    try:
        sa_info = load_sa_credentials()
        if args.sheet_title:
            url, sheet_id = upload_to_gsheet(sa_info, df, sheet_title=args.sheet_title, share_with_email=None)
            print("Planilha URL:", url, "id:", sheet_id)
        if args.drive_folder_id:
            res = upload_file_to_drive(sa_info, args.out, drive_folder_id=args.drive_folder_id)
            print("Drive link:", res.get("webViewLink", "N/A"))
    except Exception as e:
        print("Google integration skipped / failed:", e)

if __name__ == "__main__":
    main()
import subprocess, os
proj = r"C:\Users\Patty\Desktop\NovoSiteWork"
subprocess.run(["code", proj], check=False)

