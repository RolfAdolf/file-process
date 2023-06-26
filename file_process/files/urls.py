from django.urls import path

from . import views


urlpatterns = [
    path(
        "files/",
        views.FilesViewSet.as_view({"get": "list"}),
        name="files_list",
    ),
    path(
        "upload/",
        views.FilesViewSet.as_view({"post": "create"}),
        name="upload_file",
    ),
    path(
        "files/<int:pk>/",
        views.FilesViewSet.as_view({"get": "retrieve"}),
        name="get_file",
    ),
]
