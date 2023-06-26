from celery import shared_task

from .models import File
from .utils import image_compress, pdf_compress, audio_compress


def change_attr(file_id: int) -> object:
    file = File.objects.get(id=file_id)
    file.processed = True
    file.save()
    return file


@shared_task
def image_process(file_id: int) -> object:
    file_obj = File.objects.get(id=file_id)
    image_compress(file_obj.file.path)
    return change_attr(file_id)


@shared_task
def pdf_process(file_id: int) -> object:
    file_obj = File.objects.get(id=file_id)
    pdf_compress(file_obj.file.path)
    return change_attr(file_id)


@shared_task
def audio_process(file_id: int) -> object:
    file_obj = File.objects.get(id=file_id)
    new_file_path = audio_compress(file_obj.file.path)
    return change_attr(file_id, new_file_path)


# Correspondence between file type and compression processes
process_task = {
    "image/jpeg": image_process,
    "image/png": image_process,
    "application/pdf": pdf_process,
    "audio/mpeg": audio_process,
    "audio/x-wav": audio_process,
}
