"""Contains CustomTextEdit class"""

from PySide6.QtCore import Qt
from PySide6.QtGui import QWheelEvent
from PySide6.QtWidgets import QTextEdit


class CustomTextEdit(QTextEdit):
    """A zoomable QTextEdit"""
    def __init__(self):
        super().__init__()
        self.image_detected_callback = None

    # TODO: À débugguer, il ne se passe rien...
    def wheelEvent(self, event: QWheelEvent):
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            if event.angleDelta().y() > 0:
                self.zoomIn(1)
            else:
                self.zoomOut(1)
            event.ignore()
        else:
            super().wheelEvent(event)

    # TODO: permettre la suppresion des images inutilisées (car effacées par l'utilisateur) du dossier Images
    def keyPressEvent(self, event):
        self.image_detected_callback = None
        if event.key() in (Qt.Key.Key_Backspace, Qt.Key.Key_Delete):
            cursor = self.textCursor()
            cursor_position = cursor.position()

            # Check if the cursor is positioned on an image
            cursor.movePosition(cursor.MoveOperation.StartOfBlock)
            while not cursor.atEnd():
                cursor.movePosition(cursor.MoveOperation.NextCharacter, cursor.MoveMode.KeepAnchor)
                if cursor.charFormat().isImageFormat():
                    image_position = cursor.position()
                    image_name = cursor.charFormat().toImageFormat().name()
                    if image_position <= cursor_position < image_position + len(image_name):
                        # Cursor is inside an image, remove it
                        cursor.removeSelectedText()
                        self.image_detected_callback = image_name
                        return

            # If cursor is not on an image, handle default behavior
            super().keyPressEvent(event)
        else:
            super().keyPressEvent(event)

    def set_image_detected_callback(self, callback: str | None) -> None:
        """Method needed to get image name when deleted"""
        self.image_detected_callback = callback

