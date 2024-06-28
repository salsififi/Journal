"""Contains MainWindow class"""
import sys
from functools import wraps
from pathlib import Path
from typing import Callable

from PySide6.QtCore import Qt, QLocale, QDate
from PySide6.QtGui import QIcon, QFont, QTextCharFormat, QAction, QKeySequence, QColor, QIntValidator
from PySide6.QtWidgets import QMainWindow, QSplitter, QCalendarWidget, QPushButton, QWidget, QLabel, \
    QVBoxLayout, QHBoxLayout, QToolBar, QFileDialog, QComboBox, QMessageBox

from journal.api.daily_note import DailyNote, get_notes, delete_all_notes
from journal.api.images_functions import copy_image
from journal.ui.CustomTextEdit import CustomTextEdit
from journal.ui.constants_ui import *


class MainWindow(QMainWindow):
    """Main window"""

    def __init__(self, app) -> None:
        super().__init__()
        self.app = app
        self.resize(1000, 600)

        self.setup_ui()
        self.color_dates()
        self.display_note()

    # region UI setup
    def setup_ui(self) -> None:
        """Sets up the UI"""
        self.create_widgets()
        self.create_actions()
        self.create_layouts()
        self.modify_widgets()
        self.add_widgets_to_layouts()
        self.setup_connections()

    def create_widgets(self) -> None:
        """Creates the UI widgets"""
        # splitter
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.wid_sidebar = QWidget()
        self.wid_notes = QWidget()

        # left sidebar
        self.btn_toggle_sidebar = QPushButton("<")
        self.calendar = QCalendarWidget()
        self.btn_search = QPushButton(QIcon(ICON_SEARCH), "")

        # notes zone
        self.toolbar = QToolBar()
        self.lbl_date = QLabel()
        self.te_notes = CustomTextEdit()
        self.cmb_font_size = QComboBox()

        # menu
        self.file_menu = self.menuBar().addMenu("Fichier")

    def create_actions(self) -> None:
        """Adds actions to notes zone toolbar and menu"""
        self.act_bold = self.toolbar.addAction(QIcon(ICON_BOLD), "Gras")
        self.act_italic = self.toolbar.addAction(QIcon(ICON_ITALIC), "Italique")
        self.act_underline = self.toolbar.addAction(QIcon(ICON_UNDERLINE), "Souligné")
        self.act_strikethrough = self.toolbar.addAction(QIcon(ICON_STRIKETHROUGH), "Barré")
        self.toolbar.addSeparator()
        self.act_copy = self.toolbar.addAction(QIcon(ICON_COPY), "Copier")
        self.act_paste = self.toolbar.addAction(QIcon(ICON_PASTE), "Coller")
        self.toolbar.addSeparator()
        self.act_decrease_font_size = self.toolbar.addAction("a-")
        self.act_increase_font_size = self.toolbar.addAction("A+")
        self.toolbar.addWidget(self.cmb_font_size)
        self.toolbar.addSeparator()
        self.act_code = self.toolbar.addAction(QIcon(ICON_CODE), "Insérer du code")
        self.act_image = self.toolbar.addAction(QIcon(ICON_IMAGE), "Inérer une image")

        self.act_quit = self.file_menu.addAction("Quitter Journal", QKeySequence("Ctrl+Q"))
        self.act_delete_all_notes = self.file_menu.addAction("Effacer toutes les notes...")

        self.toggleable_actions = [self.act_bold,
                                   self.act_italic,
                                   self.act_underline,
                                   self.act_strikethrough]

    def create_layouts(self) -> None:
        """Creates the UI layouts"""
        self.sidebar_layout = QHBoxLayout()
        self.toggle_layout = QVBoxLayout()
        self.calendar_layout = QVBoxLayout()
        self.notes_layout = QVBoxLayout()

    def modify_widgets(self) -> None:
        """Modifies the UI widgets and layouts"""
        # left sidebar
        self.wid_sidebar.setFixedWidth(WID_CALENDAR_EXPANDED_WIDTH)
        self.calendar.setVerticalHeaderFormat(QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)
        self.calendar.setFixedHeight(400)
        self.btn_toggle_sidebar.setFixedSize(20, 20)

        # notes zone
        self.lbl_date.setObjectName("lbl_date")
        self.lbl_date.setAlignment(Qt.AlignmentFlag.AlignCenter)

        for action in self.toggleable_actions:
            action.setCheckable(True)

        self.te_notes.setFontPointSize(DEFAULT_FONT_SIZE)

        self.cmb_font_size.setEditable(True)
        self.cmb_font_size.setFixedWidth(60)
        self.cmb_font_size.addItems(CMB_SIZES)
        self.cmb_font_size.setCurrentText(str(DEFAULT_FONT_SIZE))
        self.cmb_font_size.lineEdit().setValidator(QIntValidator())

        self.set_application_style()

    def add_widgets_to_layouts(self) -> None:
        """Adds widgets to the layouts"""
        # splitter
        self.setCentralWidget(self.splitter)
        self.splitter.addWidget(self.wid_sidebar)
        self.splitter.addWidget(self.wid_notes)

        # left sidebar
        self.wid_sidebar.setLayout(self.sidebar_layout)
        self.sidebar_layout.addLayout(self.calendar_layout)
        self.sidebar_layout.addLayout(self.toggle_layout)
        self.toggle_layout.addWidget(self.btn_toggle_sidebar)
        self.calendar_layout.addWidget(self.calendar)
        self.calendar_layout.addWidget(self.btn_search, alignment=Qt.AlignmentFlag.AlignRight)

        # notes zone
        self.wid_notes.setLayout(self.notes_layout)
        self.notes_layout.addWidget(self.toolbar)
        self.notes_layout.addWidget(self.lbl_date)
        self.notes_layout.addWidget(self.te_notes)

    def setup_connections(self) -> None:
        """Sets up the connections and shortcuts"""
        self.btn_toggle_sidebar.clicked.connect(self.toggle_sidebar)
        self.calendar.selectionChanged.connect(self.display_note)
        self.te_notes.textChanged.connect(self.note_changed)
        self.te_notes.selectionChanged.connect(self.update_actions_state)

        # Actions:
        for action in self.toggleable_actions:
            action.triggered.connect(self.toggle_action)
        for signal in [self.act_decrease_font_size.triggered,
                       self.act_increase_font_size.triggered,
                       self.cmb_font_size.activated,
                       self.cmb_font_size.lineEdit().returnPressed]:
            signal.connect(self.change_font_size)

        self.act_image.triggered.connect(self.insert_image)
        self.act_quit.triggered.connect(sys.exit)
        self.act_delete_all_notes.triggered.connect(self.delete_all)

    # endregion

    # region Decorators

    @staticmethod
    def modify_font(f: Callable) -> Callable:
        """Applies modifications to text_edit font based on cursor position"""

        @wraps(f)
        def wrapper(self, *args, **kwargs):
            sender = self.sender()
            cursor = self.te_notes.textCursor()
            char_format = cursor.charFormat()  # if cursor.hasSelection() else QTextCharFormat()
            res = f(self, sender, char_format, *args, **kwargs)
            self.te_notes.mergeCurrentCharFormat(char_format)
            return res

        return wrapper

    # endregion

    # region Methods for actions in alphabetical order
    @modify_font
    def change_font_size(self, sender: QAction | QWidget, char_format: QTextCharFormat, str_size: str = None) -> None:
        """Changes font size"""
        font_size = int(char_format.fontPointSize())
        if sender in (self.act_decrease_font_size, self.act_increase_font_size):
            font_size = font_size + (4 if sender == self.act_increase_font_size else -4)
            char_format.setFontPointSize(font_size)
            self.cmb_font_size.setCurrentText(str(font_size))
        elif sender in (self.cmb_font_size, self.cmb_font_size.lineEdit()):
            char_format.setFontPointSize(int(self.cmb_font_size.currentText()))
            self.te_notes.setFocus()

    def delete_all(self) -> None:
        """Deletes all notes after a warning"""
        confirm_box = QMessageBox(QMessageBox.Icon.Warning,
                                  "Du passé faisons table rase ?",
                                  DELETE_ALL_MESSAGE,
                                  buttons=(YES | NO),
                                  parent=self)
        confirm_box.setDefaultButton(NO)

        if confirm_box.exec() == YES:
            self.color_dates(delete_all=True)
            self.te_notes.clear()
            delete_all_notes()
            info_box = QMessageBox(QMessageBox.Icon.Information,
                                   "Effacement effectué",
                                   "Toutes les notes ont été effacées.",
                                   buttons=OK,
                                   parent=self)
            info_box.exec()

    def insert_image(self) -> None:
        """Opens a file dialog window to insert a file.
        If ian image is selected, copies it to the application Images folder,
        then inserts it."""
        file_dialog = QFileDialog(self, "Sélectionnez une image...",
                                  str(BASE_FOLDER),
                                  FILE_FILTER)
        if file_dialog.exec():
            selected_file = file_dialog.selectedFiles()[0]
            self.te_notes.insertHtml(f'<img src="{copy_image(selected_file)}" />')

    @modify_font
    def toggle_action(self, sender: QAction, char_format: QTextCharFormat) -> None:
        """Toggles text style based on triggered action"""
        match sender:
            case self.act_bold:
                char_format.setFontWeight(QFont.Weight.Bold if sender.isChecked() else QFont.Weight.Normal)
            case self.act_italic:
                char_format.setFontItalic(sender.isChecked())
            case self.act_underline:
                char_format.setFontUnderline(sender.isChecked())
            case self.act_strikethrough:
                char_format.setFontStrikeOut(sender.isChecked())

    def update_actions_state(self) -> None:
        """Adjusts bold, italic, underline and strikethrough action status
        based on cursor position"""
        char_format = self.te_notes.textCursor().charFormat()
        self.act_bold.setChecked(char_format.fontWeight() == QFont.Weight.Bold)
        self.act_italic.setChecked(char_format.fontItalic())
        self.act_underline.setChecked(char_format.fontUnderline())
        self.act_strikethrough.setChecked(char_format.fontStrikeOut())
        self.cmb_font_size.setCurrentText("" if self.has_different_font_sizes() else
                                          f"{int(char_format.fontPointSize())}")

    # endregion

    # region Other methods in alphabetical order
    def color_dates(self, delete_all: bool = False) -> None:
        """Applies background color to dates in calendar based on delete_all status"""
        for date in get_notes().keys():
            self.set_date_format(QDate.fromString(date, Qt.DateFormat.ISODate),
                                 BG_WHEN_EMPTY if delete_all else BG_WHEN_NOTE)

    def display_note(self):
        """Changes the date in the label when a date is selected"""
        selected_date = self.calendar.selectedDate()
        iso_date = selected_date.toString(Qt.DateFormat.ISODate)
        formatted_date = QLocale(QLocale.Language.French).toString(selected_date, "dddd d MMMM").capitalize()
        self.lbl_date.setText(formatted_date)

        # TODO: voir si possible de changer ça pour alléger le processus
        notes = get_notes()
        if notes.get(iso_date):
            self.te_notes.setText(notes[iso_date].html_content)
        else:
            self.te_notes.clear()
            self.te_notes.setFontPointSize(DEFAULT_FONT_SIZE)
            self.cmb_font_size.setCurrentText(str(DEFAULT_FONT_SIZE))
        self.set_application_style()
        self.te_notes.setFocus()

    def has_different_font_sizes(self) -> bool | None:
        """True if selection has different font sizes, False if not"""
        cursor = self.te_notes.textCursor()
        if cursor.hasSelection():
            sizes = set()
            selection_start = cursor.selectionStart()
            selection_end = cursor.selectionEnd()
            cursor.setPosition(selection_start)
            while cursor.position() < selection_end:
                cursor.movePosition(cursor.MoveOperation.NextCharacter, cursor.MoveMode.KeepAnchor)
                sizes.add(int(cursor.charFormat().fontPointSize()))
            return len(sizes) > 1

    def note_changed(self) -> None:
        """Saves note changes"""
        iso_date = self.calendar.selectedDate().toString(Qt.DateFormat.ISODate)
        note = DailyNote(date=iso_date, html_content=self.te_notes.toHtml())
        if self.te_notes.toPlainText():
            note.save_note()
            if len(self.te_notes.toPlainText()) == 1:
                self.set_date_format(self.calendar.selectedDate(), BG_WHEN_NOTE)
                self.set_application_style()
        else:
            note.delete_note()
            self.set_date_format(self.calendar.selectedDate(), BG_WHEN_EMPTY)
            self.set_application_style()

    def set_date_format(self, date: QDate, color: QColor) -> None:
        """Sets the date format based on the existence of an associated note"""
        date_format = QTextCharFormat()
        date_format.setBackground(color)
        self.calendar.setDateTextFormat(date, date_format)

    def set_application_style(self) -> None:
        """Sets the application style"""
        with open(STYLE_FILE, 'r', encoding='utf-8') as f:
            stylesheet = f.read()
            stylesheet = stylesheet.replace("{selected_date_bg_color}",
                                            BG_WHEN_NOTE_SELECTED if self.te_notes.toPlainText()
                                            else BG_WHEN_EMPTY_SELECTED)
        self.setStyleSheet(stylesheet)

    def toggle_sidebar(self):
        """Shows or hides sidebar"""
        if self.wid_sidebar.width() == WID_CALENDAR_EXPANDED_WIDTH:
            for i in range(self.calendar_layout.count()):
                self.calendar_layout.itemAt(i).widget().setVisible(False)
            self.wid_sidebar.setFixedWidth(WID_CALENDAR_COLLAPSED_WIDTH)
            self.btn_toggle_sidebar.setText(">")
        else:
            for i in range(self.calendar_layout.count()):
                self.calendar_layout.itemAt(i).widget().setVisible(True)
            self.wid_sidebar.setFixedWidth(WID_CALENDAR_EXPANDED_WIDTH)
            self.btn_toggle_sidebar.setText("<")
    # endregion
