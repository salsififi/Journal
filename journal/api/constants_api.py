"""Constants used by the API"""

from pathlib import Path

from PySide6.QtCore import QStandardPaths

__all__ = ['JOURNAL_FOLDER',
           'NOTES_FOLDER',
           'IMAGES_FOLDER',
           'SETTINGS_FILE',]

# Paths
DOCUMENTS_FOLDER = QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation)
JOURNAL_FOLDER = Path(DOCUMENTS_FOLDER) / ".JOURNAL"
NOTES_FOLDER = JOURNAL_FOLDER / "Notes"
IMAGES_FOLDER = JOURNAL_FOLDER / "Images"
SETTINGS_FILE = JOURNAL_FOLDER / "settings.json"


if __name__ == '__main__':
    pass