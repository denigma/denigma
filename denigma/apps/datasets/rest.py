from rest_framework import viewsets

from models import Reference


class ReferenceViewSet(viewsets.ModelViewSet):
    """API endpoint that allows datasets references be viewed or edited."""
    model = Reference