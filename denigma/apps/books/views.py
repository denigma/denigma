# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse
from models import Book, Publisher, Author
from django.shortcuts import get_object_or_404
from django.views.generic import list_detail


def latest_books(request):
    book_list = Book.objects.order_by('-pub_date')[:10]
    return render_to_response('books/latest_books.html', {'book_list': book_list})

def search_form(request):
    return render_to_response('search_form.html')

def search(request):
    #if 'q' in request.GET: message = "You searched for: %r % request.GET['q']
    #else: message = 'You submitted an empty form.'
    #return HttpResponse(message)
    errors = []
    if 'q' in request.GET:# and request.GET['q']:
        q = request.GET['q']
        if not q:
            errors.append('Enter a search term.')
        elif len(q) > 200:
            errors.append('Please enter at most 20 characters.')
        else:
            books = Book.objects.filter(title__icontains=q)
            return render_to_response('search_results.html',
                                  {'books':books, 'query':q})

        #return HttpResponse('Please submit a search term')
    return render_to_response('search_form.html',{'errors':errors})
    
def books_by_publisher(request, name):
    # Looks up the publisher (and raise a 404 if it can't be found).
    publisher = get_object_or_404(Publisher, name__iexact=name)

    # Use the object_list view for the heavy lifting.
    return list_detail.objects_list(
        request,
        queryset = Book.objects.filter(publisher=publisher),
        template_name = 'books/books_by_publisher.html',
        template_boject_name = 'book',
        extra_context = {'publisher': publisher}
    )

def author_detail(request, author_id):
    # Delegate to the genreic view and get an HttpResponse.
    response = list_detail.object_detail(
        request,
        queryset = Author.objects.all(),
        object_id = author_id,
    )

    # Record the last accessed date. We do this after the call
    # to object_detail(), not before it,so that this won't be called
    # unless the Author actually exists. (If the authro doesn't exist,
    # object_detail() will raise Http404, and we won't reach this point.)
    now = datetime.datetime.now()
    Author.objects.filter(id=author_id).update(last_accessed=now)
    
    return response

def author_list_plaintext(request):
    response = list_detail.object_list(
        request,
        queryset = Author.objects.all(),
        mimetype = 'text/plain',
        template_name = 'books/author_list.txt',
    )
    response["Content-Disposition"] = "attachment; filename=authors.txt"
    return response
