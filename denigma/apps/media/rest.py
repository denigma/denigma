from rest_framework import viewsets

from models import Image
from serializers import ImageSerializer


class ImageViewSet(viewsets.ModelViewSet):
    model = Image
    serializer_class = ImageSerializer
