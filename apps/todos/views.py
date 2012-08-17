from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from models import Todo, importance_choices
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views.generic.create_update import update_object, delete_object


def todo_index(request):
##    todos = Todo.objects.all().order_by('importance', 'title')
##    t = loader.get_template('index.html')
##    c = Context({'todos':todos, 'choices': importance_choices,})
##    return HttpResponse(t.render(c))
    if request.user.id is None: # Catch people who haven't logged in.
        return HttpResponseRedirect(reverse(todo_login))
    todos = Todo.objects.filter(owner=request.user).order_by('importance', 'title')
    return render_to_response('todos/index.html',
                              {'todos': todos,
                               'choices': importance_choices,
                               'user': request.user,
                               'error_msg': request.GET.get('error_msg', ''),
                               })


def add_todo(request):
    t = Todo( # Creates new todo
        title = request.POST['title'],
        description = request.POST['description'],
        importance = request.POST['importance'],
        start_date = request.POST['start_date'],
        stop_date = request.POST['stop_date'],
        owner = request.user)
    t.save()
    # reverse() takes etiher a view or the name of a view and returns its URLS:
    return HttpResponseRedirect(reverse(todo_index)) # Redirect todo_index view 


def update_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)
    if todo.owner.id != request.user.id:
        return HttpResponseRedirect(reverse(todo_index) +
                                    "?error_msw=That's not your todo!")
    return update_object( # Call generic update function:
        request,
        object_id=todo_id,
        model=Todo,
        template_name='todos/todo_form.html',
        post_save_redirect='.todos/%(id)s'
     )

def view_todo(request, todo_id):
    pass

def edit_todo(request, todo_id):
    pass

def delete_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)
    if todo.owner.id != request.user.id:
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
    })

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
