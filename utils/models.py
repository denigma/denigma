"""Pretty django models model instances updating."""
from django.db.models import AutoField


def copy_model_instance(obj):
    initial = dict([(f.name, getattr(obj, f.name))
                    for f in obj._meta.fields
                        if not isinstance(f, AutoField) and\
                            not f in obj._meta.parents.values()])
    return obj.__class__(**initial)

def refresh(instance):
    """Select and return instance from database.
    Usage:    ``instance = refresh(instance)```
    """
    return instance.__class__.objects.get(pk=instance.pk)

def update(instance, **data):
    """Update instance with data directly by using ``update()``
    skipping calling ``save()`` method and without calling signals.
    Usage:     ``instance = update(instance, some_field=some_value)``
    """
    instance.__class__.objects.filter(pk=instance.pk).update(**data)
    return refresh(instance)