from rest_framework import viewsets

from models import Classification, Species, Animal


class ClassificationViewSet(viewsets.ModelViewSet):
    model = Classification


class SpeciesViewSet(viewsets.ModelViewSet):
    model = Species

class AnimalViewSet(viewsets.ModelViewSet):
    model = Animal