from PySide6.QtCore import QDate, QSize, Qt, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QAbstractSpinBox,
    QCalendarWidget,
    QDateEdit,
    QHBoxLayout,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from app.theme import get_chevron_path


class _FocusDateEdit(QDateEdit):
    focusChanged = Signal(bool)

    def focusInEvent(self, event):
        super().focusInEvent(event)
        self.focusChanged.emit(True)

    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.focusChanged.emit(False)


class DateField(QWidget):
    """QComboBox ile ayni gorunume sahip, ozel bir ok butonuyla takvim acan tarih alani.

    Qt'nin QDateEdit + calendarPopup=True kombinasyonu kendi buton cercevesini QSS ile
    tam duzgun stillendirmiyor (native beveled buton kaliyor), bu yuzden native
    up/down/calendar butonlari tamamen kapatilip yerine QComboBox'takiyle birebir
    ayni QSS'i kullanan bir QToolButton eklendi.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("DateFieldContainer")
        self.setAttribute(Qt.WA_StyledBackground, True)

        self._edit = _FocusDateEdit(self)
        self._edit.setObjectName("DateFieldEdit")
        self._edit.setFrame(False)
        self._edit.setCalendarPopup(False)
        self._edit.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self._edit.focusChanged.connect(self._set_focused)

        self._button = QToolButton(self)
        self._button.setObjectName("DateFieldButton")
        self._button.setCursor(Qt.PointingHandCursor)
        self._button.setIcon(QIcon(get_chevron_path()))
        self._button.setIconSize(QSize(13, 13))
        self._button.setFocusPolicy(Qt.NoFocus)
        self._button.clicked.connect(self._toggle_calendar)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self._edit, 1)
        layout.addWidget(self._button, 0)

        self.setFixedHeight(29)

        self._calendar = QCalendarWidget()
        self._calendar.clicked.connect(self._on_date_picked)
        self._popup = QWidget(self, Qt.Popup)
        popup_layout = QVBoxLayout(self._popup)
        popup_layout.setContentsMargins(0, 0, 0, 0)
        popup_layout.addWidget(self._calendar)

        self.setProperty("focused", False)

    def _set_focused(self, focused: bool) -> None:
        self.setProperty("focused", focused)
        self.style().unpolish(self)
        self.style().polish(self)

    def _toggle_calendar(self) -> None:
        if self._popup.isVisible():
            self._popup.hide()
            return
        current = self._edit.date()
        self._calendar.setSelectedDate(current if current.isValid() else QDate.currentDate())
        pos = self.mapToGlobal(self.rect().bottomLeft())
        self._popup.move(pos)
        self._popup.show()

    def _on_date_picked(self, date: QDate) -> None:
        self._edit.setDate(date)
        self._popup.hide()

    def date(self) -> QDate:
        return self._edit.date()

    def setDate(self, date: QDate) -> None:
        self._edit.setDate(date)

    def setDateRange(self, lo: QDate, hi: QDate) -> None:
        self._edit.setDateRange(lo, hi)
        self._calendar.setDateRange(lo, hi)

    def setDisplayFormat(self, fmt: str) -> None:
        self._edit.setDisplayFormat(fmt)

    def setSpecialValueText(self, text: str) -> None:
        self._edit.setSpecialValueText(text)
