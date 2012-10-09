from django.conf.urls.defaults import patterns, url, include
from django.views.generic import list_detail


from models import Publisher, Book
from views import books_by_publisher, author_detail
from views import AuthorCreate, AuthorUpdate, AuthorDelete


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
    'queryset': Book.objects.filter(publisher__name='Apress Publishing'),
    'template_name': 'book/apress_list.html'
}

urlpatterns = patterns('books.views',
    url(r'^$', 'index', name='books'),
    #url(r'^about/(|w+)/$', 'about_pages'),
    #url(r'^publishers/$', list_detail.object_list, 'publisher_info'),
    #url(r'^books/$', list_detail.object_list, 'book_info'),
    #url(r'^books/apress/$', list_detail.object_list, 'apress_books'),
    #url(r'^books/(\w+)$', 'books_by_publisher'),

    url(r'^authors/(?P<author_id>\d+)$', 'author_detail'),
    #url(r'^author/add/$', AuthorCreate.as_view(), name='author_add'),
    #url(r'^author/(?P<pk>\d+)/$', AuthorUpdate.as_view(), name='author_update').
    #url(r'^author/(?P<pk>\d+)/$', AuthorDelete.as_view(), name='author_delete'),
)

urlpatterns += patterns('books.views',                       
    url(r'latest/$', 'latest_books'),
    url(r'^search-form/$', 'search_form'),
    url(r'^search/$', 'search'),
    url(r'^author_list_plaintext/$', 'author_list_plaintext'),
)
