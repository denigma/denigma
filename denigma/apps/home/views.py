from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from forms import DynamicForm


def home(request):
    return HttpResponse("Home Page")

def index(request):
    return render_to_response('home/index.html', {'user': request.user})

def base(request):
    return render_to_response('home/base.html',
                             {'user': request.user,
                              'error_msg': request.GET.get('error_msg', ''),
                             }, context_instance=RequestContext(request))

def page(request):
   return render_to_response('home/page.html',
                             context_instance=RequestContext(request))

def dynamic_view(request, val):
    """Dynamically generate input data from formset."""
    initial_data = []
    initial_data.append({'fields_1': data.info})

    # Inializing formset:
    DynamicFormSet=formset_factory(DynamicForm, extra=0)
    formset = DynamicFormSet(initial=initial_data)
    context = {'formset': formset}
    if request.method == 'POST':
        formset = DynamicFormSet
        if formset.is_valie():
            # You can work with the formset dictionary elements in the views function (or) pass it to
            #forms.py script through an instance of MyForm
            return HttpResponse(formset.cleaned_data)
    return render_to_response('test.html', context,
        context_instance=RequestContext(request))


def LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


def SuperUserRequiredMixin(object):
    @user_passes_test(lambda u: u.is_superuser)
    def dispatch(self, request, *args, **kwargs):
        return super(SuperUserRequiredMixin, self).dispatch(request, *args, **kwargs)