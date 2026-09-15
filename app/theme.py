from app.resources import get_asset_url

ACCENT = "#2f6fed"
ACCENT_DARK = "#4a90ff"

_current_theme = "dark"

LIGHT_SELECT_BG = "#cfd1d4"
LIGHT_SELECT_HOVER = "#c3c5c8"
LIGHT_SELECT_TEXT = "#16181a"
LIGHT_FOCUS_BORDER = "#9a9da2"

DARK_SELECT_BG = "#545454"
DARK_SELECT_HOVER = "#5c5c5c"
DARK_SELECT_TEXT = "#ffffff"
DARK_FOCUS_BORDER = "#8a8a8a"


def _combo_rules(border, text, popup_bg, chevron_url, select_bg, select_text, item_hover):
    return f"""
QComboBox {{
    padding-right: 30px;
}}
QComboBox::drop-down {{
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 28px;
    border-left: 1px solid {border};
    border-top-right-radius: 4px;
    border-bottom-right-radius: 4px;
    background-color: transparent;
}}
QComboBox::down-arrow {{
    image: url({chevron_url});
    width: 13px;
    height: 13px;
}}
QComboBox QAbstractItemView {{
    background-color: {popup_bg};
    color: {text};
    border: 1px solid {border};
    outline: none;
    padding: 3px;
}}
QComboBox QAbstractItemView::item {{
    padding: 5px 8px;
    border-radius: 3px;
}}
QComboBox QAbstractItemView::item:hover {{
    background-color: {item_hover};
    color: {text};
}}
QComboBox QAbstractItemView::item:selected {{
    background-color: {select_bg};
    color: {select_text};
}}

QSpinBox::up-button, QSpinBox::down-button {{
    width: 0px;
    height: 0px;
    border: none;
}}
"""


def _date_field_rules(border, bg, text, focus_border, hover):
    return f"""
QWidget#DateFieldContainer {{
    background-color: {bg};
    border: 1px solid {border};
    border-radius: 4px;
}}
QWidget#DateFieldContainer[focused="true"] {{
    border: 1px solid {focus_border};
}}
QDateEdit#DateFieldEdit {{
    background-color: transparent;
    color: {text};
    border: none;
    border-radius: 0px;
    padding: 4px 2px 4px 6px;
}}
QToolButton#DateFieldButton {{
    background-color: transparent;
    border: none;
    border-left: 1px solid {border};
    border-top-right-radius: 4px;
    border-bottom-right-radius: 4px;
    width: 27px;
    padding: 0px;
}}
QToolButton#DateFieldButton:hover {{
    background-color: {hover};
}}
"""


def _focus_rules(border_color):
    return f"""
QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QComboBox:on,
QSpinBox:focus, QDateEdit:focus {{
    border: 1px solid {border_color};
    outline: none;
}}
"""


def build_light_qss() -> str:
    chevron = get_asset_url("chevron_dark.png")
    return f"""
QWidget {{
    background-color: #f4f5f7;
    color: #16181a;
    font-size: 13px;
}}
QMainWindow, QDialog {{
    background-color: #f4f5f7;
}}
QLineEdit, QTextEdit, QComboBox, QSpinBox, QDateEdit {{
    background-color: #ffffff;
    color: #16181a;
    border: 1px solid #c2c4c8;
    border-radius: 4px;
    padding: 4px;
    selection-background-color: {LIGHT_SELECT_BG};
    selection-color: {LIGHT_SELECT_TEXT};
}}
QTableWidget {{
    background-color: #ffffff;
    color: #16181a;
    gridline-color: #dcdde0;
    alternate-background-color: #f2f3f5;
    border: 1px solid #d4d5d8;
}}
QTableWidget::item:selected {{
    background-color: {LIGHT_SELECT_BG};
    color: {LIGHT_SELECT_TEXT};
}}
QHeaderView::section {{
    background-color: #e8e9ec;
    color: #16181a;
    font-weight: 600;
    padding: 5px;
    border: none;
    border-right: 1px solid #d4d5d8;
    border-bottom: 2px solid #c2c4c8;
}}
QListWidget {{
    background-color: #ffffff;
    color: #16181a;
    border: 1px solid #c2c4c8;
    border-radius: 4px;
}}
QListWidget::item {{
    padding: 6px 8px;
    border-radius: 3px;
}}
QListWidget::item:hover {{
    background-color: #eceded;
}}
QListWidget::item:selected {{
    background-color: {LIGHT_SELECT_BG};
    color: {LIGHT_SELECT_TEXT};
}}
QListWidget::item:selected:hover {{
    background-color: {LIGHT_SELECT_HOVER};
}}
QPushButton {{
    background-color: #e8e9ec;
    color: #16181a;
    border: 1px solid #c2c4c8;
    border-radius: 4px;
    padding: 6px 14px;
    font-weight: 500;
}}
QPushButton:hover {{
    background-color: #dcdee2;
    border-color: #aeb1b6;
}}
QPushButton:pressed {{
    background-color: #cfd1d5;
}}
QMenuBar {{
    background-color: #eceef1;
    color: #16181a;
    border-bottom: 1px solid #d4d5d8;
}}
QMenuBar::item:selected {{
    background-color: {ACCENT};
    color: #ffffff;
}}
QMenu {{
    background-color: #ffffff;
    color: #16181a;
    border: 1px solid #c2c4c8;
}}
QMenu::item:selected {{
    background-color: {ACCENT};
    color: #ffffff;
}}
{_combo_rules("#c2c4c8", "#16181a", "#ffffff", chevron, LIGHT_SELECT_BG, LIGHT_SELECT_TEXT, "#e4e5e8")}
{_focus_rules(LIGHT_FOCUS_BORDER)}
{_date_field_rules("#c2c4c8", "#ffffff", "#16181a", LIGHT_FOCUS_BORDER, "#e4e5e8")}
"""


