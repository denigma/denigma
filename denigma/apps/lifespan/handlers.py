# -*- coding: utf-8 -*-
"""Handles the changes of the references in the Intervention effect and factor observation fields."""
import re

from datasets.models import Reference


def changed_references(sender, instance, action, reverse, model, pk_set, **kwargs):
    #print("changed referenes: %s" % action)
    if action == "post_clear":
        rc = re.compile(r'\W(?P<id>\d{7,})\W')
        if hasattr(instance, 'effect'): # isinstance(instance, Intervention):
            references = re.findall(rc, instance.effect)
        else: # if isinstance(instance, Factor):
            references = re.findall(rc, instance.observation)
        for reference in references:
            reference, created = Reference.objects.get_or_create(pmid=reference)
            #print(reference)
            instance.references.add(reference)
            #print("lifespan.models.Intervention.save(): %s" % instance.references.all())