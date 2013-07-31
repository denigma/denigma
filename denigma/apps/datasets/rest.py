from rest_framework import viewsets

from models import Reference

class ReferenceViewSet(viewsets.ModelViewSet):
    model = Reference