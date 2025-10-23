try:
    import gspread, google, pandas, openai
    print("Imports OK: gspread, google, pandas, openai")
except Exception as e:
    print("Erro nos imports:", type(e).__name__, e)
