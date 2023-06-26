from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls.exceptions import NoReverseMatch
from django.core.exceptions import ObjectDoesNotExist

from pathlib import Path

from files.models import File


test_media_storage = Path("media/samples/")
test_upload_media_storage = Path("media/files/")

test_files = (
    ("file_example_JPEG_4MB.jpeg", "image/jpeg"),
    ("file_example_MP3_5MG.mp3", "audio/mpeg"),
    ("file_example_PDF_15MB.pdf", "application/pdf"),
    ("file_example_PNG_3MB.png", "image/png"),
    ("file_example_WAV_10MG.wav", "audio/x-wav"),
)


class ListRetrieveAPITests(APITestCase):
    def setUp(self):
        for test_file in test_files:
            file = SimpleUploadedFile(
                test_file[0],
                open(test_media_storage / test_file[0], "rb").read(),
                content_type=test_file[1],
            )
            File.objects.create(file=file)

    def test_files_list(self):
        response = self.client.get(reverse("files_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

    def test_file_retrieve(self):
        response = self.client.get(reverse("get_file", args=(1,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], 1)

    def test_invalid_retrieve(self):
        response = self.client.get(reverse("get_file", args=(6,)))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        some_wrong_url = "doesnt_exist_lasjfkasjfkasjkcxnw_123"

        with self.assertRaises(NoReverseMatch):
            response = self.client.get(reverse("get_file", args=(some_wrong_url,)))

        with self.assertRaises(NoReverseMatch):
            response = self.client.get(reverse("files_list", args=(some_wrong_url,)))


class UploadAPITests(APITestCase):
    def test_valid_upload(self):
        ids = []
        for test_file in test_files:
            file = SimpleUploadedFile(
                test_file[0],
                open(test_media_storage / test_file[0], "rb").read(),
                content_type=test_file[1],
            )
            response = self.client.post(reverse("upload_file"), {"file": file})
            ids.append(response.data["id"])

        for i in ids:
            try:
                file_obj = File.objects.get(id=i)
            except ObjectDoesNotExist:
                self.fail(
                    f"There is no object with id {i} in database."
                    f"Probably {test_files[i-1]}"
                )

    def test_invalid_upload(self):
        wrong_type_file = SimpleUploadedFile(
            "wrong_type.txt",
            b"Content of the file with wrong type",
            content_type="text/plain",
        )
        response = self.client.post(reverse("upload_file"), {"file": wrong_type_file})
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
