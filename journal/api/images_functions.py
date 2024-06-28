"""Functions to manage images"""
import shutil
from pathlib import Path

from journal.api.constants_api import IMAGES_FOLDER


def copy_image(source_path: str | Path) -> Path:
    """Copies an image to the application Images folder"""
    destination_path = IMAGES_FOLDER / Path(source_path).name
    IMAGES_FOLDER.mkdir(parents=True, exist_ok=True)
    shutil.copy(source_path, destination_path)
    return destination_path


def delete_image(image: str) -> None:
    """Deletes an image from the application Images folder"""
    # TODO
    pass
