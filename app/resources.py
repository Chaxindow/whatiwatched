import os
import sys


def get_assets_dir() -> str:
    if getattr(sys, "frozen", False):
        base_dir = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
    else:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, "assets")


def get_icon_path() -> str:
    return os.path.join(get_assets_dir(), "icon.ico")


def get_asset_url(filename: str) -> str:
    return os.path.join(get_assets_dir(), filename).replace("\\", "/")
