STRINGS = {
    "app_title": {"tr": "WhatIWatched", "en": "WhatIWatched"},
    "search_label": {"tr": "Ara:", "en": "Search:"},
    "search_placeholder": {"tr": "İsme göre ara...", "en": "Search by name..."},
    "status_label": {"tr": "Durum:", "en": "Status:"},
    "add_button": {"tr": "Yeni Ekle", "en": "Add New"},
    "filter_all": {"tr": "Tümü", "en": "All"},

    "col_name": {"tr": "İsim", "en": "Name"},
    "col_category": {"tr": "Kategori", "en": "Category"},
    "col_status": {"tr": "Durum", "en": "Status"},
    "col_rating": {"tr": "Puanım", "en": "My Rating"},
    "col_imdb": {"tr": "IMDB", "en": "IMDB"},
    "col_season": {"tr": "Sezon", "en": "Season"},
    "col_added": {"tr": "Eklenme Tarihi", "en": "Added Date"},
    "col_finished": {"tr": "Bitirme Tarihi", "en": "Finished Date"},
    "col_link": {"tr": "Link", "en": "Link"},
    "col_notes": {"tr": "Not", "en": "Notes"},

    "category.dizi": {"tr": "Dizi", "en": "TV Series"},
    "category.film": {"tr": "Film", "en": "Movie"},
    "category.anime": {"tr": "Anime", "en": "Anime"},
    "category.oyun": {"tr": "Oyun", "en": "Game"},

    "status.izledim": {"tr": "İzledim", "en": "Watched"},
    "status.izlemedim": {"tr": "İzlemedim", "en": "Not Watched"},
    "status.yarim": {"tr": "Yarım Bıraktım", "en": "Dropped"},
    "status.izliyorum": {"tr": "İzliyorum", "en": "Watching"},

    "menu_view": {"tr": "Görünüm", "en": "View"},
    "menu_theme_light": {"tr": "Açık Tema", "en": "Light Theme"},
    "menu_theme_dark": {"tr": "Koyu Tema", "en": "Dark Theme"},
    "menu_language": {"tr": "Dil", "en": "Language"},
    "menu_data": {"tr": "Veri", "en": "Data"},
    "action_export": {"tr": "Dışa Aktar...", "en": "Export..."},
    "action_import": {"tr": "İçe Aktar...", "en": "Import..."},

    "export_dialog_title": {"tr": "Verileri Dışa Aktar", "en": "Export Data"},
    "import_dialog_title": {"tr": "Verileri İçe Aktar", "en": "Import Data"},
    "export_success_title": {"tr": "Dışa Aktarma Tamamlandı", "en": "Export Complete"},
    "export_success_text": {"tr": "{count} kayıt dışa aktarıldı.", "en": "{count} entries exported."},
    "export_error_title": {"tr": "Dışa Aktarma Hatası", "en": "Export Error"},
    "export_error_text": {"tr": "Dosya yazılamadı: {error}", "en": "Could not write file: {error}"},

    "import_confirm_title": {"tr": "İçe Aktarma Onayı", "en": "Import Confirmation"},
    "import_confirm_text": {"tr": "Seçilen dosyadaki kayıtlar mevcut listeye eklenecek (üzerine yazılmayacak). Devam edilsin mi?", "en": "Entries from the selected file will be added to your current list (nothing will be overwritten). Continue?"},
    "import_success_title": {"tr": "İçe Aktarma Tamamlandı", "en": "Import Complete"},
    "import_success_text": {"tr": "{count} kayıt içe aktarıldı.", "en": "{count} entries imported."},
    "import_success_text_skipped": {"tr": "{count} kayıt içe aktarıldı, {skipped} kayıt geçersiz olduğu için atlandı.", "en": "{count} entries imported, {skipped} entries skipped (invalid)."},
    "import_error_title": {"tr": "İçe Aktarma Hatası", "en": "Import Error"},
    "import_error_text": {"tr": "Dosya okunamadı: {error}", "en": "Could not read file: {error}"},

    "dialog_title_add": {"tr": "Yeni Kayıt Ekle", "en": "Add New Entry"},
    "dialog_title_edit": {"tr": "Kaydı Düzenle", "en": "Edit Entry"},

    "field_name": {"tr": "İsim", "en": "Name"},
    "field_category": {"tr": "Kategori", "en": "Category"},
    "field_status": {"tr": "Durum", "en": "Status"},
    "field_rating": {"tr": "Puanım", "en": "My Rating"},
    "field_imdb": {"tr": "IMDB Puanı", "en": "IMDB Rating"},
    "field_link": {"tr": "Link", "en": "Link"},
    "field_season": {"tr": "Sezon", "en": "Season"},
    "field_added": {"tr": "Eklenme Tarihi", "en": "Added Date"},
    "field_finished": {"tr": "Bitirme Tarihi", "en": "Finished Date"},
    "field_notes": {"tr": "Not", "en": "Notes"},

    "placeholder_rating": {"tr": "0-10 (boş bırakılabilir)", "en": "0-10 (optional)"},

    "context_edit": {"tr": "Düzenle", "en": "Edit"},
    "context_delete": {"tr": "Sil", "en": "Delete"},

    "delete_confirm_title": {"tr": "Silme Onayı", "en": "Delete Confirmation"},
    "delete_confirm_text": {"tr": "Bu kaydı silmek istediğine emin misin?", "en": "Are you sure you want to delete this entry?"},
}

_current_lang = "tr"


def set_language(lang: str) -> None:
    global _current_lang
    if lang in ("tr", "en"):
        _current_lang = lang


def get_language() -> str:
    return _current_lang


def tr(key: str) -> str:
    entry = STRINGS.get(key)
    if entry is None:
        return key
    return entry.get(_current_lang, key)
