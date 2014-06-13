from django.views.generic import FormView, TemplateView
from django.db.models import Q
from django_tables2 import SingleTableView, RequestConfig
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


from lifespan.models import Population, StudyType, VariantType, Variant
from lifespan.tables import VariantTable
from lifespan.forms import FilterForm
from annotations.models import Classification, GO

#from forms import SearchForm, BrowseForm
from filters import VariantFilterSet

@csrf_exempt
def search(request, template_name='longevitydb/search.html'):
    print("Searching")
    variants = Variant.objects.all()
    if request.method == 'POST':
        if 'keyword' in request.POST:
            keyword = request.POST['keyword']
            try:
                query = float(keyword)
                variants = variants.filter(Q(odds_ratio=query) |
                                                Q(pvalue=query) |
                                                Q(pmid=query) |
                                                Q(factor__entrez_gene_id=query))
            except Exception as e:
                variants = variants.filter(Q(polymorphism__icontains=keyword) |
                                             Q(location__icontains=keyword) |
                                             Q(initial_number__icontains=keyword) |
                                             Q(replication_number__icontains=keyword) |
                                             Q(age_of_cases__icontains=keyword) |
                                             Q(factor__symbol=keyword) |
                                             Q(factor__name__icontains=keyword) |
                                             Q(factor__ensembl_gene_id=keyword) |
                                             Q(description__icontains=keyword) |
                                             Q(longer_lived_allele__icontains=keyword) |
                                             Q(shorter_lived_allele__icontains=keyword) |
                                             Q(ethnicity__name__icontains=keyword) |
                                             Q(study_type__name__icontains=keyword) |
                                             Q(technology__name__icontains=keyword) |
                                             Q(reference__title__icontains=keyword)).order_by('-id').order_by('pvalue')
        if 'term' in request.POST:
            term = request.POST['term'].replace('"', '')
            if 'GO:' in term:
                terms = GO.objects.filter(go_id=term)
            else:
                terms = GO.objects.filter(go_term__icontains=term)
            ids = ["Q(factor__entrez_gene_id=%s)" % go.entrez_gene_id for go in terms]
            sql = " | ".join(ids)
            variants = eval("variants.filter("+sql+")")
        qs = variants.exclude(choice__name__contains='Review').distinct().order_by('pvalue')
        table = VariantTable(qs)
        RequestConfig(request).configure(table)
        return render(request, template_name, {'table': table})
    else:
        table = VariantTable(Variant.objects.all())
        RequestConfig(request).configure(table)
        return render(request, template_name, {'table': table})


class HomeView(TemplateView):
    template_name = 'longevitydb/home.html'


class AboutView(TemplateView):
    template_name = 'longevitydb/about.html'


class BrowseView(SingleTableView, FormView):
    template_name = 'longevitydb/browse.html'
    form_class = FilterForm  # BrowseForm
    context_object_name = 'variants'
    table_class = VariantTable
    model = Variant

    def dispatch(self, request, *args, **kwargs):
        print("Dispatch")
        if 'model' in kwargs:
            self.model = kwargs['model']
        if 'type' in kwargs:
            self.type = kwargs['type']
        return super(BrowseView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        print("Get queryset")
        variants = Variant.objects.all().order_by('pvalue').exclude(pvalue=None) #, 'longer_lived_allele')
        self.variantsfilter = VariantFilterSet(variants, self.request.GET)
        self.qs = self.variantsfilter.qs.exclude(choice__name__contains='Review').distinct().order_by('pvalue')
        return self.qs

    def get_context_data(self, **kwargs):
        print("Get context data")
        context = super(BrowseView, self).get_context_data(**kwargs)
        context['classifications'] = [Classification.objects.get(title='Longevity-Associated'),
                                      Classification.objects.get(title='No Age Effect')]
        print("Got classifications")
        print(hasattr(self, 'variantsfilter')) #, len(self.variantsfilter))
        print("self.variantsfilter: %s" % type(self.variantsfilter))
        context['variantsfilter'] = self.variantsfilter
        return context
