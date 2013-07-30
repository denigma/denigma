from tastypie.resources import ModelResource
from lifespan.models import Factor


class FactorResource(ModelResource):
    class Meta:
        queryset = Factor.objects.all()
        allowed_methods = ['get']
        resource_name = 'factor'
