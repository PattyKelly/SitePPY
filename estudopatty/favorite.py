import csv

with open(r"C:\Users\Patty\Desktop\PY\estudopatty\estudosql.csv", "r") as file:
    reader = csv.DictReader (file)
    next(reader)
    for row in reader:
        print (row ["Timestamp"])
        print (row ["genres"])
        print (row ["title"])
        titles = set()

titles = set()



import csv

titles = {}

with open (r"C:\Users\Patty\Desktop\PY\estudopatty\estudosql.csv", "r") as file:
   reader = csv.DictReader(file)

   for row in reader:
      title = row["title"].strip().upper()
      if title not in titles:
         titles[title] = 0
         titles[title] += 1

for title in sorted(titles):
   print(title, titles[title])


import csv
from cs50 import SQL

open("shows.db", "w").close()
db = SQL("sqlite:///shows.db")

db.execute("CREATE TABLE IF NOT EXISTS shows (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT)")
db.execute("CREATE TABLE IF NOT EXISTS genres (show_id INTEGER, genre TEXT, FOREIGN KEY(show_id) REFERENCES shows(id))")

with open(r"C:\Users\Patty\Desktop\PY\estudopatty\estudosql.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        title = row["title"].strip().upper()

        # Utilize o método 'execute' para inserir o título e obter o ID
        db.execute("INSERT INTO shows (title) VALUES(?)", title)

        # Obtenha o ID do último show inserido
        id = db.execute("SELECT id FROM shows ORDER BY id DESC LIMIT 1")[0]["id"] if db.execute("SELECT id FROM shows ORDER BY id DESC LIMIT 1") else None

        if id:
            genres = row["genres"].split(", ")
            for genre in genres:
                db.execute("INSERT INTO genres (show_id, genre) VALUES(?, ?)", id, genre)
