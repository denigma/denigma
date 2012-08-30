from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django import forms

from models import Page, Tag

import markdown


class SearchForm(forms.Form):
    text = forms.CharField(label="Enter search term")
    search_content = forms.BooleanField(label="Search content", required=False)
    search_tags = forms.BooleanField(label="Search tags", required=False)


def search_page(request):
    """Searching for page."""
    term = ''
    if request.method == "POST":
        f = SearchForm(request.POST)
        if not f.is_valid():
            return render_to_response("./wiki/search.html", {"form":f},
                                      context_instance=RequestContext(request)) # Blank is invalid raise error.
        else:
            term = f.cleaned_data["text"]
            if ' ' in term: # Multi word term -> MultiWordTerm
               term = ''.join(term.title().split(' '))
            print term
            pages = Page.objects.filter(name__icontains=term) # Normalized: i.e. gets converted to python construct.

            contents = []
            if f.cleaned_data["search_content"]:
                contents = Page.objects.filter(content__contains=term)

            tags = []
            if f.cleaned_data["search_tags"]:
                tags = Tag.objects.filter(name__icontains=term)

            return render_to_response("./wiki/search.html",
                                      {"form":f, "pages":pages, "contents":contents,
                                      "tags":tags, "term":term},
                                      context_instance=RequestContext(request))

    f = SearchForm()
    return render_to_response("./wiki/search.html", {"form":f, "term":term},
                              context_instance=RequestContext(request))

def index_page(request):
   """"Creates a index, i.e. a list, of all entries in the Wiki."""
   pages = Page.objects.all().order_by('name')
   tags = Tag.objects.all().order_by('name')
   return render_to_response("./wiki/index.html", {"pages": pages, "tags": tags},
                             context_instance=RequestContext(request))


def view_page(request, page_name):
    if page_name in specialPages: # Do not query database for special page names.
        return specialPages[page_name](request) # Pass it a request.
    try: 
        page = Page.objects.get(pk=page_name)
        tags = page.tags.all()
    except Page.DoesNotExist:
        return render_to_response("./wiki/create.html", {"page_name":page_name},
                                  context_instance=RequestContext(request))
    content = page.content

    # Hyperlinking:
    pages = tuple([p.name for p in Page.objects.all()])
    words = content.split(' ')
    for index, word in enumerate(words):
       if word in pages:
          words[index] = '<a href="/wiki/page/{0}">{0}</a>'.format(word)
    content = " ".join(words)

    return render_to_response("./wiki/view.html", {"page_name":page_name, 
                                                   "content": markdown.markdown(content),
                                                   "tags":tags},
                                                   context_instance=RequestContext(request)) # Important for correct rendering.

def edit_page(request, page_name):
    try:
        page = Page.objects.get(pk=page_name)
        tags = " ".join([tag.name for tag in page.tags.all()])
        content = page.content
    except Page.DoesNotExist:
        content  = ""
        tags = ''
    return render_to_response("./wiki/edit.html",
                              {"page_name":page_name, "content":content, "tags":tags},
                              context_instance=RequestContext(request, {}))  # Edited it later on.
    
def save_page(request, page_name):
    content = request.POST["content"]
    tag_list = []
    if"tags" in request.POST:
        tags = request.POST["tags"]
        tag_list = [Tag.objects.get_or_create(name=tag)[0] for tag in tags.split()] # .get_or_create returns the object + Boolean whether it is already there or new.
    try:
        page = Page.objects.get(pk=page_name)
        page.content = content
    except Page.DoesNotExist:
        page = Page(name=page_name, content=content)
    page.save()

    # Add tags:
    for tag in tag_list:
       page.tags.add(tag) # Creates relationships between the page and each tags.

    return HttpResponseRedirect("/wiki/page/" + page_name + "/")

def view_tag(request, tag_name):
    """Views all the pages that are tagged with a specific tag."""
    tag = Tag.objects.get(pk=tag_name)
    pages = tag.page_set.all()
    return render_to_response("./wiki/tags.html", {"tag_name": tag_name, "pages": pages},
                              context_instance=RequestContext(request))

specialPages = {"SearchPage": search_page, "IndexPage": index_page}
