import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from app import db, settings
from app.i18n import set_language
from app.resources import get_icon_path
from app.theme import apply_theme
from app.ui.main_window import MainWindow


def main() -> None:
    db.init_db()

    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setWindowIcon(QIcon(get_icon_path()))
    apply_theme(app, settings.load_theme())
    set_language(settings.load_language())

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
