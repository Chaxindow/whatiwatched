import os

from PySide6.QtCore import QSettings

from app.db import get_db_path


def _get_settings() -> QSettings:
    base_dir = os.path.dirname(get_db_path())
    path = os.path.join(base_dir, "settings.ini")
    return QSettings(path, QSettings.IniFormat)


def load_theme() -> str:
    return _get_settings().value("theme", "dark")


def save_theme(theme: str) -> None:
    _get_settings().setValue("theme", theme)


def load_language() -> str:
    return _get_settings().value("language", "tr")


def save_language(lang: str) -> None:
    _get_settings().setValue("language", lang)
