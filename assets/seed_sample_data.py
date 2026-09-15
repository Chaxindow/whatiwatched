"""Gercek uygulama veritabanina 10 ornek kayit ekler (tek seferlik, elle calistirilir)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import db

db.init_db()

SAMPLES = [
    ("Breaking Bad", "dizi", "izledim", 10, 9.5, "https://www.imdb.com/title/tt0903747", 5, "2024-01-10", "2024-02-01", "Efsane bir dizi."),
    ("Inception", "film", "izledim", 9, 8.8, "https://www.imdb.com/title/tt1375666", None, "2024-01-01", "2024-01-01", None),
    ("Attack on Titan", "anime", "izledim", 10, 9.0, "https://www.imdb.com/title/tt2560140", 4, "2023-11-01", "2024-01-15", "Muhtesem final."),
    ("Elden Ring", "oyun", "izledim", 10, None, "https://store.steampowered.com/app/1245620", None, "2024-03-01", "2024-04-20", "Yilin oyunu."),
    ("The Office", "dizi", "izliyorum", 8, 8.9, "https://www.imdb.com/title/tt0386676", 3, "2024-05-01", None, "Hala izliyorum."),
    ("Dune: Part Two", "film", "izlemedim", None, 8.5, "https://www.imdb.com/title/tt15239678", None, "2024-06-01", None, "Izleme listesinde."),
    ("One Piece", "anime", "izliyorum", 9, 8.7, "https://www.imdb.com/title/tt0388629", 20, "2022-01-01", None, "Uzun soluklu bir seri."),
    ("The Witcher 3", "oyun", "izledim", 10, None, "https://www.imdb.com/title/tt2140553", None, "2023-05-01", "2023-07-10", "Efsanevi RPG."),
    ("Interstellar", "film", "izledim", 10, 8.7, "https://www.imdb.com/title/tt0816692", None, "2024-02-14", "2024-02-14", None),
    ("Stranger Things", "dizi", "yarim", 6, 8.6, "https://www.imdb.com/title/tt4574334", 2, "2023-08-01", None, "Biraktim, sikici geldi."),
]

for row in SAMPLES:
    db.add_entry(*row)

print(f"{len(SAMPLES)} ornek kayit eklendi -> {db.get_db_path()}")
