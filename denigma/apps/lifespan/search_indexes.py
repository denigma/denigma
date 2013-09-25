# -*- coding: utf-8 -*-
import datetime

from haystack import indexes

from models import (Study, Experiment, Strain, Measurement, Epistasis, Regimen,
                    Assay, Manipulation, Intervention, Factor)

from models import Variant, ORType, VariantType, Population, StudyType, Technology, State


class StudyIndex(indexes.SearchIndex, indexes.Indexable):
    created = indexes.DateTimeField(model_attr='created')
    updated = indexes.DateTimeField(model_attr='updated')

    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Study

    def index_queryset(self):
        return self.get_model().objects.all()


class ExperimentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Experiment

    def index_queryset(self):
        return self.get_model().objects.all()


class StrainIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Strain

    def index_queryset(self):
        return self.get_model().objects.all()


class MeasurementIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Measurement

    def index_queryset(self):
        return self.get_model().objects.all()


class EpistasisIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Epistasis

    def index_queryset(self):
        return self.get_model().objects.all()


class RegimenIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Regimen

    def index_queryset(self):
        return self.get_model().objects.all()


class AssayIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Assay

    def index_queryset(self):
        return self.get_model().objects.all()


class ManipulationIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Manipulation

    def index_queryset(self):
        return self.get_model().objects.all()


class InterventionIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Intervention

    def index_queryset(self):
        return self.get_model().objects.all()


class FactorIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Factor

    def index_queryset(self):
        return self.get_model().objects.all()


class VariantIndex(indexes.SearchIndex):
    created = indexes.DateTimeField(model_attr='created')
    updated = indexes.DateTimeField(model_attr='updated')

    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Variant

    def index_queryset(self):
        return self.get_model().objects.all()


class ORTypeIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return ORTypeIndex

    def index_queryset(self):
        return self.get_model().objects.all()

class VariantTypeIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return VariantType

    def index_queryset(self):
        return self.get_model().objects.all()


class PopulationIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Population

    def index_queryset(self):
        return self.get_model().objects.all()


class StudyTypeIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Population

    def index_queryset(self):
        return self.get_model().objects.all()


class TechnologyIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Technology

    def index_queryset(self):
        return self.get_model().objects.all()


class StateIndex(indexes.SearchIndex):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return State

    def index_queryset(self):
        return self.get_model().objects.all()


#234567891123456789212345678931234567894123456789512345678961234567897123456789