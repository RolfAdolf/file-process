from PIL import Image
from PyPDF2 import PdfReader, PdfWriter
from pydub import AudioSegment

import os
from pathlib import Path
from functools import partial
from typing import Callable


def _update_filename(instance, filename, path):
    """
    Dynamically sets the file name. Changes
    '*.wav' extension to '*.mp3'.
    :param instance: .models.File
        Instance of the File model object.
    :param filename: os.PathLike
        The original file name.
    :param path: os.PathLike
        The path to the directory where all
        media files are stored.
    :return: os.PathLike
        The path to the file in the media
        server directory.
    """
    path = path

    filename = Path(filename)
    if filename.suffix == ".wav":
        filename = filename.with_suffix(".mp3")

    return os.path.join(path, filename)


def upload_to(media_dir_path: os.PathLike) -> Callable:
    return partial(_update_filename, path=media_dir_path)


def image_compress(image_file):
    """
    Compresses the given image and rewrite
    the original image file. For more details
    check the
    https://pillow.readthedocs.io/en/stable/.
    :param image_file: os.PathLike
        The path to the source image file
        to be compressed.
    :return: os.PathLike
        The path to the compressed image file
        to be compressed.
    """
    image = Image.open(image_file)

    image.save(
        image_file,
        "JPEG",
        optimize=True,
        quality=10,
    )

    return image_file


def pdf_compress(pdf_file):
    """
    Compresses the given '.pdf' and rewrite
    the original file. For more details
    check the
    https://pypdf2.readthedocs.io/en/latest/.
    :param pdf_file: os.PathLike
        The path to the source pdf file
        to be compressed.
    :return: os.PathLike
        The path to the compressed pdf file
        to be compressed.
    """
    reader = PdfReader(pdf_file)
    writer = PdfWriter()

    for page in reader.pages:
        page.compress_content_streams()
        writer.add_page(page)

    with open(pdf_file, "wb") as f:
        writer.write(f)

    return pdf_file


def audio_compress(audio_file):
    """
    Compresses the given audio and rewrite
    the original file. Changes the '.wav'
    extension to the '.mp3'. For more
    details check the
    https://github.com/jiaaro/pydub.
    :param audio_file: os.PathLike
        The path to the source audio file
        to be compressed.
    :return: os.PathLike
        The path to the compressed pdf file
        to be compressed.
    """
    sound = AudioSegment.from_file(audio_file)
    sound.export(audio_file, format="mp3", bitrate="92k")

    audio_file = Path(audio_file)
    new_audio_file = audio_file.rename(audio_file.with_suffix(".mp3"))

    return new_audio_file
