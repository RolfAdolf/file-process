from rest_framework import serializers

from .models import File


class FileSerializer(serializers.ModelSerializer):
    file = serializers.FileField()
    processed = serializers.BooleanField(read_only=True)
    uploaded_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = File
        fields = "__all__"
