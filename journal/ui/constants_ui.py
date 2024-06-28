"""UI constants"""

from pathlib import Path

__all__ = ['ICON_BOLD', 'ICON_ITALIC', 'ICON_UNDERLINE', 'ICON_STRIKETHROUGH',
           'ICON_CODE', 'ICON_COPY', 'ICON_PASTE', 'ICON_SEARCH', 'ICON_IMAGE',
           'WID_CALENDAR_COLLAPSED_WIDTH', 'WID_CALENDAR_EXPANDED_WIDTH',
           'DEFAULT_FONT_SIZE', 'CMB_SIZES',
           'STYLE_FILE', 'BASE_FOLDER', 'FILE_FILTER',
           'YES', 'NO', 'OK',
           'BG_WHEN_NOTE', 'BG_WHEN_EMPTY', 'BG_WHEN_NOTE_SELECTED', 'BG_WHEN_EMPTY_SELECTED',
           'DELETE_ALL_MESSAGE', ]

from PySide6.QtGui import QColor
from PySide6.QtWidgets import QMessageBox

# Icons
ICONS_FOLDER = Path(__file__).parent / "icons"
ICON_SEARCH = str(ICONS_FOLDER / "search.png")
ICON_IMAGE = str(ICONS_FOLDER / "image.png")
ICON_BOLD = str(ICONS_FOLDER / "bold.png")
ICON_UNDERLINE = str(ICONS_FOLDER / "underline.png")
ICON_ITALIC = str(ICONS_FOLDER / "italic.png")
ICON_STRIKETHROUGH = str(ICONS_FOLDER / "strikethrough.png")
ICON_CODE = str(ICONS_FOLDER / "code.png")
ICON_COPY = str(ICONS_FOLDER / "copy.png")
ICON_PASTE = str(ICONS_FOLDER / "paste.png")

# Sizes
WID_CALENDAR_EXPANDED_WIDTH = 350
WID_CALENDAR_COLLAPSED_WIDTH = 50
DEFAULT_FONT_SIZE = 16
CMB_SIZES = ["8", "10", "12", "14", "16", "18", "24", "36", "48", "72"]

# Paths
BASE_FOLDER = Path().home()
STYLE_FILE = Path(__file__).parent / "style.css"

# Images
EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]
FILE_FILTER = f"Images ({" ".join(f"*{extension}" for extension in EXTENSIONS)})"

# Box buttons
YES = QMessageBox.StandardButton.Yes
NO = QMessageBox.StandardButton.No
OK = QMessageBox.StandardButton.Ok

# Calendar background colors
BG_WHEN_EMPTY = QColor("white")
BG_WHEN_NOTE = QColor("yellow")
BG_WHEN_NOTE_SELECTED = "rgb(225, 220, 22)"
BG_WHEN_EMPTY_SELECTED = "rgb(225, 250, 250)"

# Messages
DELETE_ALL_MESSAGE = """Voulez-vous vraiment tout effacer ?
Attention, cette action est irrémédiable..."""
