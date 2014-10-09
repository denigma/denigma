import csv
import json

from django.views.generic import FormView, TemplateView
from django.db.models import Q
from django_tables2 import SingleTableView, RequestConfig
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from lifespan.models import Population, StudyType, VariantType, Variant
from tables import VariantTable

from annotations.models import Classification, GO
from utils.dumper import dump


from filters import VariantFilterSet
from forms import FilterForm


@csrf_exempt
def search(request, keyword=None, template_name='longevitydb/search.html'):
    print("Searching", keyword)
    print(request.POST)
    variants = Variant.objects.all()
    context_data = {}
    if request.method == 'POST':
    #
         if ('keyword' in request.POST): # or (keyword and keyword != "Nothing"):
             print(request.POST)
             if keyword and keyword != "Nothing":
                 keyword = keyword
             else:
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

    #         keyword = 'Nothing'
    #     if ('term' in request.POST) or (t and t != "Nothing"):
    #         if t and t != "Nothing":
    #             term = t
    #         else:
             term = request.POST['keyword'].replace('"', '')
    #
             if 'GO:' in term:
                 terms = GO.objects.filter(go_id=term)
             else:
                 terms = GO.objects.filter(go_term__icontains=term)
             ids = ["Q(factor__entrez_gene_id=%s)" % go.entrez_gene_id for go in terms]
             sql = " | ".join(ids)
             variants2 = eval("variants.filter("+sql+")")
         else:
             try:
                query = float(keyword)
                variants = variants.filter(Q(odds_ratio=query) |
                                                Q(pvalue=query) |
                                                Q(pmid=query) |
                                                Q(factor__entrez_gene_id=query))
             except Exception as e:
                variants1 = variants.filter(Q(polymorphism__icontains=keyword) |
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

             term = keyword
             if 'GO:' in term:
                 terms = GO.objects.filter(go_id=term)
             else:
                 terms = GO.objects.filter(go_term__icontains=term)
             ids = ["Q(factor__entrez_gene_id=%s)" % go.entrez_gene_id for go in terms]
             sql = " | ".join(ids)
             print("SQL = " % sql)
             variants2 = eval("variants.filter("+sql+")")
             qs = variants2.exclude(choice__name__contains='Review').distinct().order_by('pvalue')
             #response_dict = {'keyword': keyword, 'term': term}
             response = HttpResponse(content_type='text/csv')
             response['Content-Disposition'] = 'attachment: filename="output.csv"'
             writer = csv.writer(response, delimiter="\t")
             dump(qs, write=False, writer=writer, exclude=('created','updated', 'choice'))
             return response
    #     else:
    #         term = 'Nothing'
        # from itertools import chain
         #variants = list(chain(variants1, variants2))
         #variants = variants1 | variants2
         qs = variants2.exclude(choice__name__contains='Review').distinct().order_by('pvalue')
    #     context_data['keyword'] = keyword
         context_data['term'] = term
         # if keyword:
         #     keyword = keyword
         #     term = keyword
         #     response_dict = {'keyword': keyword, 'term': term}
         #     response = HttpResponse(content_type='text/csv')
         #     response['Content-Disposition'] = 'attachment: filename="output.csv"'
         #     writer = csv.writer(response, delimiter="\t")
         #     dump(qs, write=False, writer=writer, exclude=('created','updated', 'choice'))
         #     return response
    #
         table = VariantTable(qs)
         RequestConfig(request).configure(table)
         context_data['table'] = table
         #context_data = {}

         return render(request, template_name, context_data)
    else:
        table = VariantTable(Variant.objects.all().order_by('pvalue').exclude(pvalue=None))
        RequestConfig(request).configure(table)
        context_data = {'keyword': "Nothing", 'table': table}
        return render(request, template_name, context_data)


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
    output = False
    success_url = '/browse/'
    selected = None

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
        print(self.request)
        try:
            if 'populations' in self.request.GET:
                populations = eval(str(self.request).split("GET:<QueryDict: {u'populations': ")[1].split('}>,')[0]) #.GET['population[]']
                print(populations)
                self.selected = populations
                query_string = []
                for population in populations:
                    print(population)
                    query_string.append('Q(ethnicity__name="%s")' % population)
                self.qs = eval('self.qs.filter('+" | ".join(query_string)+')')
        except Exception as e:
            print(e)
        return self.qs

    def form_valid(self, form):
        output = form.cleaned_data['output']
        self.output = output
        BrowseView.output = output
        return super(BrowseView, self).form_valid(form)

    def render_to_response(self, context, **response_kwargs):
        print("Render to response")
        if BrowseView.output: # or self.download:
            BrowseView.output = False
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment: filename="output.csv"'
            writer = csv.writer(response, delimiter="\t")
            dump(self.qs, write=False, writer=writer, exclude=('created','updated', 'choice'))
            return response
        else:
            return super(BrowseView, self).render_to_response(context, **response_kwargs)

    def get_context_data(self, **kwargs):
        print("Get context data")

        context = super(BrowseView, self).get_context_data(**kwargs)
        context['form'] = FilterForm()
        print(hasattr(self, 'variantsfilter')) #, len(self.variantsfilter))
        print("self.variantsfilter: %s" % type(self.variantsfilter))
        context['variantsfilter'] = self.variantsfilter
        context['populations'] = Population.objects.all()
        context['selected'] = self.selected
        return context
