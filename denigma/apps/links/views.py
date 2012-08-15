# -*- coding: utf-8 -*-
"""Views for links."""
from django.views.generic import list_detail
from links.models import Link

def links_by_language(request):

    # Use the object_list view for the heavy lifting:
    language = request.LANGUAGE_CODE
    return list_detail.object_list(
        request,
        queryset = Link.published.filter(language=language),
        template_name = "links/links_by_language.html",
        template_object_name = "links",
        )

