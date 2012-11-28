"""Denigma Duties."""
from django.shortcuts import render

from data import get


def index(request, template='duties/index.html'):
    duties = get("Duties")
    return render(request, template, {'duties': duties})