from rest_framework import viewsets

from serializers import FactorSerializer
from models import (Study, Experiment, Strain, Measurement, Epistasis,
     Comparison, Type, Regimen, Assay, Manipulation, Intervention, Factor,
     State, Technology, StudyType, Population, VariantType, ORType, Variant,
     Gender)


class StudyViewSet(viewsets.ModelViewSet):
    model = Study


class ExperimentViewSet(viewsets.ModelViewSet):
    model = Experiment


class StrainViewSet(viewsets.ModelViewSet):
    model = Strain


class MeasurementViewSet(viewsets.ModelViewSet):
    model = Measurement


class EpistasisViewSet(viewsets.ModelViewSet):
    model = Epistasis


class ComparisonViewSet(viewsets.ModelViewSet):
    model = Comparison


class TypeViewSet(viewsets.ModelViewSet):
    model = Type


class ManipulationViewSet(viewsets.ModelViewSet):
    model = Manipulation


class RegimenViewSet(viewsets.ModelViewSet):
    model = Regimen

class AssayViewSet(viewsets.ModelViewSet):
    model = Assay

class InterventionViewSet(viewsets.ModelViewSet):
    model = Intervention


class FactorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows lifespan factors to be viewed or edited.
    """
    queryset = Factor.objects.all()
    model = Factor
    serializer_class = FactorSerializer


class TypeViewSet(viewsets.ModelViewSet):
    model = Type


class StateViewSet(viewsets.ModelViewSet):
    model = State


class TechnologyViewSet(viewsets.ModelViewSet):
    model = Technology


class StudyTypeViewSet(viewsets.ModelViewSet):
    model = StudyType


class VariantTypeViewSet(viewsets.ModelViewSet):
    model = VariantType


class ORTypeViewSet(viewsets.ModelViewSet):
    model = ORType


class PopulationViewSet(viewsets.ModelViewSet):
    model = Population


class VariantViewSet(viewsets.ModelViewSet):
    model = Variant


class GenderViewSet(viewsets.ModelViewSet):
    model = Gender
