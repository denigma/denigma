from lifespan.models import Factor, Type

from rest_framework import viewsets
from serializers import FactorSerializer


class FactorViewSet(viewsets.ModelViewSet):
    """
    API endpoit that allows users to be viewed or edited.
    """
    queryset = Factor.objects.all()
    model = Factor
    serializer_class = FactorSerializer

class TypeViewSet(viewsets.ModelViewSet):
    model = Type

