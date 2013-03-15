from collections import OrderedDict, Callable

from django.http import HttpResponseRedirect
from django.db.models import Model, Manager
from django.core.urlresolvers import reverse


def reverse2(name, *args, **kwargs):
    return reverse(name, args=args, kwargs=kwargs)

def defdict_to_dict(defdict, constructor=dict):
    """Recursively convert default dicts to regular dicts.
    constructor: convert to a custom type of dict, e.g. OrderedDict."""
    if isinstance(defdict, dict):
        new = constructor()
        for key, value in defdict.items():
            new[key] = defdict_to_dict(value, constructor)
        return new
    else:
        return defdict


def defdict_to_odict(defdict):
    return defdict_to_dict(defdict, OrderedDict)


def redir(to, *args, **kwargs):
    if not (to.startswith('/') or to.startswith("http://") or to.startswith("../") or to=='#'):
        to = reverse(to, args=args, kwargs=kwargs)
    return HttpResponseRedirect(to)

class BaseModel(Model):
    class Meta: abstract = True
    obj = objects = Manager()

    def update(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.save()


class DefaultOrderedDict(OrderedDict):
    def __init__(self, default_factory=None, *a, **kw):
        if (default_factory is not None and
            not isinstance(default_factory, Callable)):
            raise TypeError('First argument must be callable')
        OrderedDict.__init__(self, *a, **kw)
        self.default_factory = default_factory

    def __getitem__(self, key):
        try:
            return OrderedDict.__getitem__(self, key)
        except KeyError:
            return self.__missing__(key)

    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        self[key] = value = self.default_factory()
        return value

    def __reduce__(self):
        if self.default_factory is None:
            args = tuple()
        else:
            args = self.default_factory,
        return type(self), args, None, None, self.items()

    def copy(self):
        return self.__copy__()

    def __copy__(self):
        return type(self)(self.default_factory, self)

    def __deepcopy(self, memo):
        import copy
        return type(self)(self.default_factory, copy.deepcopy(self.items()))

    def __repr__(self):
        return 'DefaultOrderDict(%s, %s)' % (self.default_factory, OrderedDict.__repr__(self))

