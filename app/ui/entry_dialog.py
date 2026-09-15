from PySide6.QtCore import QDate
from PySide6.QtGui import QDoubleValidator
from PySide6.QtWidgets import (
    QAbstractSpinBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QSpinBox,
    QTextEdit,
    QVBoxLayout,
)

from app.i18n import tr
from app.models import CATEGORIES, CATEGORIES_WITH_SEASON, CATEGORIES_WITHOUT_IMDB, STATUSES
from app.ui.date_field import DateField

NO_DATE = QDate(2000, 1, 1)
DATE_MIN = QDate(2000, 1, 1)
DATE_MAX = QDate(2100, 12, 31)


class EntryDialog(QDialog):
    def __init__(self, parent=None, entry=None):
        super().__init__(parent)
        self.entry = entry
        self.setWindowTitle(tr("dialog_title_edit") if entry else tr("dialog_title_add"))
        self.setMinimumWidth(420)

        self.isim_input = QLineEdit()

        self.kategori_input = QComboBox()
        for key in CATEGORIES:
            self.kategori_input.addItem(tr(f"category.{key}"), key)
        self.kategori_input.currentIndexChanged.connect(self._update_field_visibility)

        self.durum_input = QComboBox()
        for key in STATUSES:
            self.durum_input.addItem(tr(f"status.{key}"), key)

        double_validator = QDoubleValidator(0.0, 10.0, 1)
        double_validator.setNotation(QDoubleValidator.StandardNotation)

        self.puan_input = QLineEdit()
        self.puan_input.setValidator(double_validator)
        self.puan_input.setPlaceholderText(tr("placeholder_rating"))

        self.imdb_input = QLineEdit()
        self.imdb_input.setValidator(double_validator)
        self.imdb_input.setPlaceholderText(tr("placeholder_rating"))

        self.link_input = QLineEdit()
        self.link_input.setPlaceholderText("https://...")

        self.sezon_input = QSpinBox()
        self.sezon_input.setRange(0, 100)
        self.sezon_input.setSpecialValueText("—")
        self.sezon_input.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.eklenme_input = DateField()
        self.eklenme_input.setDisplayFormat("yyyy-MM-dd")
        self.eklenme_input.setDateRange(DATE_MIN, DATE_MAX)
        self.eklenme_input.setSpecialValueText("—")
        self.eklenme_input.setDate(QDate.currentDate())

        self.bitirilme_input = DateField()
        self.bitirilme_input.setDisplayFormat("yyyy-MM-dd")
        self.bitirilme_input.setDateRange(DATE_MIN, DATE_MAX)
        self.bitirilme_input.setSpecialValueText("—")
        self.bitirilme_input.setDate(NO_DATE)

        self.not_input = QTextEdit()
        self.not_input.setFixedHeight(80)

        form = QFormLayout()
        form.addRow(f"{tr('field_name')} *", self.isim_input)
        form.addRow(f"{tr('field_category')} *", self.kategori_input)
        form.addRow(f"{tr('field_status')} *", self.durum_input)
        form.addRow(tr("field_rating"), self.puan_input)
        self.imdb_label = tr("field_imdb")
        form.addRow(self.imdb_label, self.imdb_input)
        form.addRow(tr("field_link"), self.link_input)
        self.sezon_label = tr("field_season")
        form.addRow(self.sezon_label, self.sezon_input)
        form.addRow(tr("field_added"), self.eklenme_input)
        form.addRow(tr("field_finished"), self.bitirilme_input)
        form.addRow(tr("field_notes"), self.not_input)
        self.form = form

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.button(QDialogButtonBox.Ok).setText(tr("button_ok"))
        buttons.button(QDialogButtonBox.Cancel).setText(tr("button_cancel"))
        buttons.accepted.connect(self._on_accept)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(buttons)
        self.setLayout(layout)

        if entry:
            self._load_entry(entry)
        else:
            self._update_field_visibility()

    def _update_field_visibility(self) -> None:
        kategori = self.kategori_input.currentData()
        season_visible = kategori in CATEGORIES_WITH_SEASON
        self.sezon_input.setVisible(season_visible)
        self.form.labelForField(self.sezon_input).setVisible(season_visible)

        imdb_visible = kategori not in CATEGORIES_WITHOUT_IMDB
        self.imdb_input.setVisible(imdb_visible)
        self.form.labelForField(self.imdb_input).setVisible(imdb_visible)
        if not imdb_visible:
            self.imdb_input.clear()

    def _load_entry(self, entry) -> None:
        self.isim_input.setText(entry["isim"])
        self.kategori_input.setCurrentIndex(self.kategori_input.findData(entry["kategori"]))
        self.durum_input.setCurrentIndex(self.durum_input.findData(entry["durum"]))
        self.puan_input.setText("" if entry["puan"] is None else str(entry["puan"]))
        self.imdb_input.setText("" if entry["imdb_puani"] is None else str(entry["imdb_puani"]))
        self.link_input.setText(entry["link"] or "")
        self.sezon_input.setValue(entry["sezon"] or 0)
        self.eklenme_input.setDate(
            QDate.fromString(entry["eklenme_tarihi"], "yyyy-MM-dd") if entry["eklenme_tarihi"] else NO_DATE
        )
        self.bitirilme_input.setDate(
            QDate.fromString(entry["bitirilme_tarihi"], "yyyy-MM-dd") if entry["bitirilme_tarihi"] else NO_DATE
        )
        self.not_input.setPlainText(entry["notlar"] or "")
        self._update_field_visibility()

    def _on_accept(self) -> None:
        if not self.isim_input.text().strip():
            self.isim_input.setFocus()
            return
        self.accept()

    def get_values(self) -> dict:
        kategori = self.kategori_input.currentData()
        puan_text = self.puan_input.text().strip()
        imdb_text = self.imdb_input.text().strip()
        eklenme_date = self.eklenme_input.date()
        bitirilme_date = self.bitirilme_input.date()
        return {
            "isim": self.isim_input.text().strip(),
            "kategori": kategori,
            "durum": self.durum_input.currentData(),
            "puan": float(puan_text) if puan_text else None,
            "imdb_puani": float(imdb_text) if (imdb_text and kategori not in CATEGORIES_WITHOUT_IMDB) else None,
            "link": self.link_input.text().strip() or None,
            "sezon": self.sezon_input.value() if kategori in CATEGORIES_WITH_SEASON and self.sezon_input.value() > 0 else None,
            "eklenme_tarihi": eklenme_date.toString("yyyy-MM-dd") if eklenme_date != NO_DATE else None,
            "bitirilme_tarihi": bitirilme_date.toString("yyyy-MM-dd") if bitirilme_date != NO_DATE else None,
            "notlar": self.not_input.toPlainText().strip() or None,
        }
