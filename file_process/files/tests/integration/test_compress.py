from unittest import TestCase

import tempfile
import os
import shutil
from pathlib import Path

from files.utils import image_compress, audio_compress, pdf_compress


test_media_storage = Path("media/samples/")

test_files = {
    "jpeg": "file_example_JPEG_4MB.jpeg",
    "mp3": "file_example_MP3_5MG.mp3",
    "pdf": "file_example_PDF_15MB.pdf",
    "png": "file_example_PNG_3MB.png",
    "wav": "file_example_WAV_10MG.wav",
}


class CompressTest(TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()

        for test_file in os.listdir(test_media_storage):
            shutil.copy(test_media_storage / test_file, self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_image_compress(self):
        jpeg_file_path = Path(self.temp_dir.name) / test_files["jpeg"]
        png_file_path = Path(self.temp_dir.name) / test_files["png"]
        original_jpeg_size = os.path.getsize(jpeg_file_path)
        original_png_size = os.path.getsize(png_file_path)

        new_jpeg_file_path = image_compress(jpeg_file_path)
        new_png_file_path = image_compress(png_file_path)

        self.assertLess(os.path.getsize(new_jpeg_file_path), original_jpeg_size)
        self.assertLess(os.path.getsize(new_png_file_path), original_png_size)

    def test_pdf_compress(self):
        pdf_file_path = Path(self.temp_dir.name) / test_files["pdf"]

        original_pdf_size = os.path.getsize(pdf_file_path)

        new_jpeg_file_path = pdf_compress(pdf_file_path)

        self.assertLess(os.path.getsize(new_jpeg_file_path), original_pdf_size)

    def test_audio_compress(self):
        mp3_file_path = Path(self.temp_dir.name) / test_files["mp3"]
        wav_file_path = Path(self.temp_dir.name) / test_files["wav"]
        original_mp3_size = os.path.getsize(mp3_file_path)
        original_wav_size = os.path.getsize(wav_file_path)

        new_mp3_file_path = audio_compress(mp3_file_path)
        new_wav_file_path = Path(audio_compress(wav_file_path)).with_suffix(".mp3")

        self.assertLess(os.path.getsize(new_mp3_file_path), original_mp3_size)
        self.assertLess(os.path.getsize(new_wav_file_path), original_wav_size)
