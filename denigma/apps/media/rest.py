from rest_framework import viewsets

from models import Image
from serializers import ImageSerializer


class ImageViewSet(viewsets.ModelViewSet):
    """API endpoint that allows media images be viewed or edited."""
    model = Image
    serializer_class = ImageSerializer
