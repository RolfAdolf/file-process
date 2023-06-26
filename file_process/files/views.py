from rest_framework import viewsets, status
from rest_framework.response import Response
from kombu.exceptions import OperationalError

from .models import File
from .serializers import FileSerializer
from .tasks import process_task


class FilesViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all().order_by("-id")
    serializer_class = FileSerializer

    def create(self, request, *args, **kwargs):
        # Check the type's supportability
        content_type = request.FILES["file"].content_type
        try:
            compressor = process_task[content_type]
        except KeyError:
            return Response(
                data={
                    "error": f"Only {process_task.keys()} types are available for compression"
                },
                status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            )

        response = super().create(request, *args, **kwargs)

        # Create the asynchronous celery task with
        # process_task[content_type] function.
        try:
            compressor.delay(response.data.get("id"))
        except OperationalError as e:
            print("Cannot create a celery task: ", e)

        return response
