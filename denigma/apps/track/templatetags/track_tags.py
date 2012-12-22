from django import template

from track.models import Visitor

register = template.Library()


class VisitorsOnSite(template.Node):
    """
    Injects the number of active users on the site as an integer into the context.
    """
    def __init__(self, varname, same_page=False):
        """Visitor"""
        self.varname = varname
        self.same_page = same_page

    def render(self, context):
        """VisitorOnSite.render"""
        if self.same_page:
            try:
                request = context['request']
                count = Visitor.objects.active().filter(url=request.path).count()
                #print("self.same_page: %s" % count)
            except KeyError:
                raise template.TemplateSyntaxError(
                    "Please add 'django.core.context_processers.request' to "
                    "the TEMPLATE_CONTEXT_PROCESSORS if you want to see how "
                    "many users are ont he same page.")
        else:
            count = Visitor.objects.active().count()
            #print("self.same_page else: %s" % count)
        context[self.varname] = count
        #print(count)
        return ''

def visitors_on_site(parser, token):
    """Determines the number of active users on the site and puts it into the
    context."""
    try:
        tag, a, varname = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            'visitors_on_site usage: {% visitors_on_site as visitors %}')
    return VisitorsOnSite(varname)
register.tag(visitors_on_site)

def visitors_on_page(parser, token):
    """Determines the number of active users on the same page and puts it into
    the context."""
    try:
        tag, a, varname = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            'visitor_on_age usage: {% visitors_on_page as visitors %}')

    return VisitorsOnSite(varname, same_page=True)
register.tag(visitors_on_page)
#234567891123456789212345678931234567894123456789512345678961234567897123456789