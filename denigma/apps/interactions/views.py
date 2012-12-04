from django.shortcuts import render

from data import get


def index(request, template='interactions/index.html'):
    entry = get("Interactions")
    return render(request, template, {'entry': entry})

