"""Non-Functional classes.

These classes were deprecated as they appeared to make it too complex.
"""
#
# from django.forms import Form, CharField
#
#
# class SearchForm(Form):
#     term = CharField()
#
# class BrowseForm(Form):
#     pass


# class QueryView(SingleTableView, FormView):
#     context_object_name = 'variants'
#     table_class = VariantTable
#     model = Variant
#
#
# class SearchView(SingleTableView, FormView):
#     template_name = 'longevitydb/search.html'
#     form_class = SearchForm
#     #success_url = '/longevitydb/search/'
#     context_object_name = 'variants'
#     table_class = VariantTable
#     model = Variant
#
#     def dispatch(self, request, *args, **kwargs):
#         print("Dispatch")
#         if 'term' in kwargs:
#             self.term = kwargs['term']
#         #print(request.keys())
#         return super(SearchView, self).dispatch(request, *args, **kwargs)
#
#     def form_valid(self, form):
#         print("Form valid")
#         #self.term = form.cleaned_data['term']
#         #print(self.request)
#         self.term = self.request.POST['term']
#         qs = self.get_queryset()
#         #print(self.term)
#         #print(self.success_url)#
#         context = RequestContext(self.request)
#         RequestConfig(request).configure(table)
#         self.kwargs['views'] = self.get_context_data(**self.kwargs)
#         context.update(self.kwargs['views'])
#        # context['qs'] = qs
#        # context['object_list'] = qs
#         #self.kwargs['object_list'] = qs
#         return render(self.request, template_name=self.template_name,
#             context_instance=context)

    # def form_invalid(self, form):
    #     print("Form invalid")
    #     #self.term = form.cleaned_data['term']
    #     #print(self.request)
    #     self.term = self.request.POST['term']
    #     #print(self.term)
    #     #print(self.success_url)
    #     return super(SearchView, self).form_invalid(form)

    # def get_queryset(self):
    #     print("Get queryset")
    #     #print(self.request)
    #     if self.request.method == 'POST':
    #         print('POST' in self.request)
    #         if 'POST' in self.request:
    #             self.term = self.request.POST['term']
    #     if hasattr(self, 'term'):
    #         term = self.term
    #         print("Term = %s" % term)
    #         try:
    #             query = float(term)
    #             variants = Variant.objects.filter(Q(odds_ratio=query) |
    #                                             Q(pvalue=query) |
    #                                             Q(pmid=query) |
    #                                             Q(factor__entrez_gene_id=query))
    #         except Exception as e:
    #             variants = Variant.objects.filter(Q(polymorphism__icontains=term) |
    #                                          Q(location__icontains=term) |
    #                                          Q(initial_number__icontains=term) |
    #                                          Q(replication_number__icontains=term) |
    #                                          Q(age_of_cases__icontains=term) |
    #                                          Q(factor__symbol=term) |
    #                                          Q(factor__name__icontains=term) |
    #                                          Q(factor__ensembl_gene_id=term) |
    #                                          Q(description__icontains=term) |
    #                                          Q(longer_lived_allele__icontains=term) |
    #                                          Q(shorter_lived_allele__icontains=term) |
    #                                          Q(ethnicity__name__icontains=term) |
    #                                          Q(study_type__name__icontains=term) |
    #                                          Q(technology__name__icontains=term) |
    #                                          Q(reference__title__icontains=term)).order_by('-id').order_by('pvalue')
    #     else:
    #         variants = Variant.objects.all().order_by('pvalue').exclude(pvalue=None) #, 'longer_lived_allele')
    #     #self.variantsfilter = VariantFilterSet(variants, self.request.GET)
    #     #self.qs = self.variantsfilter.qs.exclude(choice__name__contains='Review').distinct().order_by('pvalue')
    #     self.qs = variants.exclude(choice__name__contains='Review').distinct().order_by('pvalue')
    #     return self.qs

    # def get_context_data(self, **kwargs):
    #     context = super(SearchView, self).get_context_data(**kwargs)
    #     context['variantsfilter'] = self.variantsfilter
    #     return context

    # def get_queryset(self):
    #     print("Get queryset")
    #     variants = Variant.objects.all().order_by('pvalue').exclude(pvalue=None) #, 'longer_lived_allele')
    #     self.variantsfilter = VariantFilterSet(variants, self.request.GET)
    #     self.qs = self.variantsfilter.qs.exclude(choice__name__contains='Review').distinct().order_by('pvalue')
    #     return self.qs
    #
    # def get_context_data(self, **kwargs):
    #     print("Get context data")
    #     context = super(SearchView, self).get_context_data(**kwargs)
    #     print("Get populations")
    #     context['populations'] = Population.objects.all()
    #     context['study_types'] = StudyType.objects.all()
    #     context['variant_types'] = VariantType.objects.all()
    #     context['variant_associations'] = Variant.objects.all()
    #     context['classifications'] = [Classification.objects.get(title='Longevity-Associated'),
    #                                   Classification.objects.get(title='No Age Effect')]
    #     print("Got classifications")
    #     print(hasattr(self, 'variantsfilter')) #, len(self.variantsfilter))
    #     print("self.variantsfilter: %s" % type(self.variantsfilter))
    #     context['variantsfilter'] = self.variantsfilter
    #     return context
