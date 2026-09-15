import webbrowser

from PySide6.QtCore import Qt
from PySide6.QtGui import QActionGroup, QIcon
from PySide6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QComboBox,
    QFileDialog,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMenu,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from app import data_io, db, settings
from app.i18n import get_language, set_language, tr
from app.models import CATEGORIES, STATUSES
from app.resources import get_icon_path
from app.theme import apply_theme
from app.ui.entry_dialog import EntryDialog

COLUMN_KEYS = [
    "col_name", "col_category", "col_status", "col_rating", "col_imdb",
    "col_season", "col_added", "col_finished", "col_link", "col_notes",
]
LINK_COLUMN = 8
NOTES_COLUMN = 9


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1150, 600)
        self.setWindowIcon(QIcon(get_icon_path()))

        self._build_menu()
        self._build_ui()
        self.retranslate_ui()
        self.reload_table()

    def _build_menu(self) -> None:
        self.menu_bar = self.menuBar()
        self.view_menu = self.menu_bar.addMenu("")
        self.light_action = self.view_menu.addAction("")
        self.light_action.setCheckable(True)
        self.dark_action = self.view_menu.addAction("")
        self.dark_action.setCheckable(True)
        theme_group = QActionGroup(self)
        theme_group.setExclusive(True)
        theme_group.addAction(self.light_action)
        theme_group.addAction(self.dark_action)
        self.light_action.triggered.connect(lambda: self._change_theme("light"))
        self.dark_action.triggered.connect(lambda: self._change_theme("dark"))

        current_theme = settings.load_theme()
        self.dark_action.setChecked(current_theme == "dark")
        self.light_action.setChecked(current_theme != "dark")

        self.lang_menu = self.menu_bar.addMenu("")
        self.lang_tr_action = self.lang_menu.addAction("Türkçe")
        self.lang_tr_action.setCheckable(True)
        self.lang_en_action = self.lang_menu.addAction("English")
        self.lang_en_action.setCheckable(True)
        lang_group = QActionGroup(self)
        lang_group.setExclusive(True)
        lang_group.addAction(self.lang_tr_action)
        lang_group.addAction(self.lang_en_action)
        self.lang_tr_action.triggered.connect(lambda: self._change_language("tr"))
        self.lang_en_action.triggered.connect(lambda: self._change_language("en"))

        current_lang = get_language()
        self.lang_tr_action.setChecked(current_lang == "tr")
        self.lang_en_action.setChecked(current_lang == "en")

        self.data_menu = self.menu_bar.addMenu("")
        self.export_action = self.data_menu.addAction("")
        self.export_action.triggered.connect(self._export_data)
        self.import_action = self.data_menu.addAction("")
        self.import_action.triggered.connect(self._import_data)

    def _export_data(self) -> None:
        file_path, _ = QFileDialog.getSaveFileName(
            self, tr("export_dialog_title"), "whatiwatched_yedek.json", "JSON (*.json)"
        )
        if not file_path:
            return
        try:
            count = data_io.export_to_json(file_path)
        except OSError as e:
            QMessageBox.critical(self, tr("export_error_title"), tr("export_error_text").format(error=e))
            return
        QMessageBox.information(self, tr("export_success_title"), tr("export_success_text").format(count=count))

    def _import_data(self) -> None:
        file_path, _ = QFileDialog.getOpenFileName(self, tr("import_dialog_title"), "", "JSON (*.json)")
        if not file_path:
            return
        reply = QMessageBox.question(
            self, tr("import_confirm_title"), tr("import_confirm_text"), QMessageBox.Yes | QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return
        try:
            imported, skipped = data_io.import_from_json(file_path)
        except (OSError, ValueError) as e:
            QMessageBox.critical(self, tr("import_error_title"), tr("import_error_text").format(error=e))
            return
        if skipped:
            text = tr("import_success_text_skipped").format(count=imported, skipped=skipped)
        else:
            text = tr("import_success_text").format(count=imported)
        QMessageBox.information(self, tr("import_success_title"), text)
        self.reload_table()

    def _change_theme(self, theme: str) -> None:
        settings.save_theme(theme)
        apply_theme(QApplication.instance(), theme)

    def _change_language(self, lang: str) -> None:
        set_language(lang)
        settings.save_language(lang)
        self.retranslate_ui()
        self.reload_table()

    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)
        root_layout = QVBoxLayout(central)

        top_bar = QHBoxLayout()
        self.search_label = QLabel()
        self.search_input = QLineEdit()
        self.search_input.textChanged.connect(self.reload_table)

        self.status_label = QLabel()
        self.durum_filter = QComboBox()
        self.durum_filter.currentIndexChanged.connect(self.reload_table)

        self.add_button = QPushButton()
        self.add_button.clicked.connect(self.open_add_dialog)

        top_bar.addWidget(self.search_label)
        top_bar.addWidget(self.search_input, 2)
        top_bar.addWidget(self.status_label)
        top_bar.addWidget(self.durum_filter, 1)
        top_bar.addWidget(self.add_button)
        root_layout.addLayout(top_bar)

        body_layout = QHBoxLayout()
        root_layout.addLayout(body_layout, 1)

        self.category_list = QListWidget()
        self.category_list.setMaximumWidth(150)
        self.category_list.currentItemChanged.connect(self.reload_table)
        body_layout.addWidget(self.category_list)

        self.table = QTableWidget(0, len(COLUMN_KEYS))
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setSortingEnabled(True)
        self.table.setWordWrap(True)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(NOTES_COLUMN, QHeaderView.Stretch)
        self.table.verticalHeader().setDefaultSectionSize(32)
        self.table.cellDoubleClicked.connect(self._on_cell_double_clicked)
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self._on_context_menu)
        body_layout.addWidget(self.table, 1)

    def retranslate_ui(self) -> None:
        self.setWindowTitle(tr("app_title"))

        self.view_menu.setTitle(tr("menu_view"))
        self.light_action.setText(tr("menu_theme_light"))
        self.dark_action.setText(tr("menu_theme_dark"))
        self.lang_menu.setTitle(tr("menu_language"))
        self.data_menu.setTitle(tr("menu_data"))
        self.export_action.setText(tr("action_export"))
        self.import_action.setText(tr("action_import"))

        self.search_label.setText(tr("search_label"))
        self.search_input.setPlaceholderText(tr("search_placeholder"))
        self.status_label.setText(tr("status_label"))
        self.add_button.setText(tr("add_button"))

        selected_category = self._current_category()
        self.category_list.blockSignals(True)
        self.category_list.clear()
        all_item = QListWidgetItem(tr("filter_all"))
        all_item.setData(Qt.UserRole, None)
        self.category_list.addItem(all_item)
        for key in CATEGORIES:
            item = QListWidgetItem(tr(f"category.{key}"))
            item.setData(Qt.UserRole, key)
            self.category_list.addItem(item)
        self._select_category(selected_category)
        self.category_list.blockSignals(False)

        selected_status = self.durum_filter.currentData() if self.durum_filter.count() else None
        self.durum_filter.blockSignals(True)
        self.durum_filter.clear()
        self.durum_filter.addItem(tr("filter_all"), None)
        for key in STATUSES:
            self.durum_filter.addItem(tr(f"status.{key}"), key)
        index = self.durum_filter.findData(selected_status)
        self.durum_filter.setCurrentIndex(index if index >= 0 else 0)
        self.durum_filter.blockSignals(False)

        self.table.setHorizontalHeaderLabels([tr(key) for key in COLUMN_KEYS])

    def _select_category(self, key) -> None:
        for row in range(self.category_list.count()):
            item = self.category_list.item(row)
            if item.data(Qt.UserRole) == key:
                self.category_list.setCurrentItem(item)
                return
        self.category_list.setCurrentRow(0)

    def _current_category(self):
        item = self.category_list.currentItem()
        return item.data(Qt.UserRole) if item else None

    def reload_table(self) -> None:
        entries = db.get_entries(
            kategori=self._current_category(),
            durum=self.durum_filter.currentData() if self.durum_filter.count() else None,
            search=self.search_input.text().strip(),
        )

        self.table.setSortingEnabled(False)
        self.table.setRowCount(0)
        for row_index, entry in enumerate(entries):
            self.table.insertRow(row_index)
            self._set_item(row_index, 0, entry["isim"], entry["id"])
            self._set_item(row_index, 1, tr(f"category.{entry['kategori']}"))
            self._set_item(row_index, 2, tr(f"status.{entry['durum']}"))
            self._set_item(row_index, 3, entry["puan"])
            self._set_item(row_index, 4, entry["imdb_puani"])
            self._set_item(row_index, 5, entry["sezon"])
            self._set_item(row_index, 6, entry["eklenme_tarihi"] or "")
            self._set_item(row_index, 7, entry["bitirilme_tarihi"] or "")
            self._set_item(row_index, LINK_COLUMN, entry["link"] or "")
            self._set_item(row_index, NOTES_COLUMN, entry["notlar"] or "")
        self.table.setSortingEnabled(True)
        self.table.resizeRowsToContents()

    def _set_item(self, row: int, col: int, value, entry_id=None) -> None:
        display = "" if value is None else str(value)
        item = QTableWidgetItem(display)
        if isinstance(value, (int, float)):
            item.setData(Qt.EditRole, value)
        if entry_id is not None:
            item.setData(Qt.UserRole, entry_id)
        if display:
            item.setToolTip(display)
        self.table.setItem(row, col, item)

    def _selected_entry_id(self):
        row = self.table.currentRow()
        if row < 0:
            return None
        return self.table.item(row, 0).data(Qt.UserRole)

    def _on_cell_double_clicked(self, row: int, col: int) -> None:
        if col == LINK_COLUMN:
            link = self.table.item(row, col).text().strip()
            if link:
                webbrowser.open(link)
                return
        self.open_edit_dialog(self.table.item(row, 0).data(Qt.UserRole))

    def open_add_dialog(self) -> None:
        dialog = EntryDialog(self)
        if dialog.exec():
            values = dialog.get_values()
            db.add_entry(**values)
            self.reload_table()

    def open_edit_dialog(self, entry_id) -> None:
        entry = next((e for e in db.get_entries() if e["id"] == entry_id), None)
        if entry is None:
            return
        dialog = EntryDialog(self, entry=entry)
        if dialog.exec():
            values = dialog.get_values()
            db.update_entry(entry_id, **values)
            self.reload_table()

    def _on_context_menu(self, position) -> None:
        entry_id = self._selected_entry_id()
        if entry_id is None:
            return
        menu = QMenu(self)
        edit_action = menu.addAction(tr("context_edit"))
        delete_action = menu.addAction(tr("context_delete"))
        action = menu.exec(self.table.viewport().mapToGlobal(position))
        if action == edit_action:
            self.open_edit_dialog(entry_id)
        elif action == delete_action:
            self._confirm_delete(entry_id)

    def _confirm_delete(self, entry_id) -> None:
        reply = QMessageBox.question(
            self,
            tr("delete_confirm_title"),
            tr("delete_confirm_text"),
            QMessageBox.Yes | QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            db.delete_entry(entry_id)
            self.reload_table()
