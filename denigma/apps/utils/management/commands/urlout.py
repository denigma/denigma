"""Provides a admin command that generates a list of URLs
and their documentation automatically.

It is non-functional as x has no name nor default_args.
"""
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    """Generates documentation for the URLs. For each URL includes the
    documentation from the callback implementing the URL and prints the default
    arguments along with the URL pattern and name."""
    def handle(self, *args, **options):
        url_module = None
        exec('import '+settings.ROOT_URLCONF+
             ';url_module='+settings.ROOT_URLCONF)
        doc = file('doc.html', 'w')
        doc.write("<table border=1 cellspacing=0 cellpadding=5>")
        doc.write("<tr><th>URL Pattern<th>Name<th>Documentation<th>Parameters")
        for x in url_module.urlpatterns:
            doc.write("<tr>")
            doc.write("<td>")
            doc.write(x._regex)
            doc.write("<td>")
            doc.write(str(x.name))
            try:
                documentation = str(x.callback.__doc__)
                doc.write("<td><pre>")
                doc.write("</pre>")
            except:
                doc.write("<td>Unable to find module")
            doc.write("<td>")
            doc.write(str(x.default_args))
        doc.write("</table")
        doc.close()
#234567891123456789212345678931234567894123456789512345678961234567897123456789