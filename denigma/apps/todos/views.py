import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views.generic.create_update import update_object, delete_object
from django.template import RequestContext
from django.views.generic.edit import CreateView
from django.db.models import Q

from profiles.models import Profile
from data.filters import FilterForm, TableFilter
from data import get

from models import Todo, priorities
from forms import TodoForm
from tables import TodoTable
from filters import TodoFilterSet


class TodoCreate(CreateView):
    context_object_name = 'todo'
    template_name= 'todos/create_todo.html'
    form_class = TodoForm
    model = Todo
    success_url = '/todos/index'

    def dispatch(self, request, *args, **kwargs):
        if 'task' in kwargs and kwargs['task']:
            self.task = kwargs['task']
        else:
            self.task = None
        return super(TodoCreate, self).dispatch(request, *args, **kwargs)

    def get_initial(self):
        """Get initial dictionary from the superclass method."""
        initial = super(TodoCreate, self).get_initial()
        initial = initial.copy()
        initial['creator'] = self.request.user.pk
        initial['importance'] = 'C'
        if self.task:
            initial['title'] = self.task
        return initial


class TodoList(TableFilter):
    model = Todo
    table_class = TodoTable
    queryset = Todo.objects.filter(done=False).order_by('-updated')
    filterset = TodoFilterSet
    success_url = '/todos/index'

    def dispatch(self, request, *args, **kwargs):
        profile = Profile.objects.get(user__username__exact=request.user.username)
        profile.last_list_check = datetime.datetime.today()
        profile.save()
        return super(TodoList, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context =super(TodoList, self).get_context_data(*args, **kwargs)
        context['entry'] = get('Todos')
        return context

    def get_queryset(self):
        qs = self.queryset
        if TodoList.query:
            terms = TodoList.query.split(None)
            for term in terms:
                qs = qs.filter(Q(title__icontains=TodoList.query) |
                               Q(description__icontains=TodoList.query))
        self.filterset = TodoFilterSet(qs, self.request.GET)
        return self.filterset.qs


def todo_index(request):
##    todos = Todo.objects.all().order_by('importance', 'title')
##    t = loader.get_template('index.html')
##    c = Context({'todos':todos, 'choices': priorities,})
##    return HttpResponse(t.render(c))
    if request.user.id is None: # Catch people who haven't logged in.
        return HttpResponseRedirect(reverse(todo_login))
    profile = Profile.objects.get(user__username__exact=request.user.username)
    profile.last_list_check = datetime.datetime.today()
    profile.save()
    todos = Todo.objects.filter(creator=request.user).order_by('importance', '-created', 'title')
    return render_to_response('todos/index.html',
                              {'todos': todos,
                               'choices': priorities,
                               'user': request.user,
                               'error_msg': request.GET.get('error_msg', ''),
                               }, context_instance=RequestContext(request))


def add_todo(request):
    t = Todo( # Creates new todo
        title = request.POST['title'],
        description = request.POST['description'],
        importance = request.POST['importance'],
        start_date = request.POST['start_date'],
        stop_date = request.POST['stop_date'],
        creator = request.user)
    t.save()
    # reverse() takes etiher a view or the name of a view and returns its URLS:
    return HttpResponseRedirect(reverse(todo_index)) # Redirect todo_index view 


def update_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)
    try:
        #if todo.owner.id != request.user.id:
        #    return HttpResponseRedirect(reverse(todo_index) +
        #                                "?error_msw=That's not your todo!")
        pass
    except ObjectDoesNotExist:
        pass
    return update_object( # Call generic update function:
        request,
        object_id=todo_id,
        model=Todo,
        template_name='todos/todo_form.html',
        post_save_redirect='/todos/%(id)s'
     )


def view_todo(request, todo_id):
    #pass
    #todo = Todo.objects.get(pk=todo_id))
    todo = get_object_or_404(Todo, id=todo_id)
    return HttpResponse("%s %s" % (todo.title, todo.description))
    #return HttpResponse(str(todo_id))
    #edit_todo(request, todo_id)

def edit_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)
    #render_to_response('todos/edit.html', todo)
    return HttpResponse("%s %s" % (todo.title, todo.description))

def delete_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)
    if todo.creator.id != request.user.id:
        return HttpResponseRedirect(
            reverse(todo_index) + "?error_msg=That's not your todo!")
    return delete_object(
        request,
        object_id=todo_id,
        model=Todo,
    template_name=('todos/todo_confirm_delete.html'),
        post_delete_redirect='..'
    )

def todo_login(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    error_msg = ''

    if (username and password):
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse(todo_index))
            else:
                error_msg = ("Your account has been disabled!")
        else:
            error_msg = ("your username and pasword were incorrect!")
            password = ''
    return render_to_response('todos/todo_login.html',
                              {'username': username,
                               'password': password,
                               'error_msg': error_msg,
    }, context_instance=RequestContext(request))

def todo_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse(todo_login))

##def todo(request):
##    return HttpResponse("""<html>
##<head>
##<title>My Todo list!</title>
##</head>
##<body>
##<h1>Todos:</h1>
##<p>Read the evolutionary paper suggested by Pedro</p>
##<p>Search for more recent publication on Evolution-degree correlations</p>
##<p>Add an intervation to decode.</p>
##<p>Order your new ebooks</p>
##<p>Respond to Pedro</p>
##</body>
##</html>""")
##
##def todo(request):
##    todos = [{'title':"Read the evolutionary paper suggested by Pedro.",
##             'importance':"Important"},
##            {'title':"Search for more recent publication on Evolution-degree correlations.",
##             'importance':"Important"},
##            {'title':"Add an intervation to decode.",
##             'importance':"Minor"},
##            {'title':"Order your new eBooks.",
##             'importance':"Minor"},
##            {'title':"Respond to Pedro.",
##             'importance':"High"},]
##    t = loader.get_template('index.html')
##    c = Context({'todos': todos,})
##    return HttpResponse(t.render(c))
