from rest_framework import viewsets

from models import Classification, Species, Animal


class ClassificationViewSet(viewsets.ModelViewSet):
    """API endpoint that allows classifications be viewed or edited."""
    model = Classification


class SpeciesViewSet(viewsets.ModelViewSet):
    """API endpoint that allows species be viewed or edited."""
    model = Species


class AnimalViewSet(viewsets.ModelViewSet):
    """API endpoint that allows animals be viewed or edited."""
    model = Animal