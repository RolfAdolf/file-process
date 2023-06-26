from django.db import models

from .utils import upload_to, _update_filename


class File(models.Model):
    file = models.FileField(upload_to=upload_to("files"))
    processed = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
