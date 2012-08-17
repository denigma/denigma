# Create your views here.
from django.http import HttpResponse
from annotations.models import DiscontinuedId, Taxonomy
#from mapping import m

def index(request):
    latest_ids = DiscontinuedId.objects.all().order_by('-entrez_gene_id')[:5]
    output = ','.join([str(p.entrez_gene_id) for p in latest_ids])
    return HttpResponse(output)
    
def search(request):
    get_it = DiscontinuedId.objects.get(discontinued_id=100534368)
    output = get_it.entrez_gene_id
    return HttpResponse(output)

def find(request):
    #m(request, 4932
    #string = m()
    return HttpResponse(request)

def update_species(request):
    taxonomy = Taxonomy.objects.all()
