import os
import sys
import sqlite3


def get_db_path() -> str:
    if getattr(sys, "frozen", False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, "whatiwatched.db")


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            isim TEXT NOT NULL,
            kategori TEXT NOT NULL,
            durum TEXT NOT NULL,
            puan REAL,
            imdb_puani REAL,
            link TEXT,
            sezon INTEGER,
            eklenme_tarihi TEXT,
            bitirilme_tarihi TEXT,
            notlar TEXT
        )
        """
    )
    conn.commit()
    conn.close()


def add_entry(isim, kategori, durum, puan, imdb_puani, link, sezon, eklenme_tarihi, bitirilme_tarihi, notlar) -> int:
    conn = get_connection()
    cur = conn.execute(
        """
        INSERT INTO entries (isim, kategori, durum, puan, imdb_puani, link, sezon, eklenme_tarihi, bitirilme_tarihi, notlar)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (isim, kategori, durum, puan, imdb_puani, link, sezon, eklenme_tarihi, bitirilme_tarihi, notlar),
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id


def update_entry(entry_id, isim, kategori, durum, puan, imdb_puani, link, sezon, eklenme_tarihi, bitirilme_tarihi, notlar) -> None:
    conn = get_connection()
    conn.execute(
        """
        UPDATE entries
        SET isim = ?, kategori = ?, durum = ?, puan = ?, imdb_puani = ?,
            link = ?, sezon = ?, eklenme_tarihi = ?, bitirilme_tarihi = ?, notlar = ?
        WHERE id = ?
        """,
        (isim, kategori, durum, puan, imdb_puani, link, sezon, eklenme_tarihi, bitirilme_tarihi, notlar, entry_id),
    )
    conn.commit()
    conn.close()


def delete_entry(entry_id) -> None:
    conn = get_connection()
    conn.execute("DELETE FROM entries WHERE id = ?", (entry_id,))
    conn.commit()
    conn.close()


def get_entries(kategori=None, durum=None, search=None, sort_by="isim", sort_desc=False):
    query = "SELECT * FROM entries WHERE 1=1"
    params = []

    if kategori:
        query += " AND kategori = ?"
        params.append(kategori)

    if durum:
        query += " AND durum = ?"
        params.append(durum)

    if search:
        query += " AND isim LIKE ?"
        params.append(f"%{search}%")

    allowed_sort_columns = {
        "isim", "kategori", "durum", "puan", "imdb_puani",
        "eklenme_tarihi", "bitirilme_tarihi",
    }
    if sort_by not in allowed_sort_columns:
        sort_by = "isim"
    query += f" ORDER BY {sort_by} {'DESC' if sort_desc else 'ASC'}"

    conn = get_connection()
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return rows
