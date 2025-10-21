try:
    import pandas as pd
    import gspread
    import google.oauth2.service_account as sac
    import requests
    import openai
    print('OK: imports: pandas, gspread, google-auth, requests, openai')
except Exception as e:
    print('ERRO import:', e)