def build_dark_qss() -> str:
    chevron = get_asset_url("chevron_light.png")
    return f"""
QWidget {{
    background-color: #2b2b2b;
    color: #e0e0e0;
    font-size: 13px;
}}
QMainWindow, QDialog {{
    background-color: #2b2b2b;
}}
QLineEdit, QTextEdit, QComboBox, QSpinBox, QDateEdit {{
    background-color: #3a3a3a;
    color: #e0e0e0;
    border: 1px solid #555555;
    border-radius: 4px;
    padding: 4px;
    selection-background-color: {DARK_SELECT_BG};
    selection-color: {DARK_SELECT_TEXT};
}}
QTableWidget {{
    background-color: #333333;
    color: #e0e0e0;
    gridline-color: #4a4a4a;
    alternate-background-color: #3a3a3a;
}}
QTableWidget::item:selected {{
    background-color: {DARK_SELECT_BG};
    color: {DARK_SELECT_TEXT};
}}
QHeaderView::section {{
    background-color: #3d3d3d;
    color: #e0e0e0;
    font-weight: 600;
    padding: 5px;
    border: none;
    border-right: 1px solid #4a4a4a;
    border-bottom: 2px solid #555555;
}}
QListWidget {{
    background-color: #333333;
    color: #e0e0e0;
    border: 1px solid #4a4a4a;
    border-radius: 4px;
}}
QListWidget::item {{
    padding: 6px 8px;
    border-radius: 3px;
}}
QListWidget::item:hover {{
    background-color: #3f3f3f;
}}
QListWidget::item:selected {{
    background-color: {DARK_SELECT_BG};
    color: {DARK_SELECT_TEXT};
}}
QListWidget::item:selected:hover {{
    background-color: {DARK_SELECT_HOVER};
}}
QPushButton {{
    background-color: #3d3d3d;
    color: #e0e0e0;
    border: 1px solid #555555;
    border-radius: 4px;
    padding: 6px 14px;
    font-weight: 500;
}}
QPushButton:hover {{
    background-color: #4a4a4a;
}}
QPushButton:pressed {{
    background-color: #545454;
}}
QMenuBar {{
    background-color: #2b2b2b;
    color: #e0e0e0;
    border-bottom: 1px solid #4a4a4a;
}}
QMenuBar::item:selected {{
    background-color: {ACCENT_DARK};
    color: #ffffff;
}}
QMenu {{
    background-color: #333333;
    color: #e0e0e0;
    border: 1px solid #4a4a4a;
}}
QMenu::item:selected {{
    background-color: {ACCENT_DARK};
    color: #ffffff;
}}
{_combo_rules("#555555", "#e0e0e0", "#3a3a3a", chevron, DARK_SELECT_BG, DARK_SELECT_TEXT, "#484848")}
{_focus_rules(DARK_FOCUS_BORDER)}
{_date_field_rules("#555555", "#3a3a3a", "#e0e0e0", DARK_FOCUS_BORDER, "#484848")}
"""


def get_chevron_path() -> str:
    return get_asset_url("chevron_light.png" if _current_theme == "dark" else "chevron_dark.png")


def apply_theme(app, theme: str) -> None:
    global _current_theme
    _current_theme = theme
    app.setStyleSheet(build_dark_qss() if theme == "dark" else build_light_qss())
