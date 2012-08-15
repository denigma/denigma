from django.conf.urls.defaults import patterns
from django.views.generic import list_detail
from books.models import Publisher, Book
from books.views import books_by_publisher, author_detail

#def get_books(): return Book.objects.all()

book_info = {
    'queryset': Book.objects.order_by('-publication_date'),
}

publisher_info = {
    'queryset': Publisher.objects.all(),
    'template_name': 'publisher_list.html',
    #'template_object_name': 'publisher',
    'extra_context': {'book_list': Book.objects.all} #() get_books
}

apress_books = {
    'ueryset': Book.objects.filter(publisher__name='Apress Publishing'),
    'template_name': 'book/apress_list.html'
}

urlpatterns = patterns('books.views',
    (r'^about/(|w+)/$', 'about_pages'),
    (r'^publishers/$', list_detail.object_list, 'publisher_info'),
    (r'^books/$', list_detail.object_list, 'book_info)',
    (r'^books/apress/$', list_detail.object_list, 'apress_books'),
    (r'^books/(\w+)$', 'books_by_publisher'),
    (r'^authors/(?P<author_id>d+)$', 'author_detail'),
)


