import json

from app import db
from app.models import CATEGORIES, STATUSES

EXPORT_FIELDS = [
    "isim", "kategori", "durum", "puan", "imdb_puani", "link",
    "sezon", "eklenme_tarihi", "bitirilme_tarihi", "notlar",
]


def export_to_json(file_path: str) -> int:
    entries = db.get_entries()
    data = [{field: entry[field] for field in EXPORT_FIELDS} for entry in entries]
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return len(data)


def import_from_json(file_path: str) -> tuple[int, int]:
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("invalid format")

    imported = 0
    skipped = 0
    for item in data:
        if not isinstance(item, dict):
            skipped += 1
            continue
        isim = (item.get("isim") or "").strip()
        kategori = item.get("kategori")
        durum = item.get("durum")
        if not isim or kategori not in CATEGORIES or durum not in STATUSES:
            skipped += 1
            continue
        db.add_entry(
            isim,
            kategori,
            durum,
            item.get("puan"),
            item.get("imdb_puani"),
            item.get("link"),
            item.get("sezon"),
            item.get("eklenme_tarihi"),
            item.get("bitirilme_tarihi"),
            item.get("notlar"),
        )
        imported += 1

    return imported, skipped
