from django.shortcuts import render
from django.http import HttpResponse, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session
from django.contrib.auth.decorators import login_required

import redis

from video.models import Comment, User


@login_required
def home(request, template_name='video/video.html'):
    comments = Comment.objects.select_related().all()[0:100]
    return render(request, template_name, locals())

@csrf_exempt
def node_api(request):
    try:
        # Get User from sessionid
        session = Session.objects.get(session_key=request.POST.get('sessionid'))
        user_id = session.get_decoded().get('_auth_user_id')
        user = User.objects.get(id=user_id)

        # Create Comment
        Comment.objects.create(user=user, text=request.POST.get('comment'))

        # Once comment has been created post it to the chat channel
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        r.publish('chat', user.username + ': ' + request.POST.get('comment'))

        return HttpResponse('Everything worked :)')
    except Exception, e:
        return HttpResponseServerError(str(e))
