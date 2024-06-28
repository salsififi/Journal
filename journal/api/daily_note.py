"""Contains DailyNote class"""
import json
import platform
import subprocess

from journal.api.constants_api import *


class DailyNote:
    """A daily note"""

    def __init__(self, date: str, html_content: str, images: list[str, ...] = None) -> None:
        self.date = date
        self.html_content = html_content
        self.images = images

    def __str__(self) -> str:
        return f"Note {self.date}: {self.html_content:.25}{'...' if len(self.html_content) > 25 else ''}"

    def __repr__(self) -> str:
        return f"Note {self.date}"

    def delete_note(self) -> None:
        """Deletes a note file"""
        (NOTES_FOLDER / f"{self.date}.json").unlink(missing_ok=True)

    def save_note(self) -> None:
        """Saves note to a json file"""
        NOTES_FOLDER.mkdir(parents=True, exist_ok=True)
        note_path = NOTES_FOLDER / f"{self.date}.json"
        note = {"date": self.date, "html_content": self.html_content, "images": self.images}
        with open(note_path, "w", encoding="utf-8") as f:
            json.dump(note, f, indent=4)


def get_notes() -> dict[str, DailyNote]:
    """Creates a list with all non-empty daily notes"""
    # Creating and hiding folders if necessary
    NOTES_FOLDER.mkdir(parents=True, exist_ok=True)
    if platform.system() == "Windows":
        subprocess.run(['attrib', '+H', str(JOURNAL_FOLDER)])

    # Getting notes
    notes = {}
    for note_file in NOTES_FOLDER.glob("*.json"):
        with open(note_file, "r", encoding="utf-8") as f:
            note_data = json.load(f)
        date = note_data.get("date")
        notes[date] = DailyNote(date, note_data.get("html_content"), note_data.get("images"))
    return notes


def delete_all_notes() -> None:
    """Deletes all note files"""
    for note in NOTES_FOLDER.glob("*.json"):
        note.unlink()


if __name__ == '__main__':
    pass
