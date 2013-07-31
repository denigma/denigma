from rest_framework import viewsets

from serializers import FactorSerializer
from models import (Study, Experiment, Strain, Measurement, Epistasis,
     Comparison, Type, Regimen, Assay, Manipulation, Intervention, Factor,
     State, Technology, StudyType, Population, VariantType, ORType, Variant,
     Gender)


class StudyViewSet(viewsets.ModelViewSet):
    """API endpoint that allows lifespan studies to be viewed or edited."""
    model = Study


class ExperimentViewSet(viewsets.ModelViewSet):
    """API endpoint that allows lifespan experiments to be viewed or edited."""
    model = Experiment


class StrainViewSet(viewsets.ModelViewSet):
    """API endpoint that allows strains to be viewed or edited."""
    model = Strain


class MeasurementViewSet(viewsets.ModelViewSet):
    """API endpoint that allows lifespan measurements to be viewed or edited."""
    model = Measurement


class EpistasisViewSet(viewsets.ModelViewSet):
    """API endpoint that allows lifespan epistases to be viewed or edited."""
    model = Epistasis


class ComparisonViewSet(viewsets.ModelViewSet):
    """API endpoint that allows lifespan comparisons to be viewed or edited."""
    model = Comparison


class TypeViewSet(viewsets.ModelViewSet):
    """API endpoint that allows lifespan factor types to be viewed or edited."""
    model = Type


class ManipulationViewSet(viewsets.ModelViewSet):
    """API endpoint that allows lifespan manipulations to be viewed or edited."""
    model = Manipulation


class RegimenViewSet(viewsets.ModelViewSet):
    """API endpoint that allows lifespan altering dietary regimens to be viewed or edited."""
    model = Regimen

class AssayViewSet(viewsets.ModelViewSet):
    """API endpoint that allows lifespan assays to be viewed or edited."""
    model = Assay

class InterventionViewSet(viewsets.ModelViewSet):
    """API endpoint that allows lifespan interventions to be viewed or edited."""
    model = Intervention


class FactorViewSet(viewsets.ModelViewSet):
    """API endpoint that allows lifespan factors to be viewed or edited."""
    queryset = Factor.objects.all()
    model = Factor
    serializer_class = FactorSerializer


class StateViewSet(viewsets.ModelViewSet):
    """API endpoint that allows choice states to be viewed or edited."""
    model = State


class TechnologyViewSet(viewsets.ModelViewSet):
    """API endpoint that allows experimental technologies to be viewed or edited."""
    model = Technology


class StudyTypeViewSet(viewsets.ModelViewSet):
    """API endpoint that allows study types to be viewed or edited."""
    model = StudyType


class VariantTypeViewSet(viewsets.ModelViewSet):
    """API endpoint that allows variant types to be viewed or edited."""
    model = VariantType


class ORTypeViewSet(viewsets.ModelViewSet):
    """API endpoint that allows odds ratio types be viewed or edited."""
    model = ORType


class PopulationViewSet(viewsets.ModelViewSet):
    """API endpoint that allows populations be viewed or edited."""
    model = Population


class VariantViewSet(viewsets.ModelViewSet):
    """API endpoint that allows variants be viewed or edited."""
    model = Variant


class GenderViewSet(viewsets.ModelViewSet):
    """API endpoint that allows genders be viewed or edited."""

    model = Gender
