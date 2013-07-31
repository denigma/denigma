from rest_framework import viewsets

from annotations.models import Classification, Species


class ClassificationViewSet(viewsets.ModelViewSet):
    model = Classification


class SpeciesViewSet(viewsets.ModelViewSet):
    model = Species